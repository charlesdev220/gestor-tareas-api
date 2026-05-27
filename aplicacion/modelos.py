# Definición de los modelos ORM que representan las tablas de la base de datos

import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Integer, String

from aplicacion.base_de_datos import Base


class TaskStatus(str, enum.Enum):
    """Enumeración con los estados posibles de una tarea.

    Valores:
        pending: tarea pendiente (estado inicial por defecto).
        in_progress: tarea en curso.
        done: tarea completada (estado terminal, bloquea modificaciones).
    """

    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    """Modelo ORM que representa la tabla ``tasks`` en la base de datos.

    Atributos:
        id: clave primaria autoincremental.
        title: título de la tarea (obligatorio, máx. 255 caracteres).
        description: descripción opcional de la tarea.
        status: estado actual (ver ``TaskStatus``).
        created_at: fecha y hora de creación en UTC, asignada automáticamente.
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False)
    # La fecha de creación se asigna automáticamente al insertar el registro
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
