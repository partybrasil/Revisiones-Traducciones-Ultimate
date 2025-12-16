# 🚀 REVISIONES-TRADUCCIONES-ULTIMATE | GitHub Copilot Complete Master Prompt

**Versión**: 1.0.0 | **Fecha**: 16 Diciembre 2025 | **Estado**: Prototipado 65% Ready for Completion

---

## 📋 MISIÓN OPERACIONAL CLARA

Eres el **Ingeniero Senior de Prototipado** responsable de completar **Revisiones-Traducciones-Ultimate** en **4 FASES = 40-50 horas concentradas**: (1) Auditoría 2h, (2) Backend Core 16h, (3) Frontend MVP 18h, (4) Testing & Docs 8h.

**Estado Actual**: Backend 70% (falta VersionManager, ComplianceValidator, PresetManager, TranslationEngine, ImageScraper completos). Frontend 40% (componentes sketch sin binding ni servicios integrados). CERO líneas de testing.

**Outcome Final**: MVP 100% funcional que crea fichas → traduce 6 idiomas → valida compliance PT/IT/ES → importa/exporta Excel/PDF → gestiona imágenes → timeline histórico → restore versiones → Dashboard responsive + Catálogo con filtros.

---

## 1️⃣ STACK TÉCNICO & ARQUITECTURA JUSTIFICADA

**Backend**: Python FastAPI + SQLAlchemy ORM + PostgreSQL con JSON columns
- **Por qué FastAPI**: Async nativo, type hints, documentación OpenAPI automática, validación Pydantic integrada, perfecto para prototipado empresarial rápido
- **SQLAlchemy**: ORM pythonic, soporte JSONB para campos polimórficos, migraciones Alembic, índices optimizados
- **PostgreSQL**: ACID compliance (auditoría crítica), JSONB native support (multiidioma), full-text search, indices B-tree eficientes
- **Performance**: AsyncIO, connection pooling, índices UNIQUE(sku), INDEX(family, status, created_date DESC)

**Frontend**: Vue.js 3 + Vite + Pinia + Tailwind CSS
- **Vue.js 3**: Reactividad elegante, composition API, rendimiento superior, comunidad enterprise
- **Vite**: Bundling sub-milisegundos, hot module replacement, tree-shaking automático
- **Pinia**: State management simple, type-safe, devtools integration, inmutable updates
- **Tailwind**: Utility-first, CSS purging, responsive defaults, custom design tokens
- **Performance**: Lazy load components, code splitting per route, imagen optimization, CSS purging

**Database Schema Justificación**: ProductSheet (table products) + ProductVersion (snapshots JSONB completos) + ProductChangelog (granular field-level changes) + LegalRule (YAML hydrated) + Preset (auto-fill templates)

---

## 2️⃣ ESTADO ACTUAL EXACTO - AUDITORÍA CRÍTICA

### Backend Structure Actual
```
backend/ ✅ PARCIAL
├── main.py ✅ (FastAPI init, basic CRUD routes functional)
├── models/ ✅ PARCIAL
│   ├── product.py ✅ (ProductSheet ORM definido, campos OK)
│   └── version.py ⚠️ (Tables definidas pero sin métodos)
├── core/ ✅ PARCIAL
│   ├── product_sheet_manager.py ✅ (CRUD básico funcional: create, read, update, delete)
│   ├── version_manager.py ❌ FALTA (0 líneas - BLOQUEADOR)
│   └── preset_manager.py ❌ FALTA (0 líneas - IMPORTANTE)
├── legal_framework/ ❌ VACÍO
│   ├── compliance_validator.py ❌ FALTA (0 líneas - BLOQUEADOR)
│   └── rules/ ❌ (Sin YAML files - portugal_rules.yaml, italy_rules.yaml, spain_rules.yaml FALTAN)
├── translations/ ❌ VACÍO
│   ├── translation_engine.py ❌ FALTA (0 líneas - IMPORTANTE)
│   ├── translation_memory.json ❌ (Vacío - FALTA data inicial)
│   └── glossaries/ ❌ (Sin YAML glossary_* - FALTAN)
├── import_export/ ❌ VACÍO
│   ├── import_export_manager.py ❌ FALTA (0 líneas - BLOQUEADOR)
│   └── excel_template_generator.py ❌ FALTA
├── image_handler/ ❌ VACÍO
│   ├── image_scraper.py ❌ FALTA (0 líneas - IMPORTANTE)
│   └── image_storage.py ❌ FALTA
└── routes/ ✅ PARCIAL
    ├── products.py ✅ (GET/POST/PUT/DELETE básicos)
    ├── versions.py ❌ FALTA (0 líneas)
    ├── legal.py ❌ FALTA (0 líneas)
    ├── import_export.py ❌ FALTA (0 líneas)
    └── images.py ❌ FALTA (0 líneas)
```

### Frontend Structure Actual
```
frontend/src/ ✅ PARCIAL
├── App.vue ✅ (Router setup básico)
├── router/index.js ✅ (Rutas definidas pero sin lazy load)
├── stores/ ⚠️ INCOMPLETO (Pinia setup pero vacío de lógica)
│   ├── productStore.js ⚠️ (State skeleton, acciones STUB)
│   ├── versionStore.js ❌ FALTA (0 líneas)
│   ├── legalStore.js ❌ FALTA (0 líneas)
│   └── uiStore.js ❌ FALTA (0 líneas)
├── services/ ⚠️ INCOMPLETO
│   ├── apiClient.js ⚠️ (Axios setup básico, sin interceptors)
│   ├── productService.js ⚠️ (Métodos stub, no integrados)
│   ├── versionService.js ❌ FALTA (0 líneas)
│   ├── legalService.js ❌ FALTA (0 líneas)
│   ├── importExportService.js ❌ FALTA (0 líneas)
│   └── imageService.js ❌ FALTA (0 líneas)
├── components/ ✅ PARCIAL
│   ├── Dashboard.vue ⚠️ (Layout OK, datos placeholders)
│   ├── CatalogView.vue ⚠️ (Layout OK, sin filtros funcionales)
│   ├── ProductCard.vue ✅ (Display simple OK)
│   ├── ProductSheetEditor.vue ⚠️ (9 tabs definidos, inputs SIN v-model, sin validación)
│   ├── LegalAlerts.vue ❌ FALTA (0 líneas - CRÍTICO)
│   ├── VersionHistory.vue ❌ FALTA (0 líneas - CRÍTICO)
│   ├── DiffViewer.vue ❌ FALTA (0 líneas - CRÍTICO)
│   └── ImportExport.vue ❌ FALTA (0 líneas - CRÍTICO)
├── assets/
│   ├── tailwind.css ✅ (OK)
│   └── design-system.css ✅ (Colores/tipografía definidos)
└── config files ✅ (vite.config.js, tailwind.config.js, package.json OK)
```

### Documentación & Config
```
├── README.md ⚠️ (Básico, falta architecture)
├── PROJECT_STATUS.md ⚠️ (Desactualizado)
├── docker-compose.yml ❌ FALTA (0 líneas)
├── .github/workflows/ci.yml ❌ FALTA (0 líneas)
└── Dockerfile ❌ FALTA (0 líneas)
```

