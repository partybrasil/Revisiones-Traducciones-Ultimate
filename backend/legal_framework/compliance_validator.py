"""Compliance Validator - Validates products against legal requirements."""
from typing import Dict, List, Any, Optional
import yaml
from pathlib import Path


class ComplianceValidator:
    """Validator for legal compliance of product sheets."""
    
    def __init__(self):
        """Initialize validator and load legal rules."""
        self.rules_dir = Path(__file__).parent
        self.rules = {}
        self._load_all_rules()
    
    def _load_all_rules(self):
        """Load all legal framework YAML files."""
        for rules_file in self.rules_dir.glob("*_rules.yaml"):
            country_code = rules_file.stem.split('_')[0].upper()
            try:
                with open(rules_file, 'r', encoding='utf-8') as f:
                    self.rules[country_code] = yaml.safe_load(f)
            except Exception as e:
                print(f"Error loading {rules_file}: {e}")
    
    def validate_for_country(
        self,
        product_data: Dict[str, Any],
        country: str
    ) -> Dict[str, Any]:
        """
        Validate product against country-specific requirements.
        
        Args:
            product_data: Product data dictionary
            country: Country code (PT, IT, ES)
            
        Returns:
            Validation result with status, percentage, issues, warnings
        """
        country_upper = country.upper()
        
        if country_upper not in self.rules:
            return {
                "status": "ERROR",
                "message": f"No rules found for country: {country}",
                "percentage": 0,
                "critical_issues": [],
                "warnings": []
            }
        
        country_rules = self.rules[country_upper]
        family = product_data.get('family', '').lower()
        
        # Get family-specific rules
        if family not in country_rules:
            # Try to find the closest match
            available_families = [k for k in country_rules.keys() if k not in ['country', 'code', 'authority', 'authority_url']]
            if available_families:
                family = available_families[0]  # Use first available
            else:
                return {
                    "status": "ERROR",
                    "message": f"No rules found for family: {product_data.get('family')}",
                    "percentage": 0,
                    "critical_issues": [],
                    "warnings": []
                }
        
        family_rules = country_rules[family]
        
        # Validate critical requirements
        critical_issues = []
        critical_requirements = family_rules.get('critical_requirements', [])
        
        for requirement in critical_requirements:
            field = requirement['field']
            translation_mandatory = requirement.get('translation_mandatory', False)
            
            # Check if field exists and has value
            if not self._validate_field(product_data, field, translation_mandatory):
                critical_issues.append({
                    "field": field,
                    "name": requirement['name'],
                    "tag": requirement['tag'],
                    "error_message": requirement['error_message'],
                    "description": requirement.get('description', ''),
                    "example": requirement.get('example', '')
                })
        
        # Validate optional requirements (warnings)
        warnings = []
        optional_requirements = family_rules.get('optional_requirements', [])
        
        for requirement in optional_requirements:
            field = requirement['field']
            
            if not self._validate_field(product_data, field, False):
                warnings.append({
                    "field": field,
                    "name": requirement['name'],
                    "tag": requirement['tag'],
                    "description": requirement.get('description', '')
                })
        
        # Calculate compliance percentage
        total_requirements = len(critical_requirements)
        met_requirements = total_requirements - len(critical_issues)
        percentage = int((met_requirements / total_requirements) * 100) if total_requirements > 0 else 0
        
        # Determine status
        if len(critical_issues) == 0:
            status = "COMPLIANT"
        elif len(critical_issues) <= 2:
            status = "WARNING"
        else:
            status = "NON_COMPLIANT"
        
        return {
            "status": status,
            "country": country_upper,
            "family": family,
            "authority": country_rules.get('authority', ''),
            "percentage": percentage,
            "total_requirements": total_requirements,
            "met_requirements": met_requirements,
            "critical_issues": critical_issues,
            "warnings": warnings,
            "regulations": family_rules.get('regulations', [])
        }
    
    def _validate_field(
        self,
        product_data: Dict[str, Any],
        field_path: str,
        translation_mandatory: bool
    ) -> bool:
        """
        Validate if a field exists and has value.
        
        Args:
            product_data: Product data dictionary
            field_path: Field path (e.g., "title_short.pt")
            translation_mandatory: Whether translation is mandatory
            
        Returns:
            True if field is valid, False otherwise
        """
        # Split nested field path
        parts = field_path.split('.')
        
        # Navigate through nested structure
        current = product_data
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return False
            
            if current is None:
                return False
        
        # Check if value is not empty
        if isinstance(current, str):
            return bool(current.strip())
        elif isinstance(current, (list, dict)):
            return len(current) > 0
        elif isinstance(current, (int, float)):
            return True
        elif isinstance(current, bool):
            return True
        
        return current is not None
    
    def get_country_rules(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Get all rules for a country.
        
        Args:
            country: Country code (PT, IT, ES)
            
        Returns:
            Country rules dictionary or None
        """
        return self.rules.get(country.upper())
    
    def get_family_requirements(
        self,
        country: str,
        family: str
    ) -> Dict[str, Any]:
        """
        Get requirements for a specific family in a country.
        
        Args:
            country: Country code
            family: Product family
            
        Returns:
            Family requirements dictionary
        """
        country_rules = self.rules.get(country.upper(), {})
        return country_rules.get(family.lower(), {})
    
    def get_available_countries(self) -> List[str]:
        """
        Get list of available countries.
        
        Returns:
            List of country codes
        """
        return list(self.rules.keys())
    
    def validate_multiple_countries(
        self,
        product_data: Dict[str, Any],
        countries: List[str]
    ) -> Dict[str, Any]:
        """
        Validate product against multiple countries.
        
        Args:
            product_data: Product data dictionary
            countries: List of country codes
            
        Returns:
            Dictionary with validation results for each country
        """
        results = {}
        
        for country in countries:
            results[country] = self.validate_for_country(product_data, country)
        
        # Calculate overall status
        all_compliant = all(r['status'] == 'COMPLIANT' for r in results.values())
        any_critical = any(r['status'] == 'NON_COMPLIANT' for r in results.values())
        
        if all_compliant:
            overall_status = "COMPLIANT"
        elif any_critical:
            overall_status = "NON_COMPLIANT"
        else:
            overall_status = "WARNING"
        
        return {
            "overall_status": overall_status,
            "countries": results,
            "total_countries": len(countries),
            "compliant_countries": sum(1 for r in results.values() if r['status'] == 'COMPLIANT')
        }
