"""Database initialization script."""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from database import Base, engine, SessionLocal
from models.product_sheet import ProductSheet, Preset
from core.preset_manager import PresetManager
import yaml


def init_database():
    """Initialize database tables."""
    print("🔧 Initializing database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully")


def load_presets():
    """Load preset data from YAML files into database."""
    print("📦 Loading presets...")
    
    db = SessionLocal()
    manager = PresetManager(db)
    
    presets_dir = Path(__file__).parent / "presets"
    count = 0
    
    for yaml_file in presets_dir.glob("*.yaml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
                if 'family' in data:
                    manager.save_preset(data['family'], data)
                    print(f"  ✓ Loaded preset: {data.get('display_name', data['family'])}")
                    count += 1
        except Exception as e:
            print(f"  ✗ Error loading {yaml_file.name}: {e}")
    
    db.close()
    print(f"✅ Loaded {count} presets")


def create_sample_product():
    """Create a sample product for testing."""
    print("📝 Creating sample product...")
    
    db = SessionLocal()
    
    # Check if sample already exists
    existing = db.query(ProductSheet).filter(ProductSheet.sku == "CF-HYD-001").first()
    if existing:
        print("  ⚠ Sample product already exists, skipping")
        db.close()
        return
    
    # Create sample product
    sample = ProductSheet(
        sku="CF-HYD-001",
        ean_list=["5412345678901"],
        brand="Cosmetics Brand Example",
        family="COSMETICS_FACIAL",
        title_short={
            "es": "Crema Hidratante Facial",
            "pt": "Creme Hidratante Facial",
            "it": "Crema Idratante Viso",
            "en": "Facial Moisturizing Cream"
        },
        description_detailed={
            "es": "Crema hidratante facial de absorción rápida con ácido hialurónico y vitamina E. Proporciona hidratación profunda durante 24 horas.",
            "pt": "Creme hidratante facial de absorção rápida com ácido hialurónico e vitamina E. Proporciona hidratação profunda durante 24 horas.",
            "it": "Crema idratante viso ad assorbimento rapido con acido ialuronico e vitamina E. Fornisce idratazione profonda per 24 ore.",
            "en": "Fast-absorbing facial moisturizer with hyaluronic acid and vitamin E. Provides deep hydration for 24 hours."
        },
        made_in={
            "country_code": "FR",
            "made_in_text": {
                "es": "Fabricado en Francia",
                "pt": "Fabricado em França",
                "it": "Fabbricato in Francia",
                "en": "Made in France"
            }
        },
        distributor={
            "company_name": "Cosmetics Distributor S.L.",
            "cif": "B12345678",
            "addresses": {
                "es": "Calle Example 123, 28001 Madrid, España",
                "pt": "Rua Example 123, 1000-001 Lisboa, Portugal"
            }
        },
        net_weight_value=50,
        net_weight_unit="ml",
        format_type="Tarro",
        format_material="Plástico",
        format_closure="Rosca",
        packaging_languages=["ES", "PT", "IT", "EN"],
        pao="12M",
        inci_ingredients="Aqua, Glycerin, Sodium Hyaluronate, Tocopherol, Cetearyl Alcohol, Glyceryl Stearate",
        allergens_present=["Linalool", "Limonene"],
        mode_of_use={
            "es": "Aplicar una cantidad adecuada sobre el rostro limpio y seco. Masajear suavemente hasta su completa absorción.",
            "pt": "Aplicar quantidade adequada sobre o rosto limpo e seco. Massajar suavemente até completa absorção.",
            "it": "Applicare una quantità adeguata sul viso pulito e asciutto. Massaggiare delicatamente fino al completo assorbimento.",
            "en": "Apply an adequate amount on clean and dry face. Massage gently until fully absorbed."
        },
        general_warnings={
            "es": "Solo para uso externo. Evitar el contacto con los ojos. Mantener fuera del alcance de los niños.",
            "pt": "Apenas para uso externo. Evitar contacto com os olhos. Manter fora do alcance das crianças.",
            "it": "Solo per uso esterno. Evitare il contatto con gli occhi. Tenere fuori dalla portata dei bambini.",
            "en": "For external use only. Avoid contact with eyes. Keep out of reach of children."
        },
        current_version="1.0",
        status="approved",
        created_by="admin",
        updated_by="admin"
    )
    
    db.add(sample)
    db.commit()
    db.close()
    
    print("✅ Sample product created: CF-HYD-001")


def main():
    """Main initialization function."""
    print("\n" + "="*60)
    print("  Database Initialization - Revisiones-Traducciones-Ultimate")
    print("="*60 + "\n")
    
    try:
        init_database()
        load_presets()
        create_sample_product()
        
        print("\n" + "="*60)
        print("  ✅ Initialization completed successfully!")
        print("="*60 + "\n")
        
        print("Next steps:")
        print("  1. Start the server: python launcher.py")
        print("  2. Access API docs: http://localhost:8000/docs")
        print("  3. Test with sample product: GET /api/products/CF-HYD-001")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