**SÍNTESIS**: 12 archivos backend FALTA implementar completamente (VersionManager, ComplianceValidator, PresetManager, TranslationEngine, ImageScraper, ImageStorage, routes completas). 6 servicios frontend FALTA. 4 componentes Vue FALTA. Tests = 0 líneas. Docker/CI = 0 líneas.

---

## 3️⃣ FASE 2: BACKEND CORE COMPLETION (16 HORAS)

### 3.1 VersionManager - Snapshots Granulares & Restore

**ARCHIVO**: `backend/core/version_manager.py` | **400-500 LOC esperadas** | **BLOQUEADOR 🔴**

**CONCEPTO**: Cada vez que usuario guarda ficha → snapshot automático JSONB completo + changelog field-by-field + versionado inteligente (1.0→1.1 minor, →2.0 major)

**MÉTODOS REQUERIDOS**:

1. **create_snapshot(sku: str, version_type: str, change_summary: str) → dict**
   - Query DB obtener ProductSheet actual
   - Obtener versión anterior si existe (else None)
   - Calcular version_number: Si no existe = "1.0", else incrementar según version_type (minor: "1.0"→"1.1", major: "1.0"→"2.0")
   - Serializar COMPLETO ProductSheet a dict (all fields, nested JSON)
   - Crear entrada ProductVersion con complete_snapshot JSONB = dict serializado
   - SOLO si existe versión anterior: calculate_diff(old_dict, new_dict)
   - Crear N entries ProductChangelog (una por cada field que cambió)
   - UPDATE products SET current_version = new_version_number, updated_date = now(), updated_by = user
   - COMMIT transaction
   - RETORNAR: {sku, version_number, changes_count, critical_changes, timestamp, status_badge}

2. **calculate_diff(old_state: dict, new_state: dict) → List[dict]**
   - Función PURA (no modifica state)
   - Comparar TODOS los fields recursivamente (use flatten_dict helper)
   - Para cada field diferente:
     - Si old=None & new!=None: change_type="added", severity="critical" si es PT/IT/ES critical field, else "important"
     - Si old!=None & new=None: change_type="deleted", severity="important"
     - Si old!=new: change_type="updated", severity="critical" si critical field, else "minor"
   - Retornar List sorted by severity DESC (critical→important→minor), then by field_path
   - EJEMPLO OUTPUT: `[{field_path: "title_short.pt", field_display_name: "Título PT", old_value: null, new_value: "Crema", change_type: "added", severity: "critical"}, ...]`

3. **get_snapshot(sku: str, version: str) → dict**
   - Query product_versions WHERE sku=sku AND version_number=version
   - Desserializar complete_snapshot JSONB
   - RETORNAR estado completo de esa versión (desserializado)

4. **compare_versions(sku: str, v_from: str, v_to: str) → dict**
   - Obtener snapshots de ambas versiones via get_snapshot()
   - Aplicar calculate_diff()
   - Contar changes: added, updated, deleted
   - RETORNAR: {from_version: v_from, to_version: v_to, stats: {added: N, updated: N, deleted: N}, changes: List[dict], total_changes: N}

5. **get_timeline(sku: str) → List[dict]**
   - Query product_versions ORDER BY snapshot_date DESC
   - Map a: [{version_number, snapshot_date, created_by, change_summary, status ("current" o "archived"), changes_count}]
   - RETORNAR lista

6. **restore_version(sku: str, version: str) → dict**
   - Obtener complete_snapshot de ProductVersion(sku, version)
   - UPDATE tabla products SET ALL FIELDS from snapshot (deserializar JSONB)
   - Llamar create_snapshot() con version_type="major", change_summary=f"Restored from v{version}"
   - RETORNAR nueva versión creada (ej: v3.0 si estaba en v2.3)

**CAMPOS CRÍTICOS POR PAÍS** (para severity calculation):
- Portugal: title_short_pt, description_detailed_pt, inci_ingredients_pt, allergens_pt, mode_of_use_pt, warnings_pt, pao_symbol
- Italy: title_short_it, description_detailed_it, inci_ingredients_it, allergens_it, mode_of_use_it, warnings_it, pao_symbol
- Spain: inci_ingredients (cualquier idioma), allergens_es, mode_of_use_es, warnings_es, pao_symbol

**INTEGRACIÓN SQLALCHEMY**:
```python
from sqlalchemy.orm import Session
from models.product import ProductSheet, ProductVersion, ProductChangelog

with Session() as session:
    # Query
    product = session.query(ProductSheet).filter_by(sku=sku).first()
    prev_version = session.query(ProductVersion).filter_by(sku=sku).order_by(ProductVersion.snapshot_date.desc()).first()
    
    # Create
    new_version = ProductVersion(
        sku=sku,
        version_number="1.1",
        complete_snapshot=product.to_dict(),  # JSONB auto-serializes dict
        version_type="minor",
        snapshot_date=datetime.utcnow(),
        created_by=user_id,
        change_summary=summary
    )
    session.add(new_version)
    
    # Changelog entries
    for change in changes_list:
        changelog = ProductChangelog(
            sku=sku,
            version_from=prev_version.version_number,
            version_to=new_version.version_number,
            changed_by=user_id,
            changed_date=datetime.utcnow(),
            field_path=change["field_path"],
            old_value=change["old_value"],
            new_value=change["new_value"],
            change_type=change["change_type"],
            severity=change["severity"]
        )
        session.add(changelog)
    
    session.commit()
```

**TESTING**: 40 tests mínimo
- test_create_snapshot_first_time_creates_v1_0()
- test_create_snapshot_increments_minor_version()
- test_create_snapshot_increments_major_version()
- test_calculate_diff_added_field_critical()
- test_calculate_diff_updated_field_minor()
- test_calculate_diff_deleted_field()
- test_calculate_diff_sorts_by_severity()
- test_compare_versions_returns_correct_stats()
- test_get_timeline_returns_ordered_versions()
- test_restore_version_reverts_all_fields()
- test_restore_creates_new_major_version()
- test_restore_audit_trail_recorded()
- ... (30+ más edge cases)

---

### 3.2 ComplianceValidator - Validación Regulatoria Multapaís

**ARCHIVO**: `backend/legal_framework/compliance_validator.py` | **350-450 LOC** | **BLOQUEADOR 🔴**

**CONCEPTO**: Validar ProductSheet contra REGULACIONES PT/IT/ES automáticamente. Cada país tiene critical_requirements (🔴 OBLIGATORIO) + optional_requirements (🟡 RECOMENDADO).

**MÉTODOS REQUERIDOS**:

1. **__init__(self)**
   - Load YAML rules desde `backend/legal_framework/rules/`:
     - portugal_rules.yaml (INFARMED)
     - italy_rules.yaml (Ministero della Salute)
     - spain_rules.yaml (AEMPS)
   - Parsear estructura: `country_legal_framework → regulations_by_family → COSMETICS_FACIAL → critical_requirements array`
   - Crear índice CACHE: `{(country, family, field_name): rule_obj}` para O(1) lookup

