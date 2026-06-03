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


# ── Tests para list_tasks: filtro por status y limit ──


def test_list_tasks_no_filter_returns_all():
    """Sin filtros, list_tasks debe devolver todas las tareas."""
    _create_task(title="Tarea A")
    _create_task(title="Tarea B")
    _create_task(title="Tarea C")

    resp = client.get("/tasks/")
    assert resp.status_code == 200
    assert len(resp.json()) == 3


def test_list_tasks_filter_by_status():
    """Filtrar por status devuelve solo las tareas con ese estado."""
    _create_task(title="Pendiente")
    task_ip = _create_task(title="En progreso")
    client.patch(f"/tasks/{task_ip['id']}", json={"status": "in_progress"})

    resp = client.get("/tasks/", params={"status": "in_progress"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["status"] == "in_progress"


def test_list_tasks_filter_by_status_no_match():
    """Si no hay tareas con el estado indicado, devuelve lista vacía."""
    _create_task(title="Pendiente")

    resp = client.get("/tasks/", params={"status": "done"})
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_tasks_limit():
    """El parámetro limit restringe la cantidad de tareas devueltas."""
    _create_task(title="Tarea A")
    _create_task(title="Tarea B")
    _create_task(title="Tarea C")

    resp = client.get("/tasks/", params={"limit": 2})
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_list_tasks_limit_greater_than_total():
    """Si limit es mayor que el total de tareas, devuelve todas."""
    _create_task(title="Tarea A")
    _create_task(title="Tarea B")

    resp = client.get("/tasks/", params={"limit": 100})
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_list_tasks_filter_status_and_limit():
    """Combinar status y limit aplica ambos filtros."""
    _create_task(title="Pendiente 1")
    _create_task(title="Pendiente 2")
    _create_task(title="Pendiente 3")
    task_ip = _create_task(title="En progreso")
    client.patch(f"/tasks/{task_ip['id']}", json={"status": "in_progress"})

    resp = client.get("/tasks/", params={"status": "pending", "limit": 2})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    assert all(t["status"] == "pending" for t in data)


def test_list_tasks_invalid_limit_returns_422():
    """Un valor de limit menor que 1 debe devolver 422."""
    resp = client.get("/tasks/", params={"limit": 0})
    assert resp.status_code == 422


def test_list_tasks_invalid_status_returns_422():
    """Un valor de status inválido debe devolver 422."""
    resp = client.get("/tasks/", params={"status": "invalid"})
    assert resp.status_code == 422
