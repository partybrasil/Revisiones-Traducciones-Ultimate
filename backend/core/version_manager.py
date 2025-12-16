"""Version Manager - Business logic for version control and snapshots."""
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from models.product_sheet import ProductSheet, ProductVersion, ProductChangelog
from datetime import datetime
import uuid


class VersionManager:
    """Manager for product version control operations."""
    
    def __init__(self, db: Session):
        """Initialize manager with database session."""
        self.db = db
    
    def create_snapshot(
        self,
        sku: str,
        version_type: str = "minor",
        change_summary: str = "",
        created_by: Optional[str] = None,
        old_state: Optional[Dict[str, Any]] = None
    ) -> Optional[ProductVersion]:
        """
        Create a version snapshot of a product sheet.
        
        Args:
            sku: Product SKU
            version_type: Type of version (major, minor, patch)
            change_summary: Summary of changes
            created_by: Username of creator
            old_state: Previous state for diff calculation (optional)
            
        Returns:
            Created ProductVersion instance or None
        """
        # Get current product
        product = self.db.query(ProductSheet).filter(ProductSheet.sku == sku).first()
        if not product:
            return None
        
        # Calculate new version number
        current_version = product.current_version or "1.0"
        new_version = self._calculate_next_version(current_version, version_type)
        
        # Archive previous current version
        self.db.query(ProductVersion).filter(
            ProductVersion.sku == sku,
            ProductVersion.status == "current"
        ).update({"status": "archived"})
        
        # Create complete snapshot
        snapshot_data = product.to_dict()
        
        # Create new version
        version = ProductVersion(
            version_id=uuid.uuid4(),
            sku=sku,
            version_number=new_version,
            version_type=version_type,
            status="current",
            snapshot_date=datetime.utcnow(),
            created_by=created_by,
            change_summary=change_summary,
            complete_snapshot=snapshot_data
        )
        
        self.db.add(version)
        
        # Update product's current version
        product.current_version = new_version
        
        # Create changelog if old state provided
        if old_state:
            changes = self.calculate_diff(old_state, snapshot_data)
            if changes:
                changelog = ProductChangelog(
                    change_id=uuid.uuid4(),
                    sku=sku,
                    version_from=current_version,
                    version_to=new_version,
                    changed_by=created_by,
                    changed_date=datetime.utcnow(),
                    changes_array=changes,
                    change_summary=change_summary
                )
                self.db.add(changelog)
        
        self.db.commit()
        self.db.refresh(version)
        
        return version
    
    def get_snapshot(self, sku: str, version_number: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific version snapshot.
        
        Args:
            sku: Product SKU
            version_number: Version number (e.g., "1.0", "2.1")
            
        Returns:
            Snapshot data or None
        """
        version = self.db.query(ProductVersion).filter(
            ProductVersion.sku == sku,
            ProductVersion.version_number == version_number
        ).first()
        
        if not version:
            return None
        
        return version.to_dict()
    
    def get_versions(self, sku: str) -> List[ProductVersion]:
        """
        Get all versions for a product.
        
        Args:
            sku: Product SKU
            
        Returns:
            List of ProductVersion instances
        """
        versions = self.db.query(ProductVersion).filter(
            ProductVersion.sku == sku
        ).order_by(ProductVersion.snapshot_date.desc()).all()
        
        return versions
    
    def compare_versions(
        self,
        sku: str,
        version_from: str,
        version_to: str
    ) -> Dict[str, Any]:
        """
        Compare two versions and return differences.
        
        Args:
            sku: Product SKU
            version_from: Starting version number
            version_to: Ending version number
            
        Returns:
            Comparison data with changes
        """
        # Get both snapshots
        v_from = self.db.query(ProductVersion).filter(
            ProductVersion.sku == sku,
            ProductVersion.version_number == version_from
        ).first()
        
        v_to = self.db.query(ProductVersion).filter(
            ProductVersion.sku == sku,
            ProductVersion.version_number == version_to
        ).first()
        
        if not v_from or not v_to:
            return {
                "error": "One or both versions not found",
                "version_from": version_from,
                "version_to": version_to
            }
        
        # Calculate differences
        changes = self.calculate_diff(
            v_from.complete_snapshot,
            v_to.complete_snapshot
        )
        
        # Count changes by type
        added = sum(1 for c in changes if c['change_type'] == 'added')
        updated = sum(1 for c in changes if c['change_type'] == 'updated')
        deleted = sum(1 for c in changes if c['change_type'] == 'deleted')
        
        return {
            "sku": sku,
            "version_from": version_from,
            "version_to": version_to,
            "total_changes": len(changes),
            "added": added,
            "updated": updated,
            "deleted": deleted,
            "changes": changes,
            "from_date": v_from.snapshot_date.isoformat(),
            "to_date": v_to.snapshot_date.isoformat(),
        }
    
    def restore_version(self, sku: str, version_number: str, restored_by: Optional[str] = None) -> Optional[ProductSheet]:
        """
        Restore a product to a previous version.
        
        Args:
            sku: Product SKU
            version_number: Version to restore to
            restored_by: Username of restorer
            
        Returns:
            Updated ProductSheet or None
        """
        # Get the version to restore
        version = self.db.query(ProductVersion).filter(
            ProductVersion.sku == sku,
            ProductVersion.version_number == version_number
        ).first()
        
        if not version:
            return None
        
        # Get current product
        product = self.db.query(ProductSheet).filter(ProductSheet.sku == sku).first()
        if not product:
            return None
        
        # Save current state for changelog
        old_state = product.to_dict()
        
        # Restore data from snapshot (excluding metadata)
        snapshot = version.complete_snapshot
        for key, value in snapshot.items():
            if key not in ['created_date', 'created_by', 'current_version'] and hasattr(product, key):
                setattr(product, key, value)
        
        product.updated_by = restored_by
        product.updated_date = datetime.utcnow()
        
        # Create new snapshot for the restoration
        new_version = self._calculate_next_version(product.current_version, "major")
        self.create_snapshot(
            sku=sku,
            version_type="major",
            change_summary=f"Restored to version {version_number}",
            created_by=restored_by,
            old_state=old_state
        )
        
        self.db.commit()
        self.db.refresh(product)
        
        return product
    
    def get_changelog(self, sku: str, limit: int = 50) -> List[ProductChangelog]:
        """
        Get changelog history for a product.
        
        Args:
            sku: Product SKU
            limit: Maximum number of changelog entries
            
        Returns:
            List of ProductChangelog instances
        """
        changelog = self.db.query(ProductChangelog).filter(
            ProductChangelog.sku == sku
        ).order_by(ProductChangelog.changed_date.desc()).limit(limit).all()
        
        return changelog
    
    def calculate_diff(self, old_state: Dict[str, Any], new_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Calculate field-level differences between two states.
        
        Args:
            old_state: Previous state dictionary
            new_state: New state dictionary
            
        Returns:
            List of changes with field paths and values
        """
        changes = []
        
        # Flatten both dictionaries for comparison
        old_flat = self._flatten_dict(old_state)
        new_flat = self._flatten_dict(new_state)
        
        # Find all unique keys
        all_keys = set(old_flat.keys()) | set(new_flat.keys())
        
        for key in all_keys:
            old_value = old_flat.get(key)
            new_value = new_flat.get(key)
            
            # Skip if values are identical
            if old_value == new_value:
                continue
            
            # Determine change type
            if old_value is None and new_value is not None:
                change_type = "added"
                severity = "important" if self._is_critical_field(key) else "minor"
            elif old_value is not None and new_value is None:
                change_type = "deleted"
                severity = "important"
            else:
                change_type = "updated"
                severity = "critical" if self._is_critical_field(key) else "minor"
            
            changes.append({
                "field_path": key,
                "field_display_name": self._format_field_name(key),
                "old_value": old_value,
                "new_value": new_value,
                "change_type": change_type,
                "severity": severity
            })
        
        # Sort by severity (critical > important > minor) then by field name
        severity_order = {"critical": 0, "important": 1, "minor": 2}
        changes.sort(key=lambda x: (severity_order.get(x["severity"], 3), x["field_path"]))
        
        return changes
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """
        Flatten a nested dictionary.
        
        Args:
            d: Dictionary to flatten
            parent_key: Parent key prefix
            sep: Separator for keys
            
        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict) and v:
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list) and v:
                # Convert list to string representation for comparison
                items.append((new_key, str(v)))
            else:
                items.append((new_key, v))
        
        return dict(items)
    
    def _calculate_next_version(self, current: str, version_type: str) -> str:
        """
        Calculate next version number.
        
        Args:
            current: Current version string (e.g., "1.0")
            version_type: Type of version bump (major, minor, patch)
            
        Returns:
            Next version string
        """
        parts = current.split('.')
        
        # Ensure we have at least major.minor
        while len(parts) < 2:
            parts.append('0')
        
        major = int(parts[0])
        minor = int(parts[1])
        patch = int(parts[2]) if len(parts) > 2 else 0
        
        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        elif version_type == "patch":
            patch += 1
        
        if patch > 0:
            return f"{major}.{minor}.{patch}"
        else:
            return f"{major}.{minor}"
    
    def _is_critical_field(self, field_path: str) -> bool:
        """
        Determine if a field is critical for compliance.
        
        Args:
            field_path: Flattened field path
            
        Returns:
            True if field is critical
        """
        critical_fields = [
            'title_short',
            'inci_ingredients',
            'allergens_present',
            'mode_of_use',
            'general_warnings',
            'made_in',
            'distributor',
            'responsible_person',
            'pao',
        ]
        
        return any(cf in field_path for cf in critical_fields)
    
    def _format_field_name(self, field_path: str) -> str:
        """
        Format field path to human-readable name.
        
        Args:
            field_path: Flattened field path
            
        Returns:
            Formatted field name
        """
        # Replace underscores with spaces and capitalize
        return field_path.replace('_', ' ').replace('.', ' > ').title()