2. **validate_for_country(sheet: ProductSheet, country: str) → dict**
   - Obtener todas las reglas críticas para (country, sheet.family)
   - ITERAR CADA critical_requirement:
     - Si rule.translation_mandatory=true: verificar que field tiene valor en ese idioma NO vacío
     - Si rule.translation_mandatory=false: verificar que field existe (not None)
     - Si field vacío/falta: ADD a critical_issues list
   - Calcular completion_percentage = (campos_válidos / total_critical_fields) * 100
   - Status: "COMPLIANT" (100%), "WARNING" (60-99%), "NON_COMPLIANT" (<60%)
   - RETORNAR: {status, percentage, critical_issues: [{field_name, error_message, example}], warnings: [], country, family}

3. **validate_field(field_name: str, value: any, country: str, family: str) → bool**
   - Lookup rule para (country, family, field_name)
   - Aplicar validaciones specifícas según field_type:
     - INCI: lista no vacía, cada item es string válido INCI code
     - Alérgenos: array de máx 14 alérgenos UE 1169/2011 específicos (Celery, Cereals, Crustaceans, Eggs, Fish, Lupin, Milk, Molluscs, Mustard, Peanuts, Sesame, Shellfish, Soy, Tree nuts)
     - Title: min 3 chars, max 200, sin caracteres dangerosos (<, >, &)
     - Warnings: min 10 chars, max 1000
     - PAO: valor in ["6M", "12M", "18M", "24M", "36M"]
   - RETORNAR True si pasa, False si falla

4. **get_critical_missing(sheet: ProductSheet, country: str) → List[dict]**
   - Encontrar TODOS los critical_requirements que están vacíos/missing
   - Retornar list: `[{field_name, field_display_name, error_message, example, severity_emoji: "🔴 CRÍTICO"}, ...]`

5. **calculate_compliance_percentage(sheet: ProductSheet, country: str) → int**
   - Validar TODOS critical_requirements
   - Retornar (campos_válidos / total) * 100 como int (0-100)

6. **get_critical_fields_by_country(country: str, family: str) → List[str]**
   - Retornar lista de field_names que son críticos: ["title_short_pt", "description_detailed_pt", ...]

**YAML RULES STRUCTURE** (crear 3 archivos):

```yaml
# backend/legal_framework/rules/portugal_rules.yaml
country_legal_framework:
  country: "Portugal"
  code: "PT"
  authority: "INFARMED - Instituto Nacional da Farmácia e do Medicamento"
  
  regulations_by_family:
    COSMETICS_FACIAL:
      regulations:
        - "Regulamento (CE) nº 1223/2009"
        - "Decreto-Lei nº 189/2008"
      critical_requirements:
        - field: "title_short_pt"
          name: "Título Curto PT"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Designação do produto em português obrigatória"
          error_message: "O título em português está ausente ou vazio"
          example: "Creme Hidratante Facial 24h"
        - field: "description_detailed_pt"
          name: "Descrição Detalhada PT"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Descrição completa em português para conformidade INFARMED"
          error_message: "A descrição em português é obrigatória"
          example: "Creme facial hidratante com ácido hialurônico..."
        - field: "inci_ingredients_pt"
          name: "Ingredientes INCI"
          translation_mandatory: false
          severity: "🔴 CRÍTICO"
          description: "Lista INCI completa (idioma não importa, contanto que seja válida)"
          error_message: "INCI ausente ou inválida"
          example: "WATER, GLYCERIN, PHENOXYETHANOL, ..."
        - field: "allergens_pt"
          name: "Alérgenos Declarados"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Declaração clara de 14 alérgenos UE 1169/2011 em português"
          error_message: "Declaração de alérgenos obrigatória"
          example: "Contém: Amendoim, Frutos de casca rija. Pode conter: Leite"
        - field: "mode_of_use_pt"
          name: "Modo de Emprego"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Instruções de uso em português"
          error_message: "Instruções de uso obrigatórias"
          example: "Aplicar pequena quantidade na face limpa e massajar até absorção completa"
        - field: "warnings_pt"
          name: "Avisos e Precauções"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Avisos obrigatórios em português"
          error_message: "Avisos obrigatórios ausentes"
          example: "Evitar contacto com olhos. Usar protetor solar. Se irritação, suspender uso."
        - field: "pao_symbol"
          name: "PAO (Período Após Abertura)"
          translation_mandatory: false
          severity: "🔴 CRÍTICO"
          description: "Símbolo PAO: 6M, 12M, 18M, 24M ou 36M"
          error_message: "PAO não especificado"
          example: "12M"
      optional_requirements:
        - field: "made_in_pt"
          name: "Origem PT"
          translation_mandatory: true
          severity: "🟡 RECOMENDADO"
          description: "País de origem em português"
          example: "Fabricado em Portugal"
        - field: "natural_origin_percentage"
          name: "% Origem Natural"
          translation_mandatory: false
          severity: "🟡 RECOMENDADO"
          description: "Percentagem de ingredientes de origem natural certificada"
          example: "92% de ingredientes de origem natural"

    FOOD_PACKAGED:
      regulations:
        - "Regulamento (UE) 1169/2011"
      critical_requirements:
        - field: "title_short_pt"
          name: "Nome Produto PT"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          error_message: "Nome do produto em português obrigatório"
          example: "Chocolate Negro 70%"
        - field: "allergens_pt"
          name: "Alérgenos (14 UE)"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          error_message: "Alérgenos 1169/2011 obrigatórios"
          example: "Contém: Cacau, Leite. Pode conter: Frutos secos"
        - field: "net_weight_value"
          name: "Peso Líquido"
          translation_mandatory: false
          severity: "🔴 CRÍTICO"
          error_message: "Peso líquido obrigatório"
          example: 250
        - field: "net_weight_unit"
          name: "Unidade Peso"
          translation_mandatory: false
          severity: "🔴 CRÍTICO"
          error_message: "Unidade peso obrigatória"
          example: "g"

# Repetir estructura para ITALY y SPAIN (suffixes _it, _es)
```

**TESTING**: 35 tests
- test_validate_cosmetics_facials_portugal_compliant()
- test_validate_cosmetics_facials_portugal_missing_title_pt()
- test_validate_cosmetics_facials_portugal_missing_warnings_pt()
- test_validate_allergens_max_14_eu()
- test_validate_allergens_invalid_allergen()
- test_validate_inci_valid_codes()
- test_validate_inci_empty_fails()
- test_validate_pao_valid_values()
- test_validate_pao_invalid_value()
- test_compliance_percentage_100_when_all_critical_present()
- test_compliance_percentage_60_when_half_missing()
- test_compliance_percentage_0_when_all_missing()
- test_status_compliant_when_100_percent()
- test_status_warning_when_60_99_percent()
- test_status_non_compliant_when_less_60()
- test_get_critical_missing_returns_list()
- test_multi_country_same_product_different_validation()
- test_food_packaged_validation_rules()
- ... (17+ edge cases)

