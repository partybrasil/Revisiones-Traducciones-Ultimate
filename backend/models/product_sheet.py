"""SQLAlchemy models for product sheets."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON, Index
import uuid
from backend.database import Base


def generate_uuid():
    """Generate UUID string for primary keys."""
    return str(uuid.uuid4())


class ProductSheet(Base):
    """Product sheet model with all product information."""
    
    __tablename__ = "products"
    
    # Primary Key
    sku = Column(String(50), primary_key=True, unique=True, nullable=False, index=True)
    
    # General Information
    ean_list = Column(JSON, default=list)  # Array of up to 20 EANs
    internal_reference = Column(String(100))
    supplier_code = Column(String(100))
    brand = Column(String(200))
    gama = Column(JSON, default=dict)  # {es, pt, it, en, fr, br}
    family = Column(String(100), nullable=False, index=True)  # COSMETICS_FACIAL, etc.
    subfamily = Column(String(100))
    
    # Multilingual Titles and Descriptions
    title_short = Column(JSON, default=dict)  # {es, pt, it, en, fr, br}
    description_detailed = Column(JSON, default=dict)  # {es, pt, it, en, fr, br}
    
    # Regulatory Metadata
    made_in = Column(JSON, default=dict)  # {country_code, made_in_text{es,pt,it,en,br}}
    distributor = Column(JSON, default=dict)  # {company_name, cif, addresses, distributor_text}
    responsible_person = Column(JSON, default=dict)  # {name, email, phone, company, address, rp_declaration}
    natural_origin_percentage = Column(JSON, default=dict)  # {value, certified, certification_name}
    
    # Physical Properties
    net_weight_value = Column(Float)
    net_weight_unit = Column(String(10))  # g, ml, kg, L
    gross_weight_value = Column(Float)
    gross_weight_unit = Column(String(10))
    height_cm = Column(Float)
    width_cm = Column(Float)
    depth_cm = Column(Float)
    
    # Format and Packaging
    format_type = Column(String(50))  # Botella, Tubo, Tarro, Caja
    format_material = Column(String(50))  # Plástico, Vidrio, Aluminio
    format_closure = Column(String(50))  # Rosca, Tapa presión
    packaging_languages = Column(JSON, default=list)  # [ES, PT, IT, EN]
    
    # Label Positions (6 positions with multilingual content)
    label_positions = Column(JSON, default=dict)  # {frontal, trasera, lateral_izq, lateral_dcha, superior, inferior}
    
    # Pictograms and PAO
    pictograms = Column(JSON, default=list)  # Array of pictogram IDs
    pao = Column(String(10))  # 6M, 12M, 18M, 24M, 36M
    
    # Composition
    inci_ingredients = Column(Text)  # Full INCI list
    key_ingredients = Column(JSON, default=list)  # Top 5 ingredients
    allergens_present = Column(JSON, default=list)
    allergens_may_contain = Column(JSON, default=list)
    allergens_free_from = Column(JSON, default=list)
    
    # Mode of Use
    mode_of_use = Column(JSON, default=dict)  # {es, pt, it}
    application_frequency = Column(String(100))
    application_area = Column(String(200))
    
    # Warnings and Precautions
    general_warnings = Column(JSON, default=dict)  # {es, pt, it}
    specific_warnings = Column(JSON, default=dict)  # {pregnancy, lactation, children}
    storage_conditions = Column(JSON, default=dict)  # {es, pt, it}
    storage_temperature_min = Column(Integer)
    storage_temperature_max = Column(Integer)
    
    # Marketing
    key_benefits = Column(JSON, default=dict)  # {es, pt, it}
    marketing_claims = Column(JSON, default=dict)  # {es, pt, it}
    validated_claims = Column(Boolean, default=False)
    scientific_backing = Column(JSON, default=list)  # Array of URLs
    
    # Certifications
    certifications = Column(JSON, default=list)  # [{name, number, expiry_date}]
    
    # Images
    product_images = Column(JSON, default=list)  # [{type, url, source, resolution}]
    
    # Version Control
    current_version = Column(String(20), default="1.0")
    
    # Status and Completion
    status = Column(String(20), default="draft", index=True)  # draft, in_review, approved, published
    completion_percentage = Column(Integer, default=0)
    
    # Audit Fields
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(String(100))
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(String(100))
    
    # Indexes
    __table_args__ = (
        Index('idx_products_created_date', 'created_date'),
        Index('idx_products_family_status', 'family', 'status'),
    )
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'sku': self.sku,
            'ean_list': self.ean_list,
            'internal_reference': self.internal_reference,
            'supplier_code': self.supplier_code,
            'brand': self.brand,
            'gama': self.gama,
            'family': self.family,
            'subfamily': self.subfamily,
            'title_short': self.title_short,
            'description_detailed': self.description_detailed,
            'made_in': self.made_in,
            'distributor': self.distributor,
            'responsible_person': self.responsible_person,
            'natural_origin_percentage': self.natural_origin_percentage,
            'net_weight_value': self.net_weight_value,
            'net_weight_unit': self.net_weight_unit,
            'gross_weight_value': self.gross_weight_value,
            'gross_weight_unit': self.gross_weight_unit,
            'height_cm': self.height_cm,
            'width_cm': self.width_cm,
            'depth_cm': self.depth_cm,
            'format_type': self.format_type,
            'format_material': self.format_material,
            'format_closure': self.format_closure,
            'packaging_languages': self.packaging_languages,
            'label_positions': self.label_positions,
            'pictograms': self.pictograms,
            'pao': self.pao,
            'inci_ingredients': self.inci_ingredients,
            'key_ingredients': self.key_ingredients,
            'allergens_present': self.allergens_present,
            'allergens_may_contain': self.allergens_may_contain,
            'allergens_free_from': self.allergens_free_from,
            'mode_of_use': self.mode_of_use,
            'application_frequency': self.application_frequency,
            'application_area': self.application_area,
            'general_warnings': self.general_warnings,
            'specific_warnings': self.specific_warnings,
            'storage_conditions': self.storage_conditions,
            'storage_temperature_min': self.storage_temperature_min,
            'storage_temperature_max': self.storage_temperature_max,
            'key_benefits': self.key_benefits,
            'marketing_claims': self.marketing_claims,
            'validated_claims': self.validated_claims,
            'scientific_backing': self.scientific_backing,
            'certifications': self.certifications,
            'product_images': self.product_images,
            'current_version': self.current_version,
            'status': self.status,
            'completion_percentage': self.completion_percentage,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'created_by': self.created_by,
            'updated_date': self.updated_date.isoformat() if self.updated_date else None,
            'updated_by': self.updated_by,
        }


class ProductVersion(Base):
    """Version history for product sheets."""
    
    __tablename__ = "product_versions"
    
    version_id = Column(String(36), primary_key=True, default=generate_uuid)
    sku = Column(String(50), nullable=False, index=True)
    version_number = Column(String(20), nullable=False)
    version_type = Column(String(10), nullable=False)  # major, minor, patch
    status = Column(String(20), default="current")  # current, archived
    snapshot_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(String(100))
    change_summary = Column(Text)
    complete_snapshot = Column(JSON, nullable=False)  # Complete state of product at this version
    
    __table_args__ = (
        Index('idx_versions_sku_number', 'sku', 'version_number'),
        Index('idx_versions_sku_date', 'sku', 'snapshot_date'),
    )
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'version_id': str(self.version_id),
            'sku': self.sku,
            'version_number': self.version_number,
            'version_type': self.version_type,
            'status': self.status,
            'snapshot_date': self.snapshot_date.isoformat() if self.snapshot_date else None,
            'created_by': self.created_by,
            'change_summary': self.change_summary,
            'complete_snapshot': self.complete_snapshot,
        }


class ProductChangelog(Base):
    """Detailed changelog for product modifications."""
    
    __tablename__ = "product_changelog"
    
    change_id = Column(String(36), primary_key=True, default=generate_uuid)
    sku = Column(String(50), nullable=False, index=True)
    version_from = Column(String(20))
    version_to = Column(String(20), nullable=False)
    changed_by = Column(String(100))
    changed_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    changes_array = Column(JSON, nullable=False)  # Array of field-level changes
    change_summary = Column(Text)
    
    __table_args__ = (
        Index('idx_changelog_sku_date', 'sku', 'changed_date'),
        Index('idx_changelog_changed_by', 'changed_by', 'changed_date'),
    )
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'change_id': str(self.change_id),
            'sku': self.sku,
            'version_from': self.version_from,
            'version_to': self.version_to,
            'changed_by': self.changed_by,
            'changed_date': self.changed_date.isoformat() if self.changed_date else None,
            'changes_array': self.changes_array,
            'change_summary': self.change_summary,
        }


class LegalRule(Base):
    """Legal compliance rules by country and product family."""
    
    __tablename__ = "legal_rules"
    
    rule_id = Column(String(36), primary_key=True, default=generate_uuid)
    country = Column(String(2), nullable=False)  # PT, IT, ES
    family = Column(String(100), nullable=False)
    requirement_type = Column(String(20), nullable=False)  # critical, optional
    field_name = Column(String(100), nullable=False)
    field_description = Column(Text)
    translation_mandatory = Column(Boolean, default=False)
    error_message = Column(Text)
    rule_data = Column(JSON, default=dict)
    
    __table_args__ = (
        Index('idx_legal_country_family', 'country', 'family'),
    )
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'rule_id': str(self.rule_id),
            'country': self.country,
            'family': self.family,
            'requirement_type': self.requirement_type,
            'field_name': self.field_name,
            'field_description': self.field_description,
            'translation_mandatory': self.translation_mandatory,
            'error_message': self.error_message,
            'rule_data': self.rule_data,
        }


class Preset(Base):
    """Preset values for product families."""
    
    __tablename__ = "presets"
    
    preset_id = Column(String(36), primary_key=True, default=generate_uuid)
    family = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200))
    mode_of_use = Column(JSON, default=dict)  # {es, pt, it, en, fr, br}
    warnings = Column(JSON, default=dict)  # {es, pt, it, en, fr, br}
    typical_allergens = Column(JSON, default=list)
    typical_pictograms = Column(JSON, default=list)
    pao_default = Column(String(10))
    natural_origin_range = Column(String(50))
    fields_to_autofill = Column(JSON, default=dict)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'preset_id': str(self.preset_id),
            'family': self.family,
            'display_name': self.display_name,
            'mode_of_use': self.mode_of_use,
            'warnings': self.warnings,
            'typical_allergens': self.typical_allergens,
            'typical_pictograms': self.typical_pictograms,
            'pao_default': self.pao_default,
            'natural_origin_range': self.natural_origin_range,
            'fields_to_autofill': self.fields_to_autofill,
        }
