# Esquemas Pydantic para validación de datos de entrada y serialización de respuestas

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

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

    Raises:
        ValueError: si ``title`` tiene menos de 3 caracteres.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

    @field_validator("title")
    @classmethod
    def title_min_length(cls, v: str | None) -> str | None:
        """Valida que el título tenga al menos 3 caracteres."""
        if v is not None and len(v) < 3:
            raise ValueError("El título debe tener al menos 3 caracteres")
        return v


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