---

### 3.3 PresetManager - Auto-Fill Inteligente por Familia

**ARCHIVO**: `backend/core/preset_manager.py` | **250-300 LOC** | **IMPORTANTE 🟡**

**CONCEPTO**: 150+ familias de productos (COSMETICS_FACIAL, COSMETICS_BODY, FOOD_PACKAGED, SUPPLEMENTS, etc). Cada familia tiene preset con modo_de_uso, avisos, alérgenos típicos, pictogramas, PAO default. Al crear ficha + seleccionar familia → auto-fill estos campos.

**MÉTODOS**:

1. **__init__(self)**
   - Load presets YAML desde `backend/presets/150_families.yaml`
   - Crear índice: `{family_code: preset_obj}`

2. **load_preset(family: str) → dict**
   - Retornar preset completo: `{family, display_name, mode_of_use_es/pt/it, warnings_es/pt/it, typical_allergens: [], typical_pictograms: [], pao_default: "12M", natural_origin_range: "50-100%"}`

3. **apply_preset(sheet: ProductSheet, family: str) → ProductSheet**
   - Cargar preset
   - Aplicar valores a campos SOLO si están vacíos (NO sobrescribir existing):
     ```python
     if not sheet.mode_of_use_es or sheet.mode_of_use_es == "":
         sheet.mode_of_use_es = preset["mode_of_use_es"]
     if not sheet.warnings_es or sheet.warnings_es == "":
         sheet.warnings_es = preset["warnings_es"]
     if not sheet.allergens_present or len(sheet.allergens_present) == 0:
         sheet.allergens_present = preset["typical_allergens"]
     if not sheet.pictograms or len(sheet.pictograms) == 0:
         sheet.pictograms = preset["typical_pictograms"]
     if not sheet.pao or sheet.pao == "":
         sheet.pao = preset["pao_default"]
     ```
   - RETORNAR sheet actualizado
   - Contar campos autollenados para log

4. **get_available_families() → List[dict]**
   - Retornar lista de TODAS familias: `[{code: "COSMETICS_FACIAL", display_name: "Cosméticos Faciales", subfamily_count: 12}, ...]`
   - Mínimo 150 families

5. **get_preset_fields(family: str) → dict**
   - Retornar estructura útil para frontend:
     ```python
     {
       "autofillable_fields": ["mode_of_use_es", "warnings_es", "allergens_present", "pictograms", "pao"],
       "suggested_values": {...},
       "allergen_examples": ["PARFUM", "LIMONENE", ...],
       "pictogram_examples": ["skin_irritation", "eye_irritation"]
     }
     ```

**PRESETS YAML** (crear `backend/presets/150_families.yaml` - ESTRUCTURA MÍNIMA con 10 families, expandir a 150):

```yaml
presets:
  COSMETICS_FACIAL:
    display_name: "Cosméticos Faciales"
    subfamilies: ["Cremas Hidratantes", "Sérums", "Máscaras", "Limpiadoras"]
    mode_of_use_es: "Aplicar pequeña cantidad en la cara limpia y masajear suavemente hasta absorción completa. Usar mañana y noche."
    mode_of_use_pt: "Aplicar pequena quantidade no rosto limpo e massajear suavemente até absorção completa. Usar manhã e noite."
    mode_of_use_it: "Applicare una piccola quantità sul viso pulito e massaggiare delicatamente fino al completo assorbimento. Utilizzare mattina e sera."
    warnings_es: "Uso externo. Evitar contacto con los ojos. Si es irritante, suspender el uso. Mantener fuera del alcance de los niños. Usar protetor solar."
    warnings_pt: "Uso externo. Evitar contacto com os olhos. Se irritante, suspender o uso. Manter fora do alcance das crianças. Usar protetor solar."
    warnings_it: "Uso esterno. Evitare il contatto con gli occhi. Se irritante, sospendere l'uso. Tenere fuori dalla portata dei bambini. Usare filtro solare."
    typical_allergens: ["PARFUM", "LIMONENE", "BENZYL ALCOHOL", "PHENOXYETHANOL"]
    typical_pictograms: ["skin_irritation", "eye_irritation"]
    pao_default: "12M"
    natural_origin_range: "50-100%"

  COSMETICS_BODY:
    display_name: "Cosméticos Corporales"
    subfamilies: ["Cremas", "Lociones", "Geles"]
    mode_of_use_es: "Aplicar sobre la piel seca o humedecida. Masajear hasta absorción. Usar diariamente."
    warnings_es: "Uso externo. Evitar contacto con ojos. Mantener fuera del alcance de niños."
    typical_allergens: ["PARFUM", "LIMONENE"]
    pao_default: "18M"

  FOOD_PACKAGED:
    display_name: "Alimentos Empaquetados"
    subfamilies: ["Snacks", "Bebidas", "Conservas", "Congelados"]
    mode_of_use_es: "Almacenar en lugar fresco y seco. Consumir preferentemente antes de la fecha indicada en el envase."
    warnings_es: "Puede contener trazas de frutos secos, trigo y soja. No apto para celíacos."
    typical_allergens: ["Gluten", "Frutos de cáscara", "Soja", "Leche"]
    typical_pictograms: []
    pao_default: "24M"

  SUPPLEMENTS:
    display_name: "Suplementos Nutricionales"
    mode_of_use_es: "Tomar 1-2 cápsulas diarias con agua. No exceder la dosis recomendada."
    warnings_es: "Suplemento alimenticio, no medicamento. Consultar médico si está embarazada, lactancia o toma medicamentos."
    typical_allergens: ["Soja", "Gluten"]
    pao_default: "36M"

  # ... 146 familias más con estructura similar
```

**TESTING**: 20 tests
- test_load_preset_returns_all_fields()
- test_apply_preset_fills_empty_fields()
- test_apply_preset_does_not_overwrite_existing()
- test_apply_preset_counts_autofilled_fields()
- test_get_available_families_returns_150_families()
- test_get_available_families_structure_correct()
- test_get_preset_fields_returns_examples()
- ... (13+ edge cases)

---

### 3.4 TranslationEngine - Sugerencias Multidioma Fuzzy

**ARCHIVO**: `backend/translations/translation_engine.py` | **300-400 LOC** | **IMPORTANTE 🟡**

**CONCEPTO**: Usuario escribe en ES → motor sugiere traducciones PT/IT/EN/FR/BR automáticamente via fuzzy matching en translation_memory + glossary lookups.

**MÉTODOS**:

1. **__init__(self)**
   - Load translation_memory.json (dict)
   - Load glossaries desde `backend/translations/glossaries/`:
     - glossary_cosmetics_pt.yaml
     - glossary_cosmetics_it.yaml
     - glossary_food_pt.yaml
     - etc.
   - Initialize fuzzy matcher (use `difflib.get_close_matches` o `fuzzywuzzy` library)

