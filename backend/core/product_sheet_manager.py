"""Product Sheet Manager - Business logic for product CRUD operations."""
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models.product_sheet import ProductSheet
from datetime import datetime


class ProductSheetManager:
    """Manager for product sheet operations."""
    
    def __init__(self, db: Session):
        """Initialize manager with database session."""
        self.db = db
    
    def create_sheet(self, data: Dict[str, Any], created_by: Optional[str] = None) -> ProductSheet:
        """
        Create a new product sheet.
        
        Args:
            data: Product data dictionary
            created_by: Username of creator
            
        Returns:
            Created ProductSheet instance
        """
        # Calculate completion percentage
        completion = self._calculate_completion(data)
        
        # Create product sheet
        product = ProductSheet(
            sku=data.get('sku'),
            ean_list=data.get('ean_list', []),
            internal_reference=data.get('internal_reference'),
            supplier_code=data.get('supplier_code'),
            brand=data.get('brand'),
            gama=data.get('gama', {}),
            family=data.get('family'),
            subfamily=data.get('subfamily'),
            title_short=data.get('title_short', {}),
            description_detailed=data.get('description_detailed', {}),
            made_in=data.get('made_in', {}),
            distributor=data.get('distributor', {}),
            responsible_person=data.get('responsible_person', {}),
            natural_origin_percentage=data.get('natural_origin_percentage', {}),
            net_weight_value=data.get('net_weight_value'),
            net_weight_unit=data.get('net_weight_unit'),
            gross_weight_value=data.get('gross_weight_value'),
            gross_weight_unit=data.get('gross_weight_unit'),
            height_cm=data.get('height_cm'),
            width_cm=data.get('width_cm'),
            depth_cm=data.get('depth_cm'),
            format_type=data.get('format_type'),
            format_material=data.get('format_material'),
            format_closure=data.get('format_closure'),
            packaging_languages=data.get('packaging_languages', []),
            label_positions=data.get('label_positions', {}),
            pictograms=data.get('pictograms', []),
            pao=data.get('pao'),
            inci_ingredients=data.get('inci_ingredients'),
            key_ingredients=data.get('key_ingredients', []),
            allergens_present=data.get('allergens_present', []),
            allergens_may_contain=data.get('allergens_may_contain', []),
            allergens_free_from=data.get('allergens_free_from', []),
            mode_of_use=data.get('mode_of_use', {}),
            application_frequency=data.get('application_frequency'),
            application_area=data.get('application_area'),
            general_warnings=data.get('general_warnings', {}),
            specific_warnings=data.get('specific_warnings', {}),
            storage_conditions=data.get('storage_conditions', {}),
            storage_temperature_min=data.get('storage_temperature_min'),
            storage_temperature_max=data.get('storage_temperature_max'),
            key_benefits=data.get('key_benefits', {}),
            marketing_claims=data.get('marketing_claims', {}),
            validated_claims=data.get('validated_claims', False),
            scientific_backing=data.get('scientific_backing', []),
            certifications=data.get('certifications', []),
            product_images=data.get('product_images', []),
            current_version="1.0",
            status=data.get('status', 'draft'),
            completion_percentage=completion,
            created_by=created_by,
            updated_by=created_by,
        )
        
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    def get_sheet(self, sku: str) -> Optional[ProductSheet]:
        """
        Get product sheet by SKU.
        
        Args:
            sku: Product SKU
            
        Returns:
            ProductSheet instance or None
        """
        return self.db.query(ProductSheet).filter(ProductSheet.sku == sku).first()
    
    def update_sheet(
        self,
        sku: str,
        data: Dict[str, Any],
        updated_by: Optional[str] = None
    ) -> Optional[ProductSheet]:
        """
        Update product sheet.
        
        Args:
            sku: Product SKU
            data: Updated product data
            updated_by: Username of updater
            
        Returns:
            Updated ProductSheet instance or None
        """
        product = self.get_sheet(sku)
        if not product:
            return None
        
        # Update fields
        for key, value in data.items():
            if hasattr(product, key) and key not in ['sku', 'created_date', 'created_by']:
                setattr(product, key, value)
        
        # Recalculate completion
        product.completion_percentage = self._calculate_completion(data)
        product.updated_by = updated_by
        product.updated_date = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    def delete_sheet(self, sku: str) -> bool:
        """
        Delete product sheet.
        
        Args:
            sku: Product SKU
            
        Returns:
            True if deleted, False if not found
        """
        product = self.get_sheet(sku)
        if not product:
            return False
        
        self.db.delete(product)
        self.db.commit()
        
        return True
    
    def list_sheets(
        self,
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        per_page: int = 30,
        sort_by: str = "created_date",
        sort_desc: bool = True,
    ) -> tuple[List[ProductSheet], int]:
        """
        List product sheets with filters and pagination.
        
        Args:
            filters: Dictionary of filters (family, brand, status, etc.)
            page: Page number (1-indexed)
            per_page: Results per page
            sort_by: Field to sort by
            sort_desc: Sort descending if True
            
        Returns:
            Tuple of (list of products, total count)
        """
        query = self.db.query(ProductSheet)
        
        # Apply filters
        if filters:
            if 'family' in filters and filters['family']:
                query = query.filter(ProductSheet.family == filters['family'])
            
            if 'brand' in filters and filters['brand']:
                query = query.filter(ProductSheet.brand.ilike(f"%{filters['brand']}%"))
            
            if 'status' in filters and filters['status']:
                query = query.filter(ProductSheet.status == filters['status'])
            
            if 'language' in filters and filters['language']:
                # Filter products that have content in specified language
                lang = filters['language']
                query = query.filter(
                    or_(
                        ProductSheet.title_short[lang].isnot(None),
                        ProductSheet.packaging_languages.contains([lang])
                    )
                )
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        if hasattr(ProductSheet, sort_by):
            sort_field = getattr(ProductSheet, sort_by)
            if sort_desc:
                query = query.order_by(sort_field.desc())
            else:
                query = query.order_by(sort_field.asc())
        
        # Apply pagination
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)
        
        products = query.all()
        
        return products, total
    
    def search_sheets(self, query_str: str) -> List[ProductSheet]:
        """
        Search product sheets by SKU, EAN, or title.
        
        Args:
            query_str: Search query
            
        Returns:
            List of matching products
        """
        # Search in SKU, EAN list, and titles
        results = self.db.query(ProductSheet).filter(
            or_(
                ProductSheet.sku.ilike(f"%{query_str}%"),
                ProductSheet.brand.ilike(f"%{query_str}%"),
                ProductSheet.ean_list.contains([query_str])
            )
        ).limit(50).all()
        
        return results
    
    def _calculate_completion(self, data: Dict[str, Any]) -> int:
        """
        Calculate completion percentage of a product sheet.
        
        Args:
            data: Product data dictionary
            
        Returns:
            Completion percentage (0-100)
        """
        # Define required/important fields with weights
        required_fields = {
            'sku': 5,
            'family': 5,
            'title_short': 10,
            'brand': 5,
            'inci_ingredients': 10,
            'mode_of_use': 10,
            'general_warnings': 10,
            'made_in': 5,
            'distributor': 5,
            'packaging_languages': 5,
            'net_weight_value': 5,
            'format_type': 5,
            'pao': 5,
            'allergens_present': 5,
            'product_images': 5,
            'description_detailed': 10,
        }
        
        total_weight = sum(required_fields.values())
        current_weight = 0
        
        for field, weight in required_fields.items():
            value = data.get(field)
            
            # Check if field has value
            if value:
                if isinstance(value, (dict, list)):
                    if len(value) > 0:
                        current_weight += weight
                elif isinstance(value, str):
                    if value.strip():
                        current_weight += weight
                else:
                    current_weight += weight
        
        return int((current_weight / total_weight) * 100)
