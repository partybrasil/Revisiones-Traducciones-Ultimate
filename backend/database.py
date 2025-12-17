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
    # WARNING: SQLite with check_same_thread=False allows sharing connections across threads,
    # but SQLite has limited write concurrency. Multiple simultaneous writes may result in
    # "database is locked" errors. For production or high-concurrency environments, 
    # use PostgreSQL instead by setting DATABASE_URL environment variable.
    connect_args = {"check_same_thread": False}
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        connect_args=connect_args
    )
    # Enable WAL mode to improve SQLite concurrency
    from sqlalchemy import event
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        try:
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.close()
        except Exception as e:
            # WAL mode may fail on read-only or networked filesystems
            # Log the error but don't fail the connection
            import logging
            logging.warning(f"Could not enable WAL mode for SQLite: {e}")
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