2. **suggest_translation(source_text: str, source_lang: str, target_lang: str, threshold: float = 0.75) → List[str]**
   - Buscar en translation_memory[f"{source_lang}-{target_lang}"] si existe exact match
   - Si no exact: usar fuzzy matching para encontrar similares
   - Si fuzzy score > threshold (0.75): include en suggestions
   - Buscar glossary terms: si source_text contiene key_term, retornar translation_glossary
   - Ejemplo: source="Crema Hidratante" → suggest("es", "pt") → ["Creme Hidratante", "Creme Moisturizer (moisturizing cream)"]
   - RETORNAR máx 5 sugerencias ordenadas por confidence DESC

3. **save_translation(source_text: str, target_text: str, source_lang: str, target_lang: str)**
   - Guardar en translation_memory:
     ```python
     key = f"{source_lang}-{target_lang}"
     if source_text not in translation_memory[key]:
         translation_memory[key][source_text] = {
             "translations": [target_text],
             "count": 1,
             "timestamp": datetime.utcnow()
         }
     else:
         translation_memory[key][source_text]["translations"].append(target_text)
         translation_memory[key][source_text]["count"] += 1
     ```
   - Persist a file: `json.dump(translation_memory, open(filepath, 'w'))`

4. **get_glossary(family: str, target_lang: str) → dict**
   - Load glossary_FAMILY_LANG.yaml (ejemplo: glossary_cosmetics_pt.yaml)
   - RETORNAR dict: `{key_term_es: translation_pt, ...}`

5. **load_translation_memory(filepath: str = "backend/translations/translation_memory.json")`
   - Parse JSON
   - Validar estructura
   - RETORNAR dict

6. **export_memory_to_csv(output_path: str)**
   - Exportar translation_memory a CSV con columns: source_text, target_text, source_lang, target_lang, count, confidence

**TRANSLATION MEMORY INITIAL** (crear `backend/translations/translation_memory.json`):

```json
{
  "es-pt": {
    "Crema Hidratante": ["Creme Hidratante", 5],
    "Modo de Empleo": ["Modo de Emprego", 3],
    "Advertencia": ["Aviso", 2],
    "Sin Gluten": ["Sem Glúten", 1]
  },
  "es-it": {
    "Crema Hidratante": ["Crema Idratante", 4],
    "Aviso": ["Avvertenza", 2],
    "Ingrediente": ["Ingrediente", 1]
  },
  "es-en": {
    "Crema": ["Cream", 10],
    "Modo de Empleo": ["Instructions for use", 5]
  }
}
```

**GLOSSARIES** (crear `backend/translations/glossaries/glossary_cosmetics_pt.yaml`):

```yaml
COSMETICS_FACIAL:
  "Crema Hidratante": "Creme Hidratante"
  "Sérum": "Sérum"
  "Máscara": "Máscara"
  "Limpiadora": "Limpadora"
  "Modo de Empleo": "Modo de Emprego"
  "Aviso": "Aviso"
  "Alérgeno": "Alergénio"
  "Ingrediente": "Ingrediente"

FOOD_PACKAGED:
  "Sin Gluten": "Sem Glúten"
  "Alérgeno": "Alergénio"
  "Conservante": "Conservante"
  "Azúcar": "Açúcar"
