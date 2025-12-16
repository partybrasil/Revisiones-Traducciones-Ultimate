"""
API Routes - Image Management

Endpoints para búsqueda, upload y gestión de imágenes de productos.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Añadir backend al path
sys.path.append(str(Path(__file__).parent.parent))

from image_handler.image_scraper import ImageScraper
from image_handler.image_storage import ImageStorage


router = APIRouter(prefix="/api/images", tags=["images"])

# Inicializar managers
image_scraper = ImageScraper()
image_storage = ImageStorage()


# --- Pydantic Models ---

class ImageSearchResult(BaseModel):
    """Resultado de búsqueda de imágenes."""
    url: str
    title: str
    source: str
    resolution: tuple
    estimated_size_kb: int = 0


class ImageUploadResponse(BaseModel):
    """Respuesta de upload de imagen."""
    status: str
    message: str
    path: str
    size_kb: float


class ImageInfo(BaseModel):
    """Información de una imagen."""
    filename: str
    path: str
    relative_path: str
    type: str
    size_kb: float
    created_at: str


class ImageStatsResponse(BaseModel):
    """Estadísticas de almacenamiento de imágenes."""
    total_images: int
    total_size_mb: float
    images_by_type: Dict[str, Dict]
    skus_count: int = 0


# --- Routes ---

@router.get("/search", response_model=List[ImageSearchResult])
async def search_images(
    q: str = Query(..., description="Término de búsqueda"),
    max_results: int = Query(20, ge=1, le=50, description="Máximo de resultados")
):
    """
    Buscar imágenes en la web.
    
    Args:
        q: Término de búsqueda
        max_results: Número máximo de resultados (1-50)
    
    Returns:
        Lista de resultados con URLs, títulos y metadata
    """
    try:
        results = image_scraper.search_images(q, max_results)
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/{sku}", response_model=ImageUploadResponse)
async def upload_image(
    sku: str,
    image_type: str = Query("general", description="Tipo de imagen"),
    file: UploadFile = File(...)
):
    """
    Subir imagen de producto.
    
    Args:
        sku: SKU del producto
        image_type: Tipo de imagen (frontal, trasera, lateral, general, etc.)
        file: Archivo de imagen
    
    Validaciones:
    - Formato: JPG, PNG, GIF, WEBP
    - Tamaño máximo: 10MB
    - Resolución mínima: 100x100px
    """
    try:
        # Validar tipo de imagen
        if image_type not in image_storage.VALID_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image_type. Must be one of: {image_storage.VALID_IMAGE_TYPES}"
            )
        
        # Leer archivo
        file_bytes = await file.read()
        
        # Guardar
        saved_path = image_storage.save_uploaded_file(
            file_bytes=file_bytes,
            filename=file.filename,
            sku=sku,
            image_type=image_type
        )
        
        if not saved_path:
            raise HTTPException(status_code=400, detail="Failed to save image. Invalid file.")
        
        # Calcular tamaño
        size_kb = len(file_bytes) / 1024
        
        return {
            "status": "success",
            "message": f"Image uploaded successfully for {sku}",
            "path": saved_path,
            "size_kb": round(size_kb, 2)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{sku}/list", response_model=List[ImageInfo])
async def list_images(
    sku: str,
    image_type: Optional[str] = Query(None, description="Filtrar por tipo de imagen")
):
    """
    Listar imágenes de un producto.
    
    Args:
        sku: SKU del producto
        image_type: Tipo de imagen (opcional, para filtrar)
    
    Returns:
        Lista de imágenes con metadata
    """
    try:
        images = image_storage.list_images(sku, image_type)
        return images
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{sku}/{image_type}/{filename}")
async def get_image(sku: str, image_type: str, filename: str):
    """
    Obtener imagen específica.
    
    Args:
        sku: SKU del producto
        image_type: Tipo de imagen
        filename: Nombre del archivo
    
    Returns:
        Archivo de imagen
    """
    try:
        filepath = image_storage.get_image_path(sku, image_type, filename)
        
        if not filepath:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Detectar media type
        ext = Path(filepath).suffix.lower()
        media_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        media_type = media_type_map.get(ext, 'image/jpeg')
        
        return FileResponse(filepath, media_type=media_type)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{sku}/{image_type}")
async def delete_images(
    sku: str,
    image_type: str,
    filename: Optional[str] = Query(None, description="Archivo específico (opcional)")
):
    """
    Eliminar imagen(es) de un producto.
    
    Args:
        sku: SKU del producto
        image_type: Tipo de imagen
        filename: Nombre específico del archivo (opcional). Si no se provee, elimina todas del tipo.
    
    Returns:
        Confirmación de eliminación
    """
    try:
        success = image_storage.delete_image(sku, image_type, filename)
        
        if not success:
            raise HTTPException(status_code=404, detail="Image(s) not found")
        
        return {
            "status": "success",
            "message": f"Image(s) deleted successfully",
            "sku": sku,
            "image_type": image_type,
            "filename": filename or "all"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{sku}/all")
async def delete_all_images(sku: str):
    """
    Eliminar todas las imágenes de un producto.
    
    Args:
        sku: SKU del producto
    
    Returns:
        Confirmación de eliminación
    """
    try:
        success = image_storage.delete_all_images(sku)
        
        if not success:
            raise HTTPException(status_code=404, detail="No images found for this product")
        
        return {
            "status": "success",
            "message": f"All images deleted for {sku}",
            "sku": sku
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{sku}/download-from-url")
async def download_image_from_url(
    sku: str,
    url: str = Query(..., description="URL de la imagen"),
    image_type: str = Query("general", description="Tipo de imagen")
):
    """
    Descargar imagen desde URL y guardarla.
    
    Args:
        sku: SKU del producto
        url: URL de la imagen
        image_type: Tipo de imagen
    
    Returns:
        Confirmación de descarga
    """
    try:
        saved_path = image_scraper.download_image(url, sku, image_type)
        
        if not saved_path:
            raise HTTPException(status_code=400, detail="Failed to download image from URL")
        
        return {
            "status": "success",
            "message": "Image downloaded and saved successfully",
            "url": url,
            "saved_path": saved_path,
            "sku": sku,
            "image_type": image_type
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=ImageStatsResponse)
async def get_storage_stats(sku: Optional[str] = Query(None)):
    """
    Obtener estadísticas de almacenamiento de imágenes.
    
    Args:
        sku: SKU específico (opcional). Si no se provee, stats globales.
    
    Returns:
        Estadísticas de almacenamiento
    """
    try:
        stats = image_storage.get_storage_stats(sku)
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types")
async def get_image_types():
    """
    Obtener tipos de imagen válidos.
    
    Returns:
        Lista de tipos de imagen permitidos
    """
    return {
        "valid_types": image_storage.VALID_IMAGE_TYPES,
        "allowed_extensions": list(image_storage.ALLOWED_EXTENSIONS)
    }
