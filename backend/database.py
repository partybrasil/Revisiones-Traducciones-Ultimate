"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Use absolute import so launcher works when executed from repo root
from backend.config import settings

# Configure engine based on database type
connect_args = {}
if settings.database_url.startswith("sqlite"):
    # SQLite specific configuration
    connect_args = {"check_same_thread": False}
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        connect_args=connect_args
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency for FastAPI to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