```

**TESTING**: 25 tests
- test_suggest_translation_exact_match()
- test_suggest_translation_fuzzy_match()
- test_suggest_translation_above_threshold()
- test_suggest_translation_below_threshold()
- test_suggest_translation_from_glossary()
- test_save_translation_creates_entry()
- test_save_translation_increments_count()
- test_get_glossary_returns_dict()
- test_export_memory_to_csv()
- ... (16+ edge cases)

---

### 3.5 ImportExportManager - Operaciones MASIVAS Excel/PDF

**ARCHIVO**: `backend/import_export/import_export_manager.py` | **400-500 LOC** | **BLOQUEADOR 🔴**

**CONCEPTO**: Descargar template Excel 60+ columnas → rellenar datos masivos → importar 23 productos en 1 click. Exportar fichas a PDF profesional con imágenes, pictogramas, tabla compliance.

**MÉTODOS**:

1. **generate_excel_template() → bytes**
   - Usar openpyxl library
   - Crear Excel A4:
     - Row 1: Headers (60+ columnas):
       - SKU, EAN_PRIMARY, EAN_SECONDARY, TITLE_ES_SHORT, TITLE_PT_SHORT, TITLE_IT_SHORT
       - BRAND, GAMA_ES, FAMILY, SUBFAMILY
       - NET_WEIGHT, NET_WEIGHT_UNIT, GROSS_WEIGHT, HEIGHT_CM, WIDTH_CM, DEPTH_CM
       - FORMAT_TYPE, FORMAT_MATERIAL, FORMAT_CLOSURE
       - INCI_INGREDIENTS, MODE_OF_USE_ES, MODE_OF_USE_PT, MODE_OF_USE_IT
       - WARNINGS_ES, WARNINGS_PT, WARNINGS_IT
       - PAO, ALLERGENS, PICTOGRAMS, NATURAL_ORIGIN_PERCENTAGE
       - MADE_IN, DISTRIBUTOR_NAME, RESPONSIBLE_PERSON_NAME, etc.
     - Row 2: Ejemplos (datos de demostración):
       - CF-HYD-001, 5412345678901, , "Crema Hidratante", "Creme Hidratante", "Crema Idratante"
       - MiMarca, Facial, COSMETICS_FACIAL, Cremas
       - 50, "ml", 75, 10.5, 8.2, 4.0
       - Botella, Plástico, Rosca
       - "WATER, GLYCERIN, PHENOXYETHANOL", "Aplicar...", "Aplicar...", "Applicare..."
       - "Evitar ojos", "Evitar olhos", "Evitare occhi"
       - "12M", "Fragancia", "skin_irritation, eye_irritation", 92
       - "Fabricado en España", "DistribuidorS.A.", "Juan García", etc.
     - Datavalidation dropdowns:
       - FAMILY: 150 opciones (COSMETICS_FACIAL, COSMETICS_BODY, FOOD_PACKAGED, SUPPLEMENTS, ...)
       - FORMAT_TYPE: (Botella, Tubo, Tarro, Caja, Bolsa)
       - FORMAT_MATERIAL: (Plástico, Vidrio, Aluminio, Cartón)
       - PAO: (6M, 12M, 18M, 24M, 36M)
       - NET_WEIGHT_UNIT: (g, ml, kg, L)
     - Color-coding headers:
       - 🔴 Red: critical fields (SKU, TITLE_ES_SHORT, INCI_INGREDIENTS, ALLERGENS, MODE_OF_USE)
       - 🟡 Yellow: recommended (BRAND, GAMA_ES, MADE_IN)
       - ⚪ White: optional (todas las demás)
     - Autosize columns, freeze header row
   - RETORNAR bytes via BytesIO

2. **import_from_excel(file_path: str) → dict**
   - Usar openpyxl para leer Excel
   - Iterar filas (skip header+ejemplo, start from row 3):
     - Validaciones:
       - SKU: no vacío, format check (alphanumeric + dash)
       - EAN: si existe, validar checksum (algoritmo EAN-13)
       - TITLE_ES_SHORT: no vacío, min 3 chars
       - FAMILY: debe estar en lista 150 familias
       - NET_WEIGHT_VALUE: si existe, debe ser float > 0
       - PAO: si existe, debe estar en lista válidos
     - Si ERROR: add a errors_list con {row_number, sku, error_message}
     - Si VÁLIDA:
       - Crear ProductSheet() con datos del row
       - Aplicar preset via PresetManager.apply_preset()
       - Guardar en DB
       - Crear v1.0 snapshot automático
   - RETORNAR dict:
     ```python
     {
       "imported": 23,
       "errors": [],
       "skipped": 0,
       "status": "SUCCESS",
       "completion_percentage": 45,
       "log": "23 productos importados exitosamente"
     }
     ```

3. **export_to_pdf(sku: str) → bytes**
   - Usar ReportLab library
   - Generar PDF A4 profesional:
     - Header (top):
       - Logo placeholder (1cm x 1cm left)
       - Título: "FICHA DE PRODUCTO"
       - Subtítulo: SKU + EAN
     - Body (2 columnas):
       - LEFT (60%):
         - General Info (tabla 2 cols: label | value):
           - SKU: CF-HYD-001
           - EAN: 5412345678901
           - Brand: MiMarca
           - Family: Cosméticos Faciales
           - Subfamily: Cremas Hidratantes
         - Physical Properties (tabla):
           - Dimensiones: 10.5cm x 8.2cm x 4.0cm
           - Peso Neto: 50 ml
           - Peso Bruto: 75g
           - Formato: Botella Plástico Rosca
         - Composición (tabla):
           - Header: Ingrediente | INCI Code
           - Rows: 20+ INCI items
         - Modo de Uso (justified text, multiidioma):
           - ES, PT, IT columns
       - RIGHT (40%):
         - Metadata:
           - Fabricante: País flags con texto
           - Distribuidor: empresa + CIF + direcciones
           - Responsable Legal: nombre + email + phone
           - Origen Natural: % con icono
           - Certificaciones: lista con números + expiry dates
     - Warnings Section (highlight rojo):
       - ⚠️ icon
       - Avisos ES/PT/IT multiidioma
       - Precauciones especiales (embarazo, lactancia, niños)
     - Images Section:
       - Product images (3 fotos centradas, max 300x300px cada una)
       - Captions: Frontal / Trasera / Lateral
     - Compliance Footer:
       - 3 badges: 🇵🇹 compliance% | 🇮🇹 compliance% | 🇪🇸 compliance%
       - Verde si ✓ COMPLIANT, Amarillo si ⚠️ WARNING, Rojo si ❌ NON_COMPLIANT
     - Page numbers, date generated
   - RETORNAR bytes via BytesIO

4. **export_to_markdown(sku: str) → str**
   - Generar .md estructurado:
     ```markdown
     # Ficha de Producto: CF-HYD-001
     
     ## Información General
     
     | Propiedad | Valor |
     |-----------|-------|
     | SKU | CF-HYD-001 |
     | EAN | 5412345678901 |
     | Brand | MiMarca |
     | ...
     
     ## Composición INCI
     
     - WATER (Aqua)
     - GLYCERIN
     - PHENOXYETHANOL
     - ...
     
     ## Modo de Empleo
     
     ### Español
     Aplicar pequeña cantidad...
     
     ### Portugués
     Aplicar pequena quantidade...
     
     ### Italiano
     Applicare una piccola quantità...
     
     ## Avisos y Precauciones
     
     ⚠️ **Warnings**: [content]
     
     ## Cumplimiento Regulatorio
     
     | País | Compliance | Status |
     |------|-----------|--------|
     | PT 🇵🇹 | 95% | ✓ COMPLIANT |
     | IT 🇮🇹 | 75% | ⚠️ WARNING |
     | ES 🇪🇸 | 60% | ❌ NON_COMPLIANT |
     ```
   - RETORNAR string

5. **export_to_html(sku: str) → str**
   - Generar HTML con style inline (similar a markdown pero HTML tags)
   - Usable para email o web preview

6. **export_catalog_excel(filters: dict) → bytes**
   - Aplicar filtros: `{family: "", brand: "", status: "", created_after: date}`
   - Query múltiples ProductSheets
   - Generar Excel template con N rows de productos
   - RETORNAR bytes

**TESTING**: 30 tests
- test_excel_template_has_60_columns()
- test_excel_template_has_datavalidation_dropdowns()
- test_excel_template_color_coding_headers()
- test_import_excel_valid_data_creates_products()
- test_import_excel_invalid_ean_checksum_fails()
- test_import_excel_missing_critical_field_fails()
- test_import_excel_returns_correct_stats()
- test_import_excel_creates_v1_0_snapshots()
- test_pdf_export_includes_all_sections()
- test_pdf_export_includes_images()
- test_pdf_export_includes_compliance_badges()
- test_pdf_export_multiidioma_content()
- test_markdown_export_structure_correct()
- test_html_export_style_inline()
- test_catalog_excel_respects_filters()
- test_catalog_excel_multiple_products()
- ... (15+ edge cases)

---

### 3.6 ImageScraper + ImageStorage - Gestión VISUAL

**ARCHIVOS**: `backend/image_handler/image_scraper.py` + `image_storage.py` | **250-300 LOC total** | **IMPORTANTE 🟡**

**ImageScraper Methods**:

1. **search_images(query: str, max_results: int = 20) → List[dict]**
   - Usar Bing Images API (gratuito) O web scraping beautifulsoup4
   - RETORNAR: `[{url: str, title: str, source: str, resolution: tuple (w,h)}, ...]`

2. **download_image(url: str, sku: str, image_type: str) → str**
   - GET request a URL
   - Validate formato (PIL.Image.open check)
   - Validate size < 10MB
   - Guardar en filesystem: `backend/storage/images/{sku}/{image_type}/image_{timestamp}.jpg`
   - RETORNAR local file path

3. **validate_image(file_path: str) → bool**
   - PIL.Image.open() check formato válido
   - Size < 10MB
   - Resolution > 100x100px
   - RETORNAR True/False

4. **resize_image(file_path: str, max_width: int = 3000) → None**
   - Usar Pillow (PIL)
   - Resize manteniendo aspect ratio
   - Comprimir a 85% quality JPEG

**ImageStorage Methods**:

1. **save_uploaded_file(file: UploadFile, sku: str, image_type: str) → str**
   - Recibir file multipart
   - validate_image()
   - Guardar en storage con timestamp filename
   - RETORNAR path

2. **get_image_path(sku: str, image_type: str) → str**
   - Retornar path completo

3. **delete_image(sku: str, image_type: str) → bool**
   - Delete file del filesystem
   - Update ProductSheet.product_images array (remove entry)
   - RETORNAR True si successful

**Storage Directory**:
```
backend/storage/images/
├── CF-HYD-001/
│   ├── frontal/
│   │   └── image_1702734000.jpg
│   ├── trasera/
│   │   └── image_1702734015.jpg
│   └── lateral/
│       └── image_1702734030.jpg
└── CF-VIT-001/
    └── frontal/
        └── image_1702741000.jpg
