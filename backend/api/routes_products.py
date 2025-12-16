"""API routes for product sheet operations."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from database import get_db
from core.product_sheet_manager import ProductSheetManager


router = APIRouter()


class ProductSheetCreate(BaseModel):
    """Schema for creating a product sheet."""
    sku: str = Field(..., min_length=1, max_length=50)
    ean_list: List[str] = Field(default_factory=list)
    brand: Optional[str] = None
    family: str = Field(..., min_length=1)
    title_short: Dict[str, str] = Field(default_factory=dict)
    description_detailed: Dict[str, str] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "sku": "CF-HYD-001",
                "ean_list": ["5412345678901"],
                "brand": "Cosmetics Brand",
                "family": "COSMETICS_FACIAL",
                "title_short": {
                    "es": "Crema Hidratante Facial"
                }
            }
        }


class ProductSheetUpdate(BaseModel):
    """Schema for updating a product sheet."""
    ean_list: Optional[List[str]] = None
    brand: Optional[str] = None
    family: Optional[str] = None
    title_short: Optional[Dict[str, str]] = None
    description_detailed: Optional[Dict[str, str]] = None
    status: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title_short": {
                    "pt": "Creme Hidratante Facial"
                },
                "status": "in_review"
            }
        }


class ProductSheetResponse(BaseModel):
    """Schema for product sheet response."""
    sku: str
    family: str
    brand: Optional[str] = None
    title_short: Dict[str, str]
    current_version: str
    status: str
    completion_percentage: int
    created_date: str
    updated_date: str
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for product list response."""
    products: List[Dict[str, Any]]
    total: int
    page: int
    per_page: int
    pages: int


@router.post("/", response_model=Dict[str, Any], status_code=201)
async def create_product(
    product: ProductSheetCreate,
    db: Session = Depends(get_db)
):
    """Create a new product sheet."""
    manager = ProductSheetManager(db)
    
    # Check if SKU already exists
    existing = manager.get_sheet(product.sku)
    if existing:
        raise HTTPException(status_code=400, detail=f"Product with SKU {product.sku} already exists")
    
    # Create product
    new_product = manager.create_sheet(product.dict(), created_by="system")
    
    return new_product.to_dict()


@router.get("/", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
    family: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List all product sheets with filters and pagination."""
    manager = ProductSheetManager(db)
    
    filters = {}
    if family:
        filters['family'] = family
    if brand:
        filters['brand'] = brand
    if status:
        filters['status'] = status
    
    products, total = manager.list_sheets(
        filters=filters,
        page=page,
        per_page=per_page
    )
    
    return {
        "products": [p.to_dict() for p in products],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }


@router.get("/search")
async def search_products(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Search products by SKU, EAN, or title."""
    manager = ProductSheetManager(db)
    results = manager.search_sheets(q)
    
    return {
        "results": [p.to_dict() for p in results],
        "count": len(results)
    }


@router.get("/{sku}", response_model=Dict[str, Any])
async def get_product(
    sku: str,
    db: Session = Depends(get_db)
):
    """Get a specific product sheet by SKU."""
    manager = ProductSheetManager(db)
    product = manager.get_sheet(sku)
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with SKU {sku} not found")
    
    return product.to_dict()


@router.put("/{sku}", response_model=Dict[str, Any])
async def update_product(
    sku: str,
    product_update: ProductSheetUpdate,
    db: Session = Depends(get_db)
):
    """Update a product sheet."""
    manager = ProductSheetManager(db)
    
    # Only include non-None fields
    update_data = {k: v for k, v in product_update.dict().items() if v is not None}
    
    product = manager.update_sheet(sku, update_data, updated_by="system")
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with SKU {sku} not found")
    
    return product.to_dict()


@router.delete("/{sku}", status_code=204)
async def delete_product(
    sku: str,
    db: Session = Depends(get_db)
):
    """Delete a product sheet."""
    manager = ProductSheetManager(db)
    
    success = manager.delete_sheet(sku)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Product with SKU {sku} not found")
    
    return None


@router.get("/{sku}/stats")
async def get_product_stats(
    sku: str,
    db: Session = Depends(get_db)
):
    """Get statistics for a specific product."""
    manager = ProductSheetManager(db)
    product = manager.get_sheet(sku)
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with SKU {sku} not found")
    
    # Calculate statistics
    stats = {
        "sku": sku,
        "completion_percentage": product.completion_percentage,
        "languages": len(product.packaging_languages) if product.packaging_languages else 0,
        "images": len(product.product_images) if product.product_images else 0,
        "certifications": len(product.certifications) if product.certifications else 0,
        "allergens_count": len(product.allergens_present) if product.allergens_present else 0,
        "pictograms_count": len(product.pictograms) if product.pictograms else 0,
        "has_inci": bool(product.inci_ingredients),
        "has_warnings": bool(product.general_warnings and len(product.general_warnings) > 0),
    }
    
    return stats
