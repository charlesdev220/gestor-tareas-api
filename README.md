# API de Gestión de Tareas

API REST para gestionar tareas construida con **FastAPI** y **SQLAlchemy**. Permite crear, consultar, actualizar y eliminar tareas. Cada tarea tiene un identificador, título, descripción opcional, estado (`pending`, `in_progress`, `done`) y fecha de creación automática.

---

## Requisitos previos

| Requisito | Versión mínima |
|-----------|---------------|
| Python | 3.12+ |

### Dependencias principales

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| FastAPI | 0.136.1 | Framework web asíncrono |
| SQLAlchemy | 2.0.49 | ORM para acceso a base de datos |
| Pydantic | 2.13.4 | Validación y serialización de datos |
| Uvicorn | 0.46.0 | Servidor ASGI |
| pytest | 9.0.3 | Framework de tests |
| httpx | 0.28.1 | Cliente HTTP para tests |

---

## Instalación paso a paso

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/charlesdev220/gestor-tareas-api.git
   cd gestor-tareas-api
   ```

2. **Crear y activar el entorno virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. **Instalar las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Cómo arrancar la aplicación

```bash
uvicorn aplicacion.principal:app --reload
```

La API quedará disponible en `http://127.0.0.1:8000`.

La documentación interactiva (Swagger UI) se genera automáticamente en `http://127.0.0.1:8000/docs`.

---

## Endpoints

Todos los endpoints operan bajo el prefijo `/tasks`.

### 1. Listar tareas

| | |
|---|---|
| **Método** | `GET` |
| **Ruta** | `/tasks/` |

**Parámetros de query** (opcionales):

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `status` | string | Filtra por estado (`pending`, `in_progress`, `done`) |
| `limit` | int | Número máximo de tareas a devolver (>= 1) |

**Ejemplo con curl:**

```bash
curl -X GET "http://127.0.0.1:8000/tasks/?status=pending&limit=5"
```

**Ejemplo de respuesta** (`200 OK`):

```json
[
  {
    "id": 1,
    "title": "Revisar documentación",
    "description": "Actualizar el README del proyecto",
    "status": "pending",
    "created_at": "2025-05-27T10:30:00"
  }
]
```

---

### 2. Obtener una tarea por id

| | |
|---|---|
| **Método** | `GET` |
| **Ruta** | `/tasks/{task_id}` |
| **Parámetros de ruta** | `task_id` (int) — Identificador de la tarea |

**Ejemplo con curl:**

```bash
curl -X GET http://127.0.0.1:8000/tasks/1
```

**Ejemplo de respuesta** (`200 OK`):

```json
{
  "id": 1,
  "title": "Revisar documentación",
  "description": "Actualizar el README del proyecto",
  "status": "pending",
  "created_at": "2025-05-27T10:30:00"
}
```

**Error** (`404 Not Found`):

```json
{
  "detail": "Task not found"
}
```

---

### 3. Crear una nueva tarea

| | |
|---|---|
| **Método** | `POST` |
| **Ruta** | `/tasks/` |
| **Content-Type** | `application/json` |

**Parámetros del cuerpo:**

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `title` | string | Sí | Título de la tarea |
| `description` | string | No | Descripción de la tarea |
| `status` | string | No | Estado inicial (`pending`, `in_progress`, `done`). Por defecto: `pending` |

**Ejemplo con curl:**

```bash
curl -X POST http://127.0.0.1:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Nueva tarea", "description": "Descripción de ejemplo"}'
```

**Ejemplo de respuesta** (`201 Created`):

```json
{
  "id": 2,
  "title": "Nueva tarea",
  "description": "Descripción de ejemplo",
  "status": "pending",
  "created_at": "2025-05-27T11:00:00"
}
```

---

### 4. Actualizar parcialmente una tarea

| | |
|---|---|
| **Método** | `PATCH` |
| **Ruta** | `/tasks/{task_id}` |
| **Parámetros de ruta** | `task_id` (int) — Identificador de la tarea |
| **Content-Type** | `application/json` |

**Parámetros del cuerpo** (todos opcionales):

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `title` | string | Nuevo título |
| `description` | string | Nueva descripción |
| `status` | string | Nuevo estado (`pending`, `in_progress`, `done`) |

> **Nota:** Las tareas con estado `done` no pueden ser actualizadas. El servidor devolverá `400 Bad Request`.

**Ejemplo con curl:**

```bash
curl -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

**Ejemplo de respuesta** (`200 OK`):

```json
{
  "id": 1,
  "title": "Revisar documentación",
  "description": "Actualizar el README del proyecto",
  "status": "in_progress",
  "created_at": "2025-05-27T10:30:00"
}
```

**Error** — tarea no encontrada (`404 Not Found`):

```json
{
  "detail": "Task not found"
}
```

**Error** — tarea ya completada (`400 Bad Request`):

```json
{
  "detail": "Cannot update a completed task"
}
```

---

### 5. Eliminar una tarea

| | |
|---|---|
| **Método** | `DELETE` |
| **Ruta** | `/tasks/{task_id}` |
| **Parámetros de ruta** | `task_id` (int) — Identificador de la tarea |

**Ejemplo con curl:**

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

**Respuesta exitosa:** `204 No Content` (sin cuerpo).

**Error** (`404 Not Found`):

```json
{
  "detail": "Task not found"
}
```

---

## Cómo ejecutar los tests

```bash
pytest tests/ -v
```

Los tests utilizan una base de datos SQLite en memoria con `StaticPool` para garantizar aislamiento entre casos. No tocan el archivo `tareas.db` de producción.

---

## Estructura del proyecto

```
gestor-tareas-api/
├── aplicacion/                  # Paquete principal de la aplicación
│   ├── __init__.py
│   ├── principal.py             # Punto de entrada: instancia FastAPI y registro de routers
│   ├── base_de_datos.py         # Configuración del engine y sesión de SQLAlchemy
│   ├── modelos.py               # Modelos ORM (tabla tasks, enum TaskStatus)
│   ├── esquemas.py              # Esquemas Pydantic de entrada y respuesta
│   └── rutas/                   # Definición de endpoints REST
│       ├── __init__.py
│       └── tareas.py            # Endpoints CRUD de tareas
├── tests/                       # Suite de tests
│   ├── __init__.py
│   └── test_tasks.py            # Tests con pytest y SQLite en memoria
├── AGENTS.md                    # Instrucciones y convenciones para Devin
├── requirements.txt             # Dependencias del proyecto
├── .gitignore
└── README.md
```

| Archivo / Carpeta | Descripción |
|-------------------|-------------|
| `aplicacion/principal.py` | Crea la instancia de FastAPI, genera las tablas e incluye el router de tareas |
| `aplicacion/base_de_datos.py` | Define el engine SQLite, la fábrica de sesiones (`SessionLocal`) y la dependencia `get_db` |
| `aplicacion/modelos.py` | Modelo ORM `Task` con campos `id`, `title`, `description`, `status` y `created_at`; enum `TaskStatus` |
| `aplicacion/esquemas.py` | Esquemas Pydantic: `TaskCreate` (POST), `TaskUpdate` (PATCH) y `TaskResponse` (salida) |
| `aplicacion/rutas/tareas.py` | Endpoints REST: listar, obtener, crear, actualizar y eliminar tareas |
| `tests/test_tasks.py` | Tests e2e usando `TestClient` de FastAPI con base de datos en memoria |
| `requirements.txt` | Dependencias de producción y desarrollo |
| `AGENTS.md` | Convenciones de código, estilo y lineamientos del proyecto |