```

**TESTING**: 20 tests
- test_search_images_returns_list()
- test_search_images_returns_dict_with_required_fields()
- test_download_image_saves_file()
- test_download_image_validates_format()
- test_download_image_validates_size()
- test_validate_image_checks_format()
- test_validate_image_checks_size()
- test_validate_image_checks_resolution()
- test_resize_image_maintains_aspect_ratio()
- test_save_uploaded_file_persists()
- test_delete_image_removes_file()
- ... (9+ edge cases)

---

### 3.7 Database Migrations + Routes

**Alembic Migration**:
- crear migration: `alembic revision --autogenerate -m "Add version_manager, compliance, etc."`
- definir ProductVersion, ProductChangelog tables
- add indices: UNIQUE(sku), INDEX(family, status), INDEX(created_date DESC)
- upgrade: `alembic upgrade head`

**API Routes** (crear en `backend/routes/`):

**File: `routes/versions.py`**:
```python
@router.get("/api/products/{sku}/versions")
def get_versions(sku: str) → List[dict]

@router.get("/api/products/{sku}/versions/{version}")
def get_snapshot(sku: str, version: str) → dict

@router.get("/api/products/{sku}/versions/compare")
def compare_versions(sku: str, from_version: str, to_version: str) → dict

@router.post("/api/products/{sku}/versions/{version}/restore")
def restore_version(sku: str, version: str) → dict
```

**File: `routes/legal.py`**:
```python
@router.get("/api/legal/{country}/rules")
def get_rules(country: str) → dict

@router.post("/api/legal/validate")
def validate_compliance(sku: str, country: str) → dict

@router.get("/api/products/{sku}/compliance")
def get_compliance(sku: str) → dict
```

**File: `routes/import_export.py`**:
```python
@router.get("/api/import/template")
def download_template() → bytes (Excel file)

@router.post("/api/import/excel")
def import_excel(file: UploadFile) → dict

@router.get("/api/export/pdf/{sku}")
def export_pdf(sku: str) → bytes

@router.get("/api/export/markdown/{sku}")
def export_markdown(sku: str) → str

@router.get("/api/export/html/{sku}")
def export_html(sku: str) → str

@router.get("/api/export/catalog-excel")
def export_catalog(family: str = "", brand: str = "", status: str = "") → bytes
```

**File: `routes/images.py`**:
```python
@router.get("/api/images/search")
def search_images(q: str, max_results: int = 20) → List[dict]

@router.post("/api/images/upload")
def upload_image(sku: str, image_type: str, file: UploadFile) → str

@router.get("/api/images/{sku}/{image_type}")
def get_image(sku: str, image_type: str) → file

