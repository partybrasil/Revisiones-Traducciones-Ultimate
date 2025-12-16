"""API routes for legal compliance operations."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from database import get_db
from legal_framework.compliance_validator import ComplianceValidator
from core.product_sheet_manager import ProductSheetManager


router = APIRouter()


class ValidateRequest(BaseModel):
    """Schema for validation request."""
    sku: str
    countries: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "sku": "CF-HYD-001",
                "countries": ["PT", "IT", "ES"]
            }
        }


@router.get("/countries")
async def get_available_countries():
    """Get list of available countries with legal frameworks."""
    validator = ComplianceValidator()
    countries = validator.get_available_countries()
    
    country_info = []
    for country in countries:
        rules = validator.get_country_rules(country)
        if rules:
            country_info.append({
                "code": country,
                "name": rules.get('country', country),
                "authority": rules.get('authority', ''),
                "authority_url": rules.get('authority_url', '')
            })
    
    return {
        "countries": country_info,
        "total": len(country_info)
    }


@router.get("/{country}/rules")
async def get_country_rules(country: str):
    """Get legal rules for a specific country."""
    validator = ComplianceValidator()
    rules = validator.get_country_rules(country)
    
    if not rules:
        raise HTTPException(
            status_code=404,
            detail=f"No legal framework found for country: {country}"
        )
    
    return rules


@router.get("/{country}/{family}/requirements")
async def get_family_requirements(country: str, family: str):
    """Get requirements for a specific product family in a country."""
    validator = ComplianceValidator()
    requirements = validator.get_family_requirements(country, family)
    
    if not requirements:
        raise HTTPException(
            status_code=404,
            detail=f"No requirements found for {family} in {country}"
        )
    
    return requirements


@router.post("/validate")
async def validate_compliance(
    request: ValidateRequest,
    db: Session = Depends(get_db)
):
    """Validate product compliance against multiple countries."""
    # Get product data
    manager = ProductSheetManager(db)
    product = manager.get_sheet(request.sku)
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with SKU {request.sku} not found")
    
    # Validate against each country
    validator = ComplianceValidator()
    product_data = product.to_dict()
    
    results = validator.validate_multiple_countries(product_data, request.countries)
    
    return results


@router.get("/products/{sku}/compliance/{country}")
async def get_product_compliance(
    sku: str,
    country: str,
    db: Session = Depends(get_db)
):
    """Get compliance status for a product in a specific country."""
    # Get product
    manager = ProductSheetManager(db)
    product = manager.get_sheet(sku)
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with SKU {sku} not found")
    
    # Validate compliance
    validator = ComplianceValidator()
    product_data = product.to_dict()
    
    result = validator.validate_for_country(product_data, country)
    
    return result


@router.get("/products/{sku}/compliance")
async def get_product_compliance_all(
    sku: str,
    db: Session = Depends(get_db)
):
    """Get compliance status for a product in all available countries."""
    # Get product
    manager = ProductSheetManager(db)
    product = manager.get_sheet(sku)
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with SKU {sku} not found")
    
    # Get all countries
    validator = ComplianceValidator()
    countries = validator.get_available_countries()
    
    # Validate against all countries
    product_data = product.to_dict()
    results = validator.validate_multiple_countries(product_data, countries)
    
    return results
