"""Configuration module for Revisiones-Traducciones-Ultimate backend."""
from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    # BREAKING CHANGE: The default database has changed from PostgreSQL to SQLite.
    # SQLite is suitable for development and testing, but has different concurrency,
    # transaction isolation, and performance characteristics compared to PostgreSQL.
    # For production deployments with multiple concurrent users, it is strongly 
    # recommended to use PostgreSQL by setting the DATABASE_URL environment variable.
    # Example: DATABASE_URL=postgresql://user:password@localhost/dbname
    # See the migration guide and documentation for details.
    database_url: str = Field(
        default="sqlite:///./revisiones_traducciones.db",
        alias="DATABASE_URL"
    )
    
    # Security
    secret_key: str = Field(
        default="your-super-secret-key-change-in-production-min-32-chars",
        alias="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Application
    debug: bool = Field(default=True, alias="DEBUG")
    allowed_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        alias="ALLOWED_ORIGINS"
    )
    
    # File Upload
    upload_dir: str = Field(default="./uploads", alias="UPLOAD_DIR")
    max_file_size: int = Field(default=10485760, alias="MAX_FILE_SIZE")
    
    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def origins_list(self) -> List[str]:
        """Get allowed origins as a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


settings = Settings()