@router.delete("/api/images/{sku}/{image_type}")
def delete_image(sku: str, image_type: str) → bool
```

---

## 4️⃣ FASE 3: FRONTEND MVP INTEGRATION (18 HORAS)

### 4.1 Pinia Stores - State Management Completo

**Archivo**: `frontend/src/stores/` (4 archivos) | **200-250 LOC cada uno**

**productStore.js**:
- State: products[], currentProduct, loading, error, filters, pagination
- Actions: fetchProducts(filters, page), getProduct(sku), createProduct(data), updateProduct(sku, data), deleteProduct(sku), searchProducts(query)
- Getters: getProductBySku(sku), getFilteredProducts(), getProductCount(), isLoading

**versionStore.js**:
- State: versions[], currentVersion, changelog[], diff[]
- Actions: fetchVersions(sku), getSnapshot(sku, version), compareVersions(sku, v_from, v_to), restoreVersion(sku, version)
- Getters: getCurrentVersionNumber(), getTotalVersions(), hasMultipleVersions()

**legalStore.js**:
- State: countries[], complianceStatus{}, rules{}
- Actions: fetchRules(country), validateCompliance(sku, country), getComplianceStatus(sku)
- Getters: getCompliancePercentage(country), getComplianceStatus(country), getCountriesCompliant()

**uiStore.js**:
- State: darkMode, sidebarOpen, notifications[], modals{}
- Actions: addNotification(type, message), removeNotification(id), toggleDarkMode(), toggleSidebar(), openModal(name), closeModal(name)

### 4.2 API Services - Integración Backend

**Archivos**: `frontend/src/services/` (6 archivos) | **50-100 LOC cada uno**

**apiClient.js**: Axios instance con interceptors (auth header, error handling, retry logic)

**productService.js**: createSheet, getSheet, updateSheet, deleteSheet, listSheets, searchSheets

**versionService.js**: getVersions, getSnapshot, compareVersions, restoreVersion

**legalService.js**: getCountryRules, validateCompliance, getComplianceStatus

**importExportService.js**: getTemplateExcel, importExcel, exportPDF, exportMarkdown, exportHTML, exportCatalogExcel

**imageService.js**: searchImages, uploadImage, getImage, deleteImage

### 4.3 Vue Components - Vistas Funcionales

**LegalAlerts.vue** (200-250 LOC):
- Props: sku
- 3 country cards (PT/IT/ES con flags)
- Status badges (🔴🟡🟢)
- Compliance percentage + progress bar
- "Ver Detalles" → expandible con lista critical_issues
- Watch sku → fetch compliance

**VersionHistory.vue** (250-300 LOC):
- Timeline vertical con versiones
- Blue dot = current, gray = archived
- Botones: "Ver Snapshot", "Comparar", "Restaurar"
- Expandible con changes field by field

**DiffViewer.vue** (300-350 LOC):
- 2 selectores (De | A versiones)
- Stats row (added, updated, deleted counts)
- Changes grid (field | old | new)
- Highlighting inline de cambios
- "Restaurar" button

**ImportExport.vue** (350-400 LOC):
- 2 tabs: "Importar" | "Exportar"
- Tab 1: Drag-drop Excel, "Descargar Template", progress bar, results
- Tab 2: Format selector, filters (si bulk), "Exportar"

**ProductSheetEditor.vue UPDATE** (800-1000 LOC):
- Fix form v-model bindings (todos inputs)
- 9 tabs funcionales con contenido
- Validaciones real-time (character counter, required indicators)
- Preset auto-fill al seleccionar family
- Translation tab con sugerencias
- Images tab con upload + gallery
- Legal tab con LegalAlerts embed
- Auto-save debounced
- Completion percentage footer

**Dashboard.vue UPDATE** (300-350 LOC):
- 4 stat cards (total, families, brands, languages)
- Compliance overview (3 country cards)
- Recent activity timeline (últimas 5 acciones)
- Quick action buttons

**CatalogView.vue UPDATE** (350-400 LOC):
- Sidebar filters (family, brand, status, languages, date range)
- Search bar con debounce
- Product grid 4 columnas (responsive)
- Lazy load on scroll
- Pagination

### 4.4 Component Lifecycle & Integration

**Cada componente**:
- `onMounted`: fetch data via services
- `watch` store changes → rerender
- `v-model` binding a store state
- Manejadores errores + loading states
- Notificaciones toast en success/failure

---

## 5️⃣ FASE 4: TESTING & DOCUMENTATION (8 HORAS)

### Backend Tests (pytest)

**Coverage Target**: ≥80%

**Unit Tests** (150+ tests):
- `test_version_manager.py` (40 tests)
- `test_compliance_validator.py` (35 tests)
- `test_translation_engine.py` (25 tests)
- `test_import_export_manager.py` (30 tests)
- `test_image_scraper.py` (20 tests)

**Integration Tests**:
- test_product_creation_with_versioning.py
- test_compliance_workflow.py
- test_bulk_import_workflow.py
- test_export_pdf_with_images.py

**Run**: `pytest backend/ --cov=backend --cov-report=html` (target 80%+)

### Frontend Tests (Vitest)

**Component Tests** (50+ tests):
- ProductSheetEditor.spec.js
- CatalogView.spec.js
- LegalAlerts.spec.js
- VersionHistory.spec.js

**Store Tests**:
- productStore.spec.js
- versionStore.spec.js
- legalStore.spec.js

**Run**: `npm run test:unit --coverage` (target 70%+)

### E2E Tests (Playwright)

**5 Critical Flows** (30-45 min):
- e2e/create-product.spec.js: Crear ficha → v1.0 snapshot visible en Dashboard
- e2e/translate-product.spec.js: Open product → Translation tab → Fill PT → Save → v1.1 snapshot
- e2e/compliance.spec.js: Ficha incompleta → LegalAlerts PT NON_COMPLIANT → Edit → Complete → COMPLIANT
- e2e/version-restore.spec.js: v2.3 → Historial → Restaurar v2.0 → v3.0 creada
- e2e/bulk-import.spec.js: Download template → Fill 10 rows → Upload → 10 productos importados

**Run**: `npx playwright test e2e/` (should pass all 5 flows)

### Documentation

**README.md** (400+ words):
- Overview + key features
- Tech stack + justification
- Quick start (3 pasos)
- Architecture diagram (ASCII o visual)
- Usage guide con screenshots
- Contributing + license

**API_DOCUMENTATION.md** (500+ words):
- OpenAPI-style docs para todas rutas
- Request/response ejemplos
- Error codes + meanings

**ARCHITECTURE.md** (400+ words):
- Backend layers diagram
- Frontend component hierarchy
- Data flow diagrama
- Database schema explanation

**QUICKSTART.md** (actualizado):
- Clone repo
- Install dependencies (pip + npm)
- Setup .env
- Run `docker-compose up`
- Access http://localhost:5173

---

## 6️⃣ CHECKLIST EJECUCIÓN FINAL

### Día 1 (2h): Auditoría & Setup
- [ ] Clonar/actualizar repo
- [ ] Verificar estructura actual vs especificación
- [ ] Crear issue "Status Audit Report"
- [ ] Setup local environment (venv, node_modules, .env)

### Día 2-3 (16h): Backend Core
- [ ] VersionManager completo + tests (40 tests)
- [ ] ComplianceValidator completo + YAML rules + tests (35 tests)
- [ ] PresetManager completo + 150 families YAML + tests (20 tests)
- [ ] TranslationEngine completo + memory.json + glossaries + tests (25 tests)
- [ ] ImportExportManager completo + tests (30 tests)
- [ ] ImageScraper + ImageStorage completo + tests (20 tests)
- [ ] Database migrations Alembic
- [ ] API routes completas (versions, legal, import_export, images)
- [ ] TOTAL: 150+ backend tests passing

### Día 4-5 (18h): Frontend MVP
- [ ] Pinia stores (productStore, versionStore, legalStore, uiStore) completos
- [ ] API services (6 services) completos + apiClient interceptors
- [ ] LegalAlerts.vue + VersionHistory.vue + DiffViewer.vue + ImportExport.vue completos
- [ ] ProductSheetEditor.vue ACTUALIZADO (9 tabs, validaciones, presets, translations, images)
- [ ] Dashboard.vue ACTUALIZADO (stats, compliance, activity)
- [ ] CatalogView.vue ACTUALIZADO (filters, search, lazy load, pagination)
- [ ] Form bindings v-model completos
- [ ] 50+ frontend component tests passing

### Día 6 (8h): Testing & Docs
- [ ] Backend tests: 80%+ coverage
- [ ] Frontend tests: 70%+ coverage
- [ ] E2E tests: 5 flows passing
- [ ] Docker compose funcional
- [ ] GitHub Actions CI configured
- [ ] README.md completo
- [ ] API_DOCUMENTATION.md completo
- [ ] ARCHITECTURE.md completo
- [ ] QUICKSTART.md actualizado
- [ ] All PRs merged, main branch clean

### Validation Final (30 min):
- [ ] Create product → v1.0 snapshot ✓
- [ ] Translate to PT → v1.1 snapshot ✓
- [ ] Validate PT compliance → COMPLIANT ✓
- [ ] Compare v1.0 vs v1.1 → diff visible ✓
- [ ] Export PDF → profesional ✓
- [ ] Import Excel (5 rows) → success ✓

---

## 7️⃣ COMUNICACIÓN & ENTREGABLES

**Commits Format**:
- `feat: Implement VersionManager with snapshots and restore`
- `feat: Implement ComplianceValidator for PT/IT/ES`
- `feat: Implement LegalAlerts Vue component`
- `test: Add 80+ tests for backend managers`
- `docs: Add complete API documentation`

**PR Guidelines**:
- 1-2 features per PR (pequeños)
- Tests included en cada PR
- Update PROJECT_STATUS.md after each session

**Deliverables**:
1. ✅ GitHub repo con código completado
2. ✅ 150+ backend tests (80%+ coverage)
3. ✅ 50+ frontend tests (70%+ coverage)
4. ✅ E2E 5 flows passing
5. ✅ README + API docs + Architecture docs
6. ✅ Docker compose + CI/CD configured
7. ✅ MVP 100% funcional (create, translate, validate, export, import, versions, images)

---

## 8️⃣ ROADMAP FUTURO (Post MVP)

**Phase 3 (Semanas 9-12)**:
- Multi-user con roles (Admin/Editor/Traductor/Revisor)
- Comentarios en fichas + workflow aprobación
- WebSocket notifications real-time
- Redis caching

**Phase 4 (Q1 2026)**:
- API pública con rate limiting + OAuth2
- Soporte Francia, Alemania, UK
- Webhooks para integraciones ERP

**Phase 5+ (Q2-Q4 2026)**:
- Traducción automática GPT-4 integration
- IA suggestions compliance
- OCR imágenes
- SaaS cloud AWS/Azure
- App móvil iOS/Android

---

**ESTADO FINAL**: MVP 100% prototipado en 4 FASES = 40-50 horas. Backend Core complete. Frontend MVP functional. Testing 80%+ coverage. Documentation complete. Ready for real client deployment Q1 2026.

**Última Actualización**: 16 Diciembre 2025 | **Versión**: 1.0.0 | **Status**: Ready for Agent Implementation