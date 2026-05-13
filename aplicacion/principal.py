# Punto de entrada de la aplicación FastAPI

from fastapi import FastAPI

from aplicacion.base_de_datos import Base, engine
from aplicacion.rutas import tareas

# Crea todas las tablas en la base de datos si todavía no existen
Base.metadata.create_all(bind=engine)

# Instancia principal de la aplicación
app = FastAPI(title="API de Gestión de Tareas")

# Registro del router de tareas bajo el prefijo /tasks
app.include_router(tareas.router)
