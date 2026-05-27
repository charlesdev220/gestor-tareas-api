# Tests e2e para el endpoint PATCH /tasks/{id} — bloqueo de tareas completadas

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from aplicacion.base_de_datos import Base, get_db
from aplicacion.principal import app

# Base de datos en memoria aislada para los tests
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Provee una sesión de BD en memoria para los tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    """Crea todas las tablas antes de cada test."""
    Base.metadata.create_all(bind=engine)


def teardown_function():
    """Elimina todas las tablas después de cada test."""
    Base.metadata.drop_all(bind=engine)


def _create_task(**kwargs):
    """Crea una tarea de prueba vía POST y devuelve el JSON de respuesta."""
    body = {"title": "Tarea de prueba", **kwargs}
    resp = client.post("/tasks/", json=body)
    assert resp.status_code == 201
    return resp.json()


def test_update_done_task_returns_400():
    """Modificar una tarea con estado 'done' debe devolver 400."""
    task = _create_task()
    # Llevar la tarea a estado "done"
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "done"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "done"

    # Intentar modificar la tarea completada
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "Nuevo título"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Cannot update a completed task"


def test_update_pending_task_succeeds():
    """Modificar una tarea pendiente debe funcionar normalmente."""
    task = _create_task()
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "Título actualizado"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Título actualizado"


def test_update_in_progress_task_succeeds():
    """Modificar una tarea en progreso debe funcionar normalmente."""
    task = _create_task()
    client.patch(f"/tasks/{task['id']}", json={"status": "in_progress"})

    resp = client.patch(f"/tasks/{task['id']}", json={"title": "Actualizada"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Actualizada"


def test_update_done_task_status_change_blocked():
    """Cambiar el estado de una tarea 'done' también debe devolver 400."""
    task = _create_task()
    client.patch(f"/tasks/{task['id']}", json={"status": "done"})

    resp = client.patch(f"/tasks/{task['id']}", json={"status": "pending"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Cannot update a completed task"
