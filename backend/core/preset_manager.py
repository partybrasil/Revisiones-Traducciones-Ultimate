"""Preset Manager - Business logic for product preset operations."""
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from models.product_sheet import Preset
import yaml
import os
from pathlib import Path


class PresetManager:
    """Manager for product preset operations."""
    
    def __init__(self, db: Session):
        """Initialize manager with database session."""
        self.db = db
        self.presets_dir = Path(__file__).parent.parent / "presets"
    
    def load_preset(self, family: str) -> Optional[Dict[str, Any]]:
        """
        Load preset for a product family.
        
        Args:
            family: Product family code
            
        Returns:
            Preset data dictionary or None
        """
        # Try to get from database first
        preset = self.db.query(Preset).filter(Preset.family == family).first()
        
        if preset:
            return preset.to_dict()
        
        # Try to load from YAML file
        yaml_file = self.presets_dir / f"{family.lower()}.yaml"
        if yaml_file.exists():
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data
        
        return None
    
    def apply_preset(self, product_data: Dict[str, Any], family: str) -> Dict[str, Any]:
        """
        Apply preset values to product data.
        
        Args:
            product_data: Current product data
            family: Product family code
            
        Returns:
            Product data with preset values applied
        """
        preset = self.load_preset(family)
        
        if not preset:
            return product_data
        
        # Apply preset fields if not already set
        if 'mode_of_use' in preset and not product_data.get('mode_of_use'):
            product_data['mode_of_use'] = preset['mode_of_use']
        
        if 'warnings' in preset and not product_data.get('general_warnings'):
            product_data['general_warnings'] = preset['warnings']
        
        if 'typical_allergens' in preset and not product_data.get('allergens_may_contain'):
            product_data['allergens_may_contain'] = preset['typical_allergens']
        
        if 'typical_pictograms' in preset and not product_data.get('pictograms'):
            product_data['pictograms'] = preset['typical_pictograms']
        
        if 'pao_default' in preset and not product_data.get('pao'):
            product_data['pao'] = preset['pao_default']
        
        # Apply custom fields from fields_to_autofill
        if 'fields_to_autofill' in preset:
            for field, value in preset['fields_to_autofill'].items():
                if not product_data.get(field):
                    product_data[field] = value
        
        return product_data
    
    def get_available_families(self) -> List[str]:
        """
        Get list of available product families.
        
        Returns:
            List of family codes
        """
        # Get from database
        db_families = self.db.query(Preset.family).all()
        families = [f[0] for f in db_families]
        
        # Get from YAML files
        if self.presets_dir.exists():
            for yaml_file in self.presets_dir.glob("*.yaml"):
                family = yaml_file.stem.upper()
                if family not in families:
                    families.append(family)
        
        return sorted(families)
    
    def get_preset_fields(self, family: str) -> Dict[str, Any]:
        """
        Get preset field definitions for a family.
        
        Args:
            family: Product family code
            
        Returns:
            Dictionary of preset fields
        """
        preset = self.load_preset(family)
        
        if not preset:
            return {}
        
        return {
            'mode_of_use': preset.get('mode_of_use', {}),
            'warnings': preset.get('warnings', {}),
            'typical_allergens': preset.get('typical_allergens', []),
            'typical_pictograms': preset.get('typical_pictograms', []),
            'pao_default': preset.get('pao_default'),
            'natural_origin_range': preset.get('natural_origin_range'),
            'fields_to_autofill': preset.get('fields_to_autofill', {}),
        }
    
    def save_preset(self, family: str, preset_data: Dict[str, Any]) -> Preset:
        """
        Save or update a preset in the database.
        
        Args:
            family: Product family code
            preset_data: Preset data dictionary
            
        Returns:
            Saved Preset instance
        """
        # Check if preset exists
        preset = self.db.query(Preset).filter(Preset.family == family).first()
        
        if preset:
            # Update existing
            for key, value in preset_data.items():
                if hasattr(preset, key):
                    setattr(preset, key, value)
        else:
            # Create new
            preset = Preset(
                family=family,
                display_name=preset_data.get('display_name', family),
                mode_of_use=preset_data.get('mode_of_use', {}),
                warnings=preset_data.get('warnings', {}),
                typical_allergens=preset_data.get('typical_allergens', []),
                typical_pictograms=preset_data.get('typical_pictograms', []),
                pao_default=preset_data.get('pao_default'),
                natural_origin_range=preset_data.get('natural_origin_range'),
                fields_to_autofill=preset_data.get('fields_to_autofill', {}),
            )
            self.db.add(preset)
        
        self.db.commit()
        self.db.refresh(preset)
        
        return preset
