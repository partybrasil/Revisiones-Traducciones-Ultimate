"""API routes for version control operations."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from database import get_db
from core.version_manager import VersionManager


router = APIRouter()


class SnapshotCreate(BaseModel):
    """Schema for creating a snapshot."""
    version_type: str = Field(default="minor", pattern="^(major|minor|patch)$")
    change_summary: str = Field(default="", max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "version_type": "minor",
                "change_summary": "Traducción completa a portugués"
            }
        }


@router.get("/{sku}/versions")
async def get_product_versions(
    sku: str,
    db: Session = Depends(get_db)
):
    """Get all versions for a product."""
    manager = VersionManager(db)
    versions = manager.get_versions(sku)
    
    return {
        "sku": sku,
        "total_versions": len(versions),
        "versions": [v.to_dict() for v in versions]
    }


@router.get("/{sku}/versions/{version_number}")
async def get_version_snapshot(
    sku: str,
    version_number: str,
    db: Session = Depends(get_db)
):
    """Get a specific version snapshot."""
    manager = VersionManager(db)
    snapshot = manager.get_snapshot(sku, version_number)
    
    if not snapshot:
        raise HTTPException(
            status_code=404,
            detail=f"Version {version_number} not found for product {sku}"
        )
    
    return snapshot


@router.post("/{sku}/versions", status_code=201)
async def create_version_snapshot(
    sku: str,
    snapshot_data: SnapshotCreate,
    db: Session = Depends(get_db)
):
    """Create a new version snapshot."""
    manager = VersionManager(db)
    
    version = manager.create_snapshot(
        sku=sku,
        version_type=snapshot_data.version_type,
        change_summary=snapshot_data.change_summary,
        created_by="system"
    )
    
    if not version:
        raise HTTPException(status_code=404, detail=f"Product with SKU {sku} not found")
    
    return version.to_dict()


@router.get("/{sku}/changelog")
async def get_product_changelog(
    sku: str,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get changelog history for a product."""
    manager = VersionManager(db)
    changelog = manager.get_changelog(sku, limit=limit)
    
    return {
        "sku": sku,
        "total_entries": len(changelog),
        "changelog": [c.to_dict() for c in changelog]
    }


@router.get("/{sku}/changelog/compare")
async def compare_versions(
    sku: str,
    version_from: str = Query(..., alias="from"),
    version_to: str = Query(..., alias="to"),
    db: Session = Depends(get_db)
):
    """Compare two versions and show differences."""
    manager = VersionManager(db)
    
    comparison = manager.compare_versions(sku, version_from, version_to)
    
    if "error" in comparison:
        raise HTTPException(status_code=404, detail=comparison["error"])
    
    return comparison


@router.post("/{sku}/versions/{version_number}/restore")
async def restore_version(
    sku: str,
    version_number: str,
    db: Session = Depends(get_db)
):
    """Restore a product to a previous version."""
    manager = VersionManager(db)
    
    product = manager.restore_version(sku, version_number, restored_by="system")
    
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Version {version_number} not found for product {sku}"
        )
    
    return {
        "message": f"Product restored to version {version_number}",
        "current_version": product.current_version,
        "product": product.to_dict()
    }


@router.get("/{sku}/timeline")
async def get_version_timeline(
    sku: str,
    db: Session = Depends(get_db)
):
    """Get visual timeline of versions."""
    manager = VersionManager(db)
    versions = manager.get_versions(sku)
    
    timeline = []
    for v in versions:
        timeline.append({
            "version_number": v.version_number,
            "version_type": v.version_type,
            "status": v.status,
            "snapshot_date": v.snapshot_date.isoformat() if v.snapshot_date else None,
            "created_by": v.created_by,
            "change_summary": v.change_summary,
            "is_current": v.status == "current"
        })
    
    return {
        "sku": sku,
        "timeline": timeline
    }
