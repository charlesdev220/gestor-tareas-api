# Configuración de la conexión a la base de datos con SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./tareas.db"

# Motor de base de datos; check_same_thread es necesario para SQLite con FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fábrica de sesiones: cada petición obtiene su propia sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredan todos los modelos ORM
Base = declarative_base()


def get_db():
    """Dependencia de FastAPI que provee una sesión de base de datos.

    Abre una sesión, la cede al endpoint que la solicita y la cierra
    automáticamente al terminar la petición.

    Yields:
        Session: sesión activa de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
