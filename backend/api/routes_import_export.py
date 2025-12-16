"""
API Routes - Import/Export Manager

Endpoints para importación/exportación masiva de productos.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path
import io

# Añadir backend al path
sys.path.append(str(Path(__file__).parent.parent))

from import_export.import_export_manager import ImportExportManager
from database import get_db

router = APIRouter(prefix="/api/import-export", tags=["import-export"])


# --- Pydantic Models ---

class ImportResultResponse(BaseModel):
    """Resultado de importación desde Excel."""
    imported: int
    errors: List[Dict]
    skipped: int
    status: str
    completion_percentage: int
    message: str


class ExportFiltersRequest(BaseModel):
    """Filtros para exportación de catálogo."""
    family: Optional[str] = None
    brand: Optional[str] = None
    status: Optional[str] = None
    created_after: Optional[str] = None


# --- Routes ---

@router.get("/template/excel")
async def download_excel_template():
    """
    Descargar template Excel para importación masiva.
    
    Retorna archivo Excel con:
    - 60+ columnas
    - Headers con colores (🔴 crítico, 🟡 recomendado, ⚪ opcional)
    - Fila de ejemplo con datos demo
    - Dropdowns de validación (Family, Format, PAO, etc.)
    """
    try:
        # Obtener session de DB
        db = next(get_db())
        manager = ImportExportManager(db)
        
        # Generar template
        excel_bytes = manager.generate_excel_template()
        
        # Retornar como descarga
        return StreamingResponse(
            io.BytesIO(excel_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=productos_template_{Path().cwd().name}.xlsx"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/excel", response_model=ImportResultResponse)
async def import_from_excel(file: UploadFile = File(...)):
    """
    Importar productos desde archivo Excel.
    
    Valida:
    - SKU formato
    - EAN checksum
    - Family válida
    - Campos requeridos
    
    Crea:
    - ProductSheets en DB
    - Aplica presets automáticamente
    - Crea v1.0 snapshots
    """
    try:
        # Validar tipo de archivo
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only .xlsx and .xls files are allowed"
            )
        
        # Guardar archivo temporalmente
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Obtener session de DB
        db = next(get_db())
        manager = ImportExportManager(db)
        
        # Importar
        result = manager.import_from_excel(temp_path, current_user_id="api_user")
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/markdown/{sku}")
async def export_to_markdown(sku: str):
    """
    Exportar ficha de producto a formato Markdown.
    
    Args:
        sku: SKU del producto
    """
    try:
        db = next(get_db())
        manager = ImportExportManager(db)
        
        # Generar Markdown
        md_content = manager.export_to_markdown(sku)
        
        # Retornar como descarga
        return Response(
            content=md_content,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f"attachment; filename=ficha_{sku}.md"
            }
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/html/{sku}")
async def export_to_html(sku: str):
    """
    Exportar ficha de producto a formato HTML.
    
    Args:
        sku: SKU del producto
    """
    try:
        db = next(get_db())
        manager = ImportExportManager(db)
        
        # Generar HTML
        html_content = manager.export_to_html(sku)
        
        # Retornar como descarga
        return Response(
            content=html_content,
            media_type="text/html",
            headers={
                "Content-Disposition": f"attachment; filename=ficha_{sku}.html"
            }
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/catalog-excel")
async def export_catalog_excel(
    family: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """
    Exportar catálogo de productos a Excel con filtros.
    
    Args:
        family: Filtrar por familia (opcional)
        brand: Filtrar por marca (opcional)
        status: Filtrar por estado (opcional)
    """
    try:
        db = next(get_db())
        manager = ImportExportManager(db)
        
        # Aplicar filtros
        filters = {}
        if family:
            filters["family"] = family
        if brand:
            filters["brand"] = brand
        if status:
            filters["status"] = status
        
        # Generar Excel
        excel_bytes = manager.export_catalog_excel(filters)
        
        # Retornar como descarga
        return StreamingResponse(
            io.BytesIO(excel_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=catalogo_productos.xlsx"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_import_export_stats():
    """
    Obtener estadísticas de import/export.
    """
    try:
        db = next(get_db())
        manager = ImportExportManager(db)
        
        # Por ahora retornar info básica
        return {
            "excel_columns_count": len(manager.EXCEL_COLUMNS),
            "valid_families_count": len(manager.VALID_FAMILIES),
            "supported_formats": {
                "import": ["xlsx", "xls"],
                "export": ["xlsx", "pdf", "markdown", "html"]
            },
            "max_file_size_mb": 10
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
