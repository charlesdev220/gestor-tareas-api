# Definición de los endpoints REST para la gestión de tareas

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from aplicacion.base_de_datos import get_db
from aplicacion.esquemas import TaskCreate, TaskResponse, TaskUpdate
from aplicacion.modelos import Task, TaskPriority, TaskStatus

# Router con prefijo /tasks; agrupa todos los endpoints de tareas
router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    priority: TaskPriority | None = None,
    db: Session = Depends(get_db),
):
    """Devuelve la lista de tareas almacenadas, con filtro opcional por prioridad.

    Args:
        priority: filtra por nivel de prioridad (``low``, ``medium``, ``high``).

    Returns:
        Lista de ``TaskResponse`` con las tareas que cumplen el filtro.
    """
    query = db.query(Task)
    if priority is not None:
        query = query.filter(Task.priority == priority)
    return query.all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Devuelve una tarea por su identificador.

    Args:
        task_id: identificador numérico de la tarea.

    Returns:
        ``TaskResponse`` con los datos de la tarea.

    Raises:
        HTTPException 404: si la tarea no existe.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    """Crea una nueva tarea y devuelve el recurso creado.

    Args:
        payload: datos de la tarea según ``TaskCreate`` (incluye ``priority``).

    Returns:
        ``TaskResponse`` con la tarea creada (código 201).
    """
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    """Actualiza parcialmente una tarea existente.

    Solo modifica los campos incluidos en el cuerpo de la petición.
    Las tareas con estado ``done`` no pueden ser actualizadas.

    Args:
        task_id: identificador numérico de la tarea.
        payload: campos a actualizar según ``TaskUpdate``.

    Returns:
        ``TaskResponse`` con la tarea actualizada.

    Raises:
        HTTPException 404: si la tarea no existe.
        HTTPException 400: si la tarea ya está completada.
        HTTPException 422: si el título tiene menos de 3 caracteres.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.status == TaskStatus.done:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update a completed task",
        )
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Elimina una tarea de la base de datos.

    Args:
        task_id: identificador numérico de la tarea.

    Raises:
        HTTPException 404: si la tarea no existe.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()
