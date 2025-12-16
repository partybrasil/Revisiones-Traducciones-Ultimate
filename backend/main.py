"""Main FastAPI application for Revisiones-Traducciones-Ultimate."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import sys

# Add parent directory to path if running from backend directory
if __name__ == "__main__" or "backend" not in sys.modules:
    from pathlib import Path
    parent_dir = Path(__file__).parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

from backend.config import settings
from backend.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application."""
    # Startup
    print("🚀 Starting Revisiones-Traducciones-Ultimate...")
    
    # Create uploads directory
    os.makedirs(settings.upload_dir, exist_ok=True)
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("👋 Shutting down Revisiones-Traducciones-Ultimate...")


# Create FastAPI application
app = FastAPI(
    title="Revisiones-Traducciones-Ultimate API",
    description="Sistema profesional para gestión de fichas de producto multiidioma con compliance regulatorio",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files
if os.path.exists(settings.upload_dir):
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Revisiones-Traducciones-Ultimate API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
    }


# Import and include routers
from api import (
    routes_products, 
    routes_versions, 
    routes_legal, 
    routes_translations,
    routes_import_export,
    routes_images
)

app.include_router(routes_products.router, prefix="/api/products", tags=["products"])
app.include_router(routes_versions.router, prefix="/api", tags=["versions"])
app.include_router(routes_legal.router, prefix="/api/legal", tags=["legal"])
app.include_router(routes_translations.router)  # Ya tiene prefix en el router
app.include_router(routes_import_export.router)  # Ya tiene prefix en el router
app.include_router(routes_images.router)  # Ya tiene prefix en el router


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
