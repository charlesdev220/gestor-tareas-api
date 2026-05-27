# Esquemas Pydantic para validación de datos de entrada y serialización de respuestas

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from aplicacion.modelos import TaskStatus


class TaskCreate(BaseModel):
    """Esquema de entrada para crear una nueva tarea.

    Solo el título es obligatorio; el estado por defecto es ``pending``.
    """

    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending


class TaskUpdate(BaseModel):
    """Esquema de entrada para actualizar parcialmente una tarea (PATCH).

    Todos los campos son opcionales; solo se modifican los enviados.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskResponse(BaseModel):
    """Esquema de respuesta que devuelve la API.

    Incluye todos los campos de la tarea, incluidos los generados
    automáticamente por la base de datos (``id``, ``created_at``).
    """

    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime

    model_config = {"from_attributes": True}
