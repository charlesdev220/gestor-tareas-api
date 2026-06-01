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


def test_update_task_title_too_short_returns_422():
    """Actualizar una tarea con un título de menos de 3 caracteres debe devolver 422."""
    task = _create_task()
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "AB"})
    assert resp.status_code == 422
    assert "El título debe tener al menos 3 caracteres" in resp.text


# --- Tests del campo prioridad ---


def test_create_task_default_priority_is_medium():
    """Crear una tarea sin especificar prioridad asigna 'medium' por defecto."""
    task = _create_task()
    assert task["priority"] == "medium"


def test_create_task_with_explicit_priority():
    """Crear una tarea con prioridad explícita la almacena correctamente."""
    task = _create_task(priority="high")
    assert task["priority"] == "high"


def test_create_task_with_invalid_priority_returns_422():
    """Crear una tarea con prioridad inválida devuelve 422."""
    resp = client.post("/tasks/", json={"title": "Tarea", "priority": "urgent"})
    assert resp.status_code == 422


def test_update_task_priority():
    """Actualizar la prioridad de una tarea existente funciona correctamente."""
    task = _create_task()
    resp = client.patch(f"/tasks/{task['id']}", json={"priority": "high"})
    assert resp.status_code == 200
    assert resp.json()["priority"] == "high"


def test_update_task_invalid_priority_returns_422():
    """Actualizar una tarea con prioridad inválida devuelve 422."""
    task = _create_task()
    resp = client.patch(f"/tasks/{task['id']}", json={"priority": "critical"})
    assert resp.status_code == 422


def test_list_tasks_filter_by_priority():
    """Filtrar tareas por prioridad devuelve solo las que coinciden."""
    _create_task(priority="low")
    _create_task(priority="high")
    _create_task(priority="high")

    resp = client.get("/tasks/", params={"priority": "high"})
    assert resp.status_code == 200
    tasks = resp.json()
    assert len(tasks) == 2
    assert all(t["priority"] == "high" for t in tasks)


def test_list_tasks_filter_invalid_priority_returns_422():
    """Filtrar tareas con prioridad inválida devuelve 422."""
    resp = client.get("/tasks/", params={"priority": "urgent"})
    assert resp.status_code == 422
