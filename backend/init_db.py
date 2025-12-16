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


def create_sample_products():
    """Create multiple sample products for testing."""
    print("📝 Creating sample products...")
    
    db = SessionLocal()
    
    # Define sample products with varied data
    sample_products = [
        # 1. Cosmetics - Facial Cream
        ProductSheet(
            sku="CF-HYD-001",
            ean_list=["5412345678901", "5412345678902"],
            brand="Cosmetics Brand Example",
            family="COSMETICS_FACIAL",
            title_short={
                "es": "Crema Hidratante Facial",
                "pt": "Creme Hidratante Facial",
                "it": "Crema Idratante Viso",
                "en": "Facial Moisturizing Cream",
                "fr": "Crème Hydratante Visage"
            },
            description_detailed={
                "es": "Crema hidratante facial de absorción rápida con ácido hialurónico y vitamina E. Proporciona hidratación profunda durante 24 horas.",
                "pt": "Creme hidratante facial de absorção rápida com ácido hialurónico e vitamina E. Proporciona hidratação profunda durante 24 horas.",
                "it": "Crema idratante viso ad assorbimento rapido con acido ialuronico e vitamina E. Fornisce idratazione profonda per 24 ore.",
                "en": "Fast-absorbing facial moisturizer with hyaluronic acid and vitamin E. Provides deep hydration for 24 hours.",
                "fr": "Crème hydratante visage à absorption rapide avec acide hyaluronique et vitamine E. Offre une hydratation profonde pendant 24 heures."
            },
            made_in={
                "country_code": "FR",
                "made_in_text": {
                    "es": "Fabricado en Francia",
                    "pt": "Fabricado em França",
                    "it": "Fabbricato in Francia",
                    "en": "Made in France",
                    "fr": "Fabriqué en France"
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
            packaging_languages=["ES", "PT", "IT", "EN", "FR"],
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
        ),
        
        # 2. Cosmetics - Anti-Aging Serum
        ProductSheet(
            sku="CS-AGE-002",
            ean_list=["5423456789012"],
            brand="Premium Beauty Lab",
            family="COSMETICS_FACIAL",
            title_short={
                "es": "Sérum Anti-Edad Intensivo",
                "pt": "Sérum Anti-Idade Intensivo",
                "it": "Siero Anti-Età Intensivo",
                "en": "Intensive Anti-Aging Serum"
            },
            description_detailed={
                "es": "Sérum concentrado con retinol y péptidos que reduce las arrugas y líneas de expresión. Resultados visibles en 4 semanas.",
                "pt": "Sérum concentrado com retinol e péptidos que reduz as rugas e linhas de expressão. Resultados visíveis em 4 semanas.",
                "it": "Siero concentrato con retinolo e peptidi che riduce le rughe e le linee di espressione. Risultati visibili in 4 settimane.",
                "en": "Concentrated serum with retinol and peptides that reduces wrinkles and expression lines. Visible results in 4 weeks."
            },
            made_in={
                "country_code": "DE",
                "made_in_text": {
                    "es": "Fabricado en Alemania",
                    "pt": "Fabricado na Alemanha",
                    "it": "Fabbricato in Germania",
                    "en": "Made in Germany"
                }
            },
            distributor={
                "company_name": "Beauty Distribution Europe Ltd.",
                "cif": "B98765432",
                "addresses": {
                    "es": "Avenida Principal 456, 08080 Barcelona, España",
                    "pt": "Avenida Central 456, 4000-100 Porto, Portugal"
                }
            },
            net_weight_value=30,
            net_weight_unit="ml",
            format_type="Botella",
            format_material="Vidrio",
            format_closure="Gotero",
            packaging_languages=["ES", "PT", "IT", "EN"],
            pao="6M",
            inci_ingredients="Aqua, Retinol, Palmitoyl Pentapeptide-4, Hyaluronic Acid, Glycerin, Phenoxyethanol",
            allergens_present=["Phenoxyethanol"],
            mode_of_use={
                "es": "Aplicar 3-4 gotas por la noche sobre el rostro limpio. Evitar el contorno de ojos.",
                "pt": "Aplicar 3-4 gotas à noite sobre o rosto limpo. Evitar o contorno dos olhos.",
                "it": "Applicare 3-4 gocce la sera sul viso pulito. Evitare il contorno occhi.",
                "en": "Apply 3-4 drops at night on clean face. Avoid eye contour."
            },
            general_warnings={
                "es": "No usar durante el embarazo. Utilizar protección solar durante el día. Solo para uso externo.",
                "pt": "Não usar durante a gravidez. Utilizar proteção solar durante o dia. Apenas para uso externo.",
                "it": "Non usare durante la gravidanza. Utilizzare protezione solare durante il giorno. Solo per uso esterno.",
                "en": "Do not use during pregnancy. Use sun protection during the day. For external use only."
            },
            current_version="1.0",
            status="in_review",
            created_by="admin",
            updated_by="admin"
        ),
        
        # 3. Food - Organic Pasta
        ProductSheet(
            sku="FP-ORG-003",
            ean_list=["8901234567890", "8901234567891"],
            brand="Organic Foods Italia",
            family="FOOD_PACKAGED",
            title_short={
                "es": "Pasta Orgánica de Trigo Integral",
                "pt": "Massa Orgânica de Trigo Integral",
                "it": "Pasta Biologica Integrale",
                "en": "Organic Whole Wheat Pasta"
            },
            description_detailed={
                "es": "Pasta elaborada con trigo integral 100% orgánico certificado. Rica en fibra y nutrientes. Tiempo de cocción: 9-11 minutos.",
                "pt": "Massa elaborada com trigo integral 100% orgânico certificado. Rica em fibra e nutrientes. Tempo de cozimento: 9-11 minutos.",
                "it": "Pasta realizzata con grano integrale 100% biologico certificato. Ricca di fibre e nutrienti. Tempo di cottura: 9-11 minuti.",
                "en": "Pasta made with 100% certified organic whole wheat. Rich in fiber and nutrients. Cooking time: 9-11 minutes."
            },
            made_in={
                "country_code": "IT",
                "made_in_text": {
                    "es": "Fabricado en Italia",
                    "pt": "Fabricado em Itália",
                    "it": "Prodotto in Italia",
                    "en": "Made in Italy"
                }
            },
            distributor={
                "company_name": "Alimentos Naturales S.A.",
                "cif": "A11223344",
                "addresses": {
                    "es": "Polígono Industrial 789, 28050 Madrid, España",
                    "pt": "Zona Industrial 789, 2500-200 Caldas da Rainha, Portugal"
                }
            },
            net_weight_value=500,
            net_weight_unit="g",
            format_type="Paquete",
            format_material="Cartón",
            format_closure="Sellado",
            packaging_languages=["ES", "PT", "IT", "EN"],
            allergens_present=["Gluten (Trigo)"],
            allergens_may_contain=["Huevo"],
            mode_of_use={
                "es": "Cocer en abundante agua hirviendo con sal durante 9-11 minutos. Escurrir y servir al gusto.",
                "pt": "Cozer em água abundante a ferver com sal durante 9-11 minutos. Escorrer e servir a gosto.",
                "it": "Cuocere in abbondante acqua bollente salata per 9-11 minuti. Scolare e servire a piacere.",
                "en": "Cook in plenty of boiling salted water for 9-11 minutes. Drain and serve as desired."
            },
            storage_conditions={
                "es": "Conservar en lugar fresco y seco. Una vez abierto, conservar en recipiente hermético.",
                "pt": "Conservar em local fresco e seco. Após aberto, conservar em recipiente hermético.",
                "it": "Conservare in luogo fresco e asciutto. Dopo l'apertura, conservare in contenitore ermetico.",
                "en": "Store in a cool, dry place. Once opened, store in airtight container."
            },
            current_version="1.0",
            status="approved",
            created_by="admin",
            updated_by="admin"
        ),
        
        # 4. Food Supplement - Vitamin C
        ProductSheet(
            sku="FS-VIT-004",
            ean_list=["7890123456789"],
            brand="Health Plus Nutrition",
            family="FOOD_SUPPLEMENTS",
            title_short={
                "es": "Vitamina C 1000mg - 60 Cápsulas",
                "pt": "Vitamina C 1000mg - 60 Cápsulas",
                "it": "Vitamina C 1000mg - 60 Capsule",
                "en": "Vitamin C 1000mg - 60 Capsules"
            },
            description_detailed={
                "es": "Suplemento de vitamina C de alta potencia que contribuye al funcionamiento normal del sistema inmunitario y a la protección de las células frente al daño oxidativo.",
                "pt": "Suplemento de vitamina C de alta potência que contribui para o normal funcionamento do sistema imunitário e para a proteção das células contra danos oxidativos.",
                "it": "Integratore di vitamina C ad alta potenza che contribuisce al normale funzionamento del sistema immunitario e alla protezione delle cellule dallo stress ossidativo.",
                "en": "High-potency vitamin C supplement that contributes to the normal function of the immune system and to the protection of cells from oxidative damage."
            },
            made_in={
                "country_code": "ES",
                "made_in_text": {
                    "es": "Fabricado en España",
                    "pt": "Fabricado em Espanha",
                    "it": "Fabbricato in Spagna",
                    "en": "Made in Spain"
                }
            },
            distributor={
                "company_name": "Suplementos Health S.L.",
                "cif": "B55667788",
                "addresses": {
                    "es": "Calle Nutrición 321, 46001 Valencia, España",
                    "pt": "Rua Saúde 321, 1100-200 Lisboa, Portugal"
                }
            },
            net_weight_value=60,
            net_weight_unit="caps",
            format_type="Frasco",
            format_material="Plástico HDPE",
            format_closure="Tapa rosca",
            packaging_languages=["ES", "PT", "IT", "EN"],
            allergens_free_from=["Gluten", "Lactosa", "Soja"],
            mode_of_use={
                "es": "Tomar 1 cápsula al día con un vaso de agua, preferiblemente con las comidas.",
                "pt": "Tomar 1 cápsula por dia com um copo de água, de preferência com as refeições.",
                "it": "Assumere 1 capsula al giorno con un bicchiere d'acqua, preferibilmente durante i pasti.",
                "en": "Take 1 capsule daily with a glass of water, preferably with meals."
            },
            general_warnings={
                "es": "Los complementos alimenticios no deben utilizarse como sustitutos de una dieta variada y equilibrada. No superar la dosis diaria recomendada. Mantener fuera del alcance de los niños.",
                "pt": "Os suplementos alimentares não devem ser utilizados como substitutos de um regime alimentar variado e equilibrado. Não exceder a dose diária recomendada. Manter fora do alcance das crianças.",
                "it": "Gli integratori alimentari non vanno intesi come sostituti di una dieta variata ed equilibrata. Non superare la dose giornaliera raccomandata. Tenere fuori dalla portata dei bambini.",
                "en": "Food supplements should not be used as a substitute for a varied and balanced diet. Do not exceed the recommended daily dose. Keep out of reach of children."
            },
            storage_conditions={
                "es": "Conservar en lugar fresco, seco y protegido de la luz.",
                "pt": "Conservar em local fresco, seco e protegido da luz.",
                "it": "Conservare in luogo fresco, asciutto e al riparo dalla luce.",
                "en": "Store in a cool, dry place away from light."
            },
            current_version="1.0",
            status="draft",
            created_by="admin",
            updated_by="admin"
        ),
        
        # 5. Cosmetics - Body Lotion
        ProductSheet(
            sku="CB-LOT-005",
            ean_list=["6789012345678"],
            brand="Natural Body Care",
            family="COSMETICS_BODY",
            title_short={
                "es": "Loción Corporal Aloe Vera",
                "pt": "Loção Corporal Aloe Vera",
                "it": "Lozione Corpo Aloe Vera",
                "en": "Aloe Vera Body Lotion"
            },
            description_detailed={
                "es": "Loción corporal hidratante enriquecida con aloe vera orgánico al 95%. Calma, hidrata y suaviza la piel. Textura ligera de rápida absorción.",
                "pt": "Loção corporal hidratante enriquecida com aloe vera orgânico a 95%. Acalma, hidrata e suaviza a pele. Textura leve de rápida absorção.",
                "it": "Lozione corpo idratante arricchita con aloe vera biologico al 95%. Calma, idrata e ammorbidisce la pelle. Texture leggera ad assorbimento rapido.",
                "en": "Moisturizing body lotion enriched with 95% organic aloe vera. Soothes, hydrates and softens the skin. Fast-absorbing light texture."
            },
            made_in={
                "country_code": "ES",
                "made_in_text": {
                    "es": "Fabricado en España",
                    "pt": "Fabricado em Espanha",
                    "it": "Fabbricato in Spagna",
                    "en": "Made in Spain"
                }
            },
            distributor={
                "company_name": "Natural Cosmetics Europa S.L.",
                "cif": "B99887766",
                "addresses": {
                    "es": "Avenida Natura 555, 03001 Alicante, España",
                    "pt": "Avenida Natural 555, 8000-300 Faro, Portugal"
                }
            },
            net_weight_value=250,
            net_weight_unit="ml",
            format_type="Botella",
            format_material="Plástico reciclado",
            format_closure="Dispensador bomba",
            packaging_languages=["ES", "PT", "IT", "EN"],
            pao="12M",
            natural_origin_percentage={"value": 95, "certified": True, "certification_name": "COSMOS Natural"},
            inci_ingredients="Aloe Barbadensis Leaf Juice, Aqua, Glycerin, Cetearyl Alcohol, Caprylic/Capric Triglyceride",
            allergens_free_from=["Parabenos", "Siliconas", "Colorantes artificiales"],
            mode_of_use={
                "es": "Aplicar generosamente sobre la piel limpia de todo el cuerpo. Masajear hasta su completa absorción. Uso diario.",
                "pt": "Aplicar generosamente sobre a pele limpa de todo o corpo. Massajar até completa absorção. Uso diário.",
                "it": "Applicare generosamente sulla pelle pulita di tutto il corpo. Massaggiare fino al completo assorbimento. Uso quotidiano.",
                "en": "Apply generously to clean skin all over the body. Massage until fully absorbed. Daily use."
            },
            general_warnings={
                "es": "Solo para uso externo. Evitar el contacto con los ojos. En caso de contacto, aclarar con agua abundante.",
                "pt": "Apenas para uso externo. Evitar contacto com os olhos. Em caso de contacto, lavar abundantemente com água.",
                "it": "Solo per uso esterno. Evitare il contatto con gli occhi. In caso di contatto, sciacquare abbondantemente con acqua.",
                "en": "For external use only. Avoid contact with eyes. If contact occurs, rinse thoroughly with water."
            },
            current_version="1.0",
            status="approved",
            created_by="admin",
            updated_by="admin"
        )
    ]
    
    created_count = 0
    skipped_count = 0
    
    for product in sample_products:
        existing = db.query(ProductSheet).filter(ProductSheet.sku == product.sku).first()
        if existing:
            print(f"  ⚠ Product {product.sku} already exists, skipping")
            skipped_count += 1
        else:
            db.add(product)
            created_count += 1
            print(f"  ✓ Created product: {product.sku} - {product.title_short.get('es', 'N/A')}")
    
    db.commit()
    db.close()
    
    print(f"✅ Sample products created: {created_count} new, {skipped_count} skipped")


def main():
    """Main initialization function."""
    print("\n" + "="*60)
    print("  Database Initialization - Revisiones-Traducciones-Ultimate")
    print("="*60 + "\n")
    
    try:
        init_database()
        load_presets()
        create_sample_products()
        
        print("\n" + "="*60)
        print("  ✅ Initialization completed successfully!")
        print("="*60 + "\n")
        
        print("Next steps:")
        print("  1. Start the server: python launcher.py")
        print("  2. Access API docs: http://localhost:8000/docs")
        print("  3. Test with sample products:")
        print("     - GET /api/products/CF-HYD-001 (Facial Cream)")
        print("     - GET /api/products/CS-AGE-002 (Anti-Aging Serum)")
        print("     - GET /api/products/FP-ORG-003 (Organic Pasta)")
        print("     - GET /api/products/FS-VIT-004 (Vitamin C)")
        print("     - GET /api/products/CB-LOT-005 (Body Lotion)")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
