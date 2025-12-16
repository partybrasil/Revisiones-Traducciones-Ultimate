---
name: Revisiones_Traducciones_Ultimate_Perplexity_Agent
description: |
    Eres el Ingeniero Senior de Prototipado responsable de completar Revisiones-Traducciones-Ultimate: una plataforma web centralizada que gestiona fichas de producto (catalogación, traducción multidioma, validación regulatoria, versionado con snapshots, importación/exportación masiva) para distribuidores/fabricantes europeos (Portugal, Italia, España).
version: 1.0.0
enabled: true
---

# 🚀 REVISIONES-TRADUCCIONES-ULTIMATE | GitHub Copilot Agent Complete Prompt

**Versión**: 1.0.0 | **Fecha**: 16 Diciembre 2025 | **Estado**: Prototipado 65% - Ready for Phase 2 Completion

---

## 📋 RESUMEN EJECUTIVO PARA EL AGENTE

Eres el **Ingeniero Senior de Prototipado** responsable de completar **Revisiones-Traducciones-Ultimate**: una plataforma web centralizada que gestiona fichas de producto (catalogación, traducción multidioma, validación regulatoria, versionado con snapshots, importación/exportación masiva) para distribuidores/fabricantes europeos (Portugal, Italia, España).

**Estado Actual**: El backend FastAPI está 70% completo pero con BRECHAS CRÍTICAS. El frontend Vue.js está en fase temprana. Los módulos de traducción, validación legal, versionado granular y scraping de imágenes NO están implementados.

**Tu Misión**: Completar el prototipo funcional en **4 FASES SECUENCIALES** (40-50 horas de trabajo concentrado):
1. **Auditoría & Diagnosis** (2h): Revisar estado actual, identificar gaps.
2. **Backend Core Completion** (16h): Terminar managers faltantes (Version, Compliance, Translation, ImageScraper).
3. **Frontend MVP Integration** (18h): Conectar componentes, crear vistas principales funcionales.
4. **Testing & Documentation** (8h): Tests unitarios, E2E, README, API docs.

---

## 1️⃣ CONTEXTO TÉCNICO ARQUITECTÓNICO

### 1.1 Stack Elegido (Justificado)

**Backend**: Python FastAPI + SQLAlchemy + PostgreSQL
- **Por qué**: Desarrollo rápido, type hints nativos, documentación automática OpenAPI, excelente para prototipado empresarial.
- **Performance**: AsyncIO, validación pydantic automática, índices DB optimizados.
- **Escalabilidad**: Fácil migración a microservicios, API RESTful estándar.

**Frontend**: Vue.js 3 + Vite + Pinia + Tailwind CSS
- **Por qué**: Reactividad elegante, DX superior, bundling instantáneo, state management centralizado.
- **Performance**: Tree-shaking automático, lazy loading components, CSS purging.
- **Escalabilidad**: Composables reutilizables, modular component hierarchy.

**Persistencia**: PostgreSQL + JSON columns
- **Por qué**: ACID compliance para auditoría, soporte native JSON (JSONB) para modelos polimórficos.
- **Indexación**: UNIQUE(sku), INDEX(family, status, created_date) optimizados.

---

## 2️⃣ ARQUITECTURA ACTUAL - ESTADO DETALLADO

### 2.1 Backend: LO QUE EXISTE ✅

```
backend/
├── main.py ✅ (FastAPI app, routes básicas CRUD)
├── requirements.txt ✅ (Dependencias core)
├── models/ ✅ 
│   ├── __init__.py
│   ├── product.py ✅ (ProductSheet model básico)
│   └── version.py ⚠️ (Estructura sin lógica)
├── routes/
│   ├── products.py ✅ (GET/POST/PUT/DELETE básicos)
│   └── versions.py ❌ (NO IMPLEMENTADO)
├── core/
│   ├── __init__.py
│   ├── product_sheet_manager.py ✅ (CRUD base funcional)
│   ├── version_manager.py ❌ (CRÍTICO - NO IMPLEMENTADO)
│   └── preset_manager.py ❌ (CRÍTICO - NO IMPLEMENTADO)
├── legal_framework/ ❌ (CARPETA VACÍA)
│   ├── compliance_validator.py ❌ (NO IMPLEMENTADO)
│   └── rules/ (YAML rules faltando)
├── translations/ ❌ (CARPETA VACÍA)
│   ├── translation_engine.py ❌ (NO IMPLEMENTADO)
│   ├── translation_memory.json ❌ (VACÍO)
│   └── glossaries/ ❌ (FALTANDO)
├── import_export/ ❌ (CARPETA VACÍA)
│   ├── import_export_manager.py ❌ (NO IMPLEMENTADO)
│   └── excel_template_generator.py ❌ (NO IMPLEMENTADO)
└── image_handler/ ❌ (CARPETA VACÍA)
    ├── image_scraper.py ❌ (NO IMPLEMENTADO)
    └── image_storage.py ❌ (NO IMPLEMENTADO)
```

### 2.2 Frontend: LO QUE EXISTE ✅

```
frontend/
├── src/
│   ├── App.vue ✅ (Estructura básica, Router definido)
│   ├── main.js ✅ (Vite entry)
│   ├── router/ ✅ (Rutas definidas)
│   │   └── index.js ✅ (Dashboard, Catalog, Create, etc.)
│   ├── stores/ ⚠️ (Pinia store structure pero vacío)
│   │   └── productStore.js ⚠️ (State pero sin actions/getters)
│   ├── components/
│   │   ├── Dashboard.vue ✅ (Stats placeholders)
│   │   ├── CatalogView.vue ✅ (Grid layout básico)
│   │   ├── ProductCard.vue ✅ (Display simple)
│   │   ├── ProductSheetEditor.vue ⚠️ (9 tabs pero inputs sin binding)
│   │   ├── LegalAlerts.vue ❌ (NO IMPLEMENTADO)
│   │   ├── VersionHistory.vue ❌ (NO IMPLEMENTADO)
│   │   ├── DiffViewer.vue ❌ (NO IMPLEMENTADO)
│   │   └── ImportExport.vue ❌ (NO IMPLEMENTADO)
│   ├── services/
│   │   ├── apiClient.js ⚠️ (Axios setup pero sin interceptors)
│   │   ├── productService.js ⚠️ (Métodos pero no conectados)
│   │   ├── versionService.js ❌ (NO IMPLEMENTADO)
│   │   ├── legalService.js ❌ (NO IMPLEMENTADO)
│   │   ├── importExportService.js ❌ (NO IMPLEMENTADO)
│   │   └── imageService.js ❌ (NO IMPLEMENTADO)
│   └── assets/
│       ├── tailwind.css ✅ (Configurado)
│       └── design-system.css ✅ (Colores/tipografía)
├── tailwind.config.js ✅
├── vite.config.js ✅
└── package.json ✅
```

### 2.3 Documentación & Config

```
├── README.md ⚠️ (Incompleto, falta arquitectura)
├── PROJECT_STATUS.md ⚠️ (Desactualizado)
├── QUICKSTART.md ⚠️ (Falta setup real)
├── docker-compose.yml ❌ (NO IMPLEMENTADO)
├── .github/workflows/ci.yml ❌ (NO IMPLEMENTADO)
└── CONTRIBUTING.md ⚠️ (Template vacío)
```

---

## 3️⃣ BRECHA CRÍTICA #1: BACKEND MANAGERS (16 HORAS)

### 3.1 VersionManager - Sistema de Snapshots COMPLETO

**Archivo**: `backend/core/version_manager.py` | **Est. Líneas**: 400-500 LOC | **Criticidad**: 🔴 CRÍTICA

**Métodos Requeridos**:

1. `create_snapshot(sku: str, version_type: str, change_summary: str) → dict`
   - Obtener estado ACTUAL de ProductSheet desde DB
   - Calcular version_number automático: "1.0" → "1.1" (minor) o "2.0" (major)
   - Serializar COMPLETO el estado en JSONB (complete_snapshot)
   - Comparar con versión anterior usando calculate_diff()
   - Crear N registros ProductChangelog (uno por change)
   - Actualizar products.current_version
   - Retornar {sku, version_number, changes_count, critical_changes, timestamp}

2. `calculate_diff(old_state: dict, new_state: dict) → List[dict]`
   - Recorrer TODOS los campos (flatten_dict recursiva)
   - Para cada campo diferente: determinar change_type (added/updated/deleted)
   - Calcular severity: "critical" si es campo crítico PT/IT/ES, else "important"/"minor"
   - Retornar sorted by severity DESC, timestamp
   - Ejemplo output: `[{field_path: "title_short.pt", old_value: null, new_value: "Crema", change_type: "added", severity: "critical"}, ...]`

3. `get_snapshot(sku: str, version: str) → dict`
   - Query product_versions tabla
   - Desserializar complete_snapshot JSONB
   - Retornar estado COMPLETO en ese momento

4. `compare_versions(sku: str, v_from: str, v_to: str) → dict`
   - Obtener snapshots de ambas versiones
   - Aplicar calculate_diff()
   - Retornar {stats: {added: 3, updated: 5, deleted: 0}, changes: [...], from_version, to_version}

5. `get_timeline(sku: str) → List[dict]`
   - Query product_versions ORDER BY snapshot_date DESC
   - Retornar lista con {version_number, snapshot_date, created_by, change_summary, status}

6. `restore_version(sku: str, version: str) → dict`
   - Obtener complete_snapshot de ProductVersion
   - UPDATE tabla products SET ALL FIELDS FROM snapshot
   - Crear nueva versión v3.0 (major) con change_summary="Restored from vX.Y"
   - Retornar nueva ficha actualizada

**Integración con SQLAlchemy**:
- Usar `session.query(ProductVersion).filter_by(sku=sku).order_by(ProductVersion.snapshot_date.desc()).first()`
- JSONB operations: `ProductVersion.complete_snapshot` es dict nativo en Python
- Transaction management: `with Session() as session: ... session.commit()`

**Test Coverage**:
- ✅ test_create_snapshot_incremental_version: "1.0" → "1.1"
- ✅ test_calculate_diff_with_critical_fields: severity "critical" para PT/IT/ES fields
- ✅ test_compare_versions_with_multiple_changes: 10+ cambios diferentes
- ✅ test_restore_version_reverts_to_previous_state: ProductSheet restore completo

---

### 3.2 ComplianceValidator - Validación Regulatoria COMPLETA

**Archivo**: `backend/legal_framework/compliance_validator.py` | **Est. Líneas**: 350-450 LOC | **Criticidad**: 🔴 CRÍTICA

**Métodos Requeridos**:

1. `__init__(self)`
   - Cargar YAML rules desde `backend/legal_framework/rules/`:
     - `portugal_rules.yaml` (INFARMED)
     - `italy_rules.yaml` (Ministero della Salute)
     - `spain_rules.yaml` (AEMPS)
   - Parsear estructura: `country_legal_framework → regulations → critical_requirements array`
   - Indexar rules por (country, family, field_name) para O(1) lookup

2. `validate_for_country(sheet: ProductSheet, country: str) → dict`
   - Obtener reglas críticas para el country y family de la ficha
   - Iterar TODOS critical_requirements:
     - Si `translation_mandatory=true`: verificar que el campo en ese idioma NO esté vacío
     - Si `translation_mandatory=false`: solo verificar que exista
   - Compilar lista de campos faltantes en critical_issues
   - Calcular completion_percentage: (campos_válidos / campos_críticos) * 100
   - Retornar {status: "COMPLIANT"/"NON_COMPLIANT"/"WARNING", percentage: int, critical_issues: List[str], warnings: List[str]}

3. `validate_field(field_name: str, value: any, country: str, family: str) → bool`
   - Lookup rule para (country, family, field_name)
   - Aplicar validaciones específicas:
     - INCI: debe ser lista INCI válida (búsqueda en INCI database o simple no-empty)
     - Alérgenos: máximo 14 específicos UE 1169/2011
     - Title: min 3 chars, max 200, no caracteres especiales peligrosos
     - Warnings: min 10 chars, max 1000
   - Retornar True si pasa, False si falla

4. `get_critical_missing(sheet: ProductSheet, country: str) → List[dict]`
   - Retornar lista de campos CRÍTICOS faltantes con format:
     - `{field_name, field_display_name, error_message, example, severity: "🔴 CRÍTICO"}`

5. `calculate_compliance_percentage(sheet: ProductSheet, country: str) → int`
   - Validar todos critical_requirements
   - Retornar 0-100 como porcentaje

6. `get_critical_fields_by_country(country: str, family: str) → List[str]`
   - Helper que retorna lista de field names críticos para ese country/family

**YAML Rules Structure** (crear estos 3 archivos):

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
          example: "Crema Hidratante Facial 24h"
        - field: "description_detailed_pt"
          name: "Descrição Detalhada PT"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Descrição completa em português"
          error_message: "A descrição em português é obrigatória"
          example: "Creme facial hidratante..."
        - field: "inci_ingredients_pt"
          name: "Ingredientes INCI PT"
          translation_mandatory: false
          severity: "🔴 CRÍTICO"
          description: "Lista INCI completa (idioma no importa)"
          error_message: "INCI ausente"
          example: "WATER, GLYCERIN, PHENOXYETHANOL"
        - field: "allergens_pt"
          name: "Alérgenos Declarados PT"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "14 alérgenos UE 1169/2011"
          error_message: "Declaração de alérgenos obrigatória"
          example: "Contém: Amendoim. Pode conter: Frutos de casca rija"
        - field: "mode_of_use_pt"
          name: "Modo de Emprego PT"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Instruções de uso em português"
          error_message: "Instruções de uso ausentes"
          example: "Aplicar pequena quantidade na face limpa"
        - field: "warnings_pt"
          name: "Avisos PT"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Avisos e precauções em português"
          error_message: "Avisos obrigatórios ausentes"
          example: "Evitar contacto com olhos. Usar protetor solar."
        - field: "pao_symbol"
          name: "Símbolo PAO"
          translation_mandatory: false
          severity: "🔴 CRÍTICO"
          description: "Período após abertura (6M, 12M, 18M, 24M, 36M)"
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
          description: "Percentagem de ingredientes de origem natural"
          example: "92% de ingredientes de origem natural"

# Repetir para ITALY y SPAIN con sufijos _it, _es
```

**Integración con ProductSheet**:
- Acceder a campos vía: `sheet.title_short_pt`, `sheet.description_detailed_pt`, etc.
- JSON multiidioma estructura: `sheet.title_short = {"es": "Crema", "pt": "Creme", "it": "Crema"}`
- Validar existencia: `if sheet.title_short.get("pt"): ...`

**Test Coverage**:
- ✅ test_cosmetics_facial_portugal_compliant: Ficha válida retorna COMPLIANT, 100%
- ✅ test_cosmetics_facial_portugal_missing_critical: Falta title_pt retorna NON_COMPLIANT
- ✅ test_inci_validation_strict: INCI debe contener palabras válidas
- ✅ test_allergens_14_eu_validation: Solo alérgenos UE permitidos
- ✅ test_multi_country_validation: Misma ficha validada PT/IT/ES

---

### 3.3 PresetManager - Auto-Fill INTELIGENTE

**Archivo**: `backend/core/preset_manager.py` | **Est. Líneas**: 250-300 LOC | **Criticidad**: 🟡 IMPORTANTE

**Métodos Requeridos**:

1. `__init__(self)`
   - Cargar presets YAML desde `backend/presets/150_families.yaml`
   - Crear índice by family_code para O(1) lookup

2. `load_preset(family: str) → dict`
   - Retornar preset completo: {family, display_name, mode_of_use_es/pt/it, warnings_es/pt/it, typical_allergens, pao_default, fields_to_autofill}

3. `apply_preset(sheet: ProductSheet, family: str) → ProductSheet`
   - Cargar preset
   - Aplicar valores por defecto a campos vacíos (NO sobrescribir si existen):
     - `sheet.mode_of_use_es = preset.mode_of_use_es if not sheet.mode_of_use_es else sheet.mode_of_use_es`
     - `sheet.warnings_es = preset.warnings_es if not sheet.warnings_es else sheet.warnings_es`
     - `sheet.allergens_present = preset.typical_allergens if not sheet.allergens_present else sheet.allergens_present`
     - `sheet.pictograms = preset.typical_pictograms if not sheet.pictograms else sheet.pictograms`
     - `sheet.pao = preset.pao_default if not sheet.pao else sheet.pao`
   - Retornar sheet actualizado

4. `get_available_families() → List[dict]`
   - Retornar lista de TODAS las familias: `[{code: "COSMETICS_FACIAL", display_name: "Cosméticos Faciales", subfamily_count: 12}, ...]`

5. `get_preset_fields(family: str) → dict`
   - Retornar structure: {autofillable_fields: [...], suggested_values: {...}, allergen_examples: [...], pictogram_examples: [...]}

**Presets YAML** (crear `backend/presets/150_families.yaml` con estructura base):

```yaml
presets:
  COSMETICS_FACIAL:
    display_name: "Cosméticos Faciales"
    subfamily: ["Cremas Hidratantes", "Sérums", "Máscaras", "Limpiadoras"]
    mode_of_use_es: "Aplicar pequeña cantidad en la cara limpia y masajear suavemente hasta absorción completa."
    mode_of_use_pt: "Aplicar pequena quantidade no rosto limpo e massajear suavemente até absorção completa."
    mode_of_use_it: "Applicare una piccola quantità sul viso pulito e massaggiare delicatamente fino al completo assorbimento."
    warnings_es: "Uso externo. Evitar contacto con los ojos. Si es irritante, suspender el uso. Mantener fuera del alcance de los niños."
    warnings_pt: "Uso externo. Evitar contacto com os olhos. Se irritante, suspender o uso. Manter fora do alcance das crianças."
    warnings_it: "Uso esterno. Evitare il contatto con gli occhi. Se irritante, sospendere l'uso. Tenere fuori dalla portata dei bambini."
    typical_allergens:
      - "PARFUM (Fragancia)"
      - "LIMONENE"
      - "BENZYL ALCOHOL"
    typical_pictograms:
      - "skin_irritation"
      - "eye_irritation"
    pao_default: "12M"
    natural_origin_range: "50-100%"

  FOOD_PACKAGED:
    display_name: "Alimentos Empaquetados"
    subfamily: ["Snacks", "Bebidas", "Conservas", "Congelados"]
    mode_of_use_es: "Almacenar en lugar fresco y seco. Consumir preferentemente antes de la fecha indicada."
    warnings_es: "Puede contener trazas de frutos secos, trigo, soja. No apto para celíacos."
    typical_allergens:
      - "Gluten"
      - "Frutos de cáscara"
      - "Soja"
    pao_default: "24M"
    typical_pictograms: []

  # ... 148 families más (estructura similar)
```

---

### 3.4 TranslationEngine - Motor de Sugerencias MULTIIDIOMA

**Archivo**: `backend/translations/translation_engine.py` | **Est. Líneas**: 300-400 LOC | **Criticidad**: 🟡 IMPORTANTE

**Métodos Requeridos**:

1. `__init__(self)`
   - Cargar translation_memory.json (dict vacío si no existe)
   - Cargar glossaries desde `backend/translations/glossaries/glossary_*.yaml` (PT, IT, EN, FR, BR)
   - Inicializar fuzzy matcher (usar `difflib.get_close_matches` o `fuzzywuzzy`)

2. `suggest_translation(source_text: str, source_lang: str, target_lang: str, threshold: float = 0.75) → List[str]`
   - Buscar en translation_memory si existe exact o similar
   - Si confidence > threshold, retornar sugerencia
   - Aplicar glossary terms: si source_text contiene keywords del glossary, retornar traducción glossary
   - Ejemplo: source="Crema Hidratante" → suggest_translation("es", "pt") → ["Creme Hidratante", "Creme Moisturizer"]
   - Retornar máx 5 sugerencias

3. `save_translation(source_text: str, target_text: str, source_lang: str, target_lang: str)`
   - Guardar en translation_memory.json: `{f"{source_lang}-{target_lang}": {source_text: [target_text, count: 1, timestamp]}}`
   - Increment count si ya existe
   - Persist en file

4. `get_glossary(family: str, target_lang: str) → dict`
   - Cargar glossary_COSMETICS_pt.yaml
   - Retornar dict: `{key_term_es: translation_pt, ...}`

5. `load_translation_memory(filepath: str = "backend/translations/translation_memory.json")`
   - Parse JSON, validar estructura
   - Retornar dict

6. `export_memory_to_csv(output_path: str)`
   - Exportar translation_memory a CSV: source_text, target_text, source_lang, target_lang, count, confidence

**Translation Memory Initial** (crear `backend/translations/translation_memory.json`):

```json
{
  "es-pt": {
    "Crema Hidratante": ["Creme Hidratante", 1],
    "Modo de Empleo": ["Modo de Emprego", 1],
    "Advertencia": ["Aviso", 1]
  },
  "es-it": {
    "Crema Hidratante": ["Crema Idratante", 1],
    "Aviso": ["Avvertenza", 1]
  }
}
```

**Glossaries** (crear `backend/translations/glossaries/`):

```yaml
# glossary_cosmetics_pt.yaml
COSMETICS_FACIAL:
  "Crema Hidratante": "Creme Hidratante"
  "Sérum": "Sérum"
  "Máscara": "Máscara"
  "Limpiadora": "Limpadora"
  "Fluorescente": "Fluorescente"
  "Modo de Empleo": "Modo de Emprego"

FOOD_PACKAGED:
  "Alérgeno": "Alergénio"
  "Sin Gluten": "Sem Glúten"
  "Conservante": "Conservante"
```

---

### 3.5 ImportExportManager - Operaciones MASIVAS

**Archivo**: `backend/import_export/import_export_manager.py` | **Est. Líneas**: 400-500 LOC | **Criticidad**: 🔴 CRÍTICA

**Métodos Requeridos**:

1. `generate_excel_template() → bytes`
   - Usar `openpyxl` library
   - Crear Excel con 60+ columnas predefindas:
     - Row 1: Headers (SKU, EAN_PRIMARY, EAN_SECONDARY, TITLE_ES_SHORT, TITLE_PT_SHORT, TITLE_IT_SHORT, BRAND, GAMA_ES, FAMILY, SUBFAMILY, NET_WEIGHT, NET_WEIGHT_UNIT, FORMAT_TYPE, FORMAT_MATERIAL, FORMAT_CLOSURE, INCI_INGREDIENTS, MODE_OF_USE_ES, WARNINGS_ES, PAO, ALLERGENS, PICTOGRAMS, etc.)
     - Row 2: Ejemplos (CF-HYD-001, 5412345678901, , "Crema Hidratante", "Creme Hidratante", "Crema Idratante", "MiMarca", "Facial", "COSMETICS_FACIAL", "Cremas", 50, "ml", "Botella", "Plástico", "Rosca", "WATER, GLYCERIN...", "Aplicar...", "Evitar...", "12M", "Fragancia, Limoneno", "Skin Irritation", ...)
     - Datavalidation dropdowns para FAMILY (150 opciones), FORMAT_TYPE, PAO
     - Color-coding: Headers críticos en rojo, recomendados en amarillo, opcionales en gris
   - Retornar bytes (BytesIO)

2. `import_from_excel(file_path: str) → dict`
   - Leer Excel con openpyxl
   - Iterar filas (skip header+ejemplo):
     - Validar SKU no vacío
     - Validar EAN checksum (si existe)
     - Validar TITLE_ES no vacío
     - Validar FAMILY está en lista 150 familias
     - Si error: add a errors_list
     - Si válida: crear ProductSheet, aplicar preset via PresetManager, guardar en DB
   - Retornar {imported: int, errors: List[str], skipped: int, status: "SUCCESS"/"PARTIAL"/"FAILED", completion_percentage: int}

3. `export_to_pdf(sku: str) → bytes`
   - Usar ReportLab
   - Generar PDF A4 profesional:
     - Logo + Header (SKU, EAN, Brand, Gama)
     - 2 columnas: General Info | Metadata (Made In, Responsible Person con flags 🇵🇹🇮🇹🇪🇸)
     - Tabla Physical Properties (Dimension, Weight, Format, Material)
     - Tabla Composition (INCI list)
     - Modo de Uso (multi-idioma justified)
     - Warnings en box rojo con ⚠️
     - Pictogramas como imágenes SVG pequeñas
     - Product Images (3 fotos centradas con captions)
     - Footer compliance badges (PT ✓, IT ✓, ES ⚠️)
   - Retornar bytes (BytesIO)

4. `export_to_markdown(sku: str) → str`
   - Generar .md estructurado:
     - `# Ficha: {sku}`
     - `## Información General`
     - Tabla metadata
     - `## Composición INCI`
     - Lista
     - `## Modo de Empleo`
     - Multi-idioma (ES, PT, IT)
     - `## Avisos`
     - `## Cumplimiento Regulatorio`
   - Retornar string

5. `export_to_html(sku: str) → str`
   - Generar HTML profesional (style inline)
   - Structure similar a markdown pero con CSS styling

6. `export_catalog_excel(filters: dict) → bytes`
   - Aplicar filtros: {family: str, brand: str, status: str, created_after: date}
   - Generar Excel con N productos (uno por row, template misma que import)
   - Retornar bytes

**Test Coverage**:
- ✅ test_excel_template_has_60_columns: Validate column count
- ✅ test_excel_import_with_valid_data: 10 productos válidos importan exitosamente
- ✅ test_excel_import_with_invalid_ean: EAN checksum validation falla
- ✅ test_pdf_export_includes_all_sections: PDF tiene logo, metadata, composition, warnings, images
- ✅ test_markdown_export_multiidioma: ES, PT, IT presente

---

### 3.6 ImageScraper & ImageStorage - Gestión VISUAL

**Archivo**: `backend/image_handler/image_scraper.py` + `image_storage.py` | **Est. Líneas**: 250-300 LOC | **Criticidad**: 🟡 IMPORTANTE

**ImageScraper Methods**:

1. `search_images(query: str, max_results: int = 20) → List[dict]`
   - Usar `requests` + `beautifulsoup4` para web scraping (Google Images alternativa)
   - O usar API gratuita: Bing Images API, Unsplash API
   - Retornar: `[{url: str, title: str, source: str, resolution: tuple}, ...]`

2. `download_image(url: str, sku: str, image_type: str) → str`
   - Download image vía requests
   - Guardar en `backend/storage/images/{sku}/{image_type}/`
   - Validar format (JPG, PNG, WebP)
   - Retornar local file path

3. `validate_image(file_path: str) → bool`
   - Verificar formato válido (PIL.Image.open)
   - Verificar size < 10MB
   - Verificar resolution > 100x100px
   - Retornar True/False

4. `resize_image(file_path: str, max_width: int = 3000) → None`
   - Usar Pillow (PIL)
   - Resize manteniendo aspect ratio
   - Comprimir a 85% quality JPEG

**ImageStorage Methods**:

1. `save_uploaded_file(file: UploadFile, sku: str, image_type: str) → str`
   - Recibir file multipart
   - Validar vía validate_image()
   - Guardar en storage
   - Retornar path

2. `get_image_path(sku: str, image_type: str) → str`
   - Retornar full path a imagen

3. `delete_image(sku: str, image_type: str) → bool`
   - Delete file del filesystem
   - Update ProductSheet.product_images array
   - Retornar True si successful

**Storage Directory Structure**:
```
backend/storage/
└── images/
    ├── CF-HYD-001/
    │   ├── frontal/
    │   │   └── image_001.jpg
    │   ├── trasera/
    │   └── lateral/
    └── CF-VIT-001/
        └── frontal/
```

---

## 4️⃣ BRECHA CRÍTICA #2: FRONTEND COMPONENTS (18 HORAS)

### 4.1 Store Pinia - State Management COMPLETO

**Archivo**: `frontend/src/stores/productStore.js` (y otros stores) | **Est. Líneas**: 200-250 LOC **Criticidad**: 🔴 CRÍTICA

**State**:
```javascript
// productStore
{
  products: [],           // Cached list
  currentProduct: null,   // Editing product
  loading: false,
  error: null,
  filters: {
    family: "",
    brand: "",
    status: "all",      // draft/in_review/approved/published
    languages: [],      // ES, PT, IT, EN, FR, BR
    search: ""
  },
  pagination: {
    page: 1,
    per_page: 20,
    total: 0
  }
}

// versionStore
{
  versions: [],          // [v1.0, v1.1, v2.0, ...]
  currentVersion: null,
  changelog: [],         // Changes in current version
  diff: {
    from_version: null,
    to_version: null,
    changes: []          // [{field, old, new, change_type, severity}, ...]
  }
}

// legalStore
{
  countries: ["PT", "IT", "ES"],
  complianceStatus: {    // {country: {status, percentage, issues}}
    PT: { status: "COMPLIANT", percentage: 95, issues: [] },
    IT: { status: "NON_COMPLIANT", percentage: 60, issues: [{field, error_message}] },
    ES: { status: "WARNING", percentage: 75, issues: [] }
  },
  rules: {}              // {country: {family: {critical_requirements: [], optional_requirements: []}}}
}

// uiStore
{
  darkMode: false,
  sidebarOpen: true,
  notifications: [],     // [{id, type, message, timestamp}]
  modals: {
    showImportDialog: false,
    showExportDialog: false,
    showConfirmDelete: false,
    showVersionRestore: false
  }
}
```

**Actions**:
```javascript
// productStore
- fetchProducts(filters?, pagination?)      // GET /api/products
- getProduct(sku)                           // GET /api/products/{sku}
- createProduct(data)                       // POST /api/products
- updateProduct(sku, data)                  // PUT /api/products/{sku}
- deleteProduct(sku)                        // DELETE /api/products/{sku}
- searchProducts(query)                     // GET /api/products/search?q=query
- setCurrentProduct(product)
- setFilters(filters)

// versionStore
- fetchVersions(sku)                        // GET /api/products/{sku}/versions
- getSnapshot(sku, version)                 // GET /api/products/{sku}/versions/{version}
- compareVersions(sku, v_from, v_to)       // GET /api/products/{sku}/versions/compare
- restoreVersion(sku, version)              // POST /api/products/{sku}/versions/{version}/restore
- setCurrentVersion(version)

// legalStore
- fetchRules(country)                       // GET /api/legal/{country}/rules
- validateCompliance(sku, country)          // POST /api/legal/validate
- getComplianceStatus(sku)                  // GET /api/products/{sku}/compliance
- setComplianceStatus(status)

// uiStore
- addNotification(type, message)
- removeNotification(id)
- toggleDarkMode()
- toggleSidebar()
- openModal(modalName)
- closeModal(modalName)
```

**Getters**:
```javascript
// productStore
- getProductBySku(sku)
- getFilteredProducts()
- getProductCount()
- isLoading
- hasError

// versionStore
- getCurrentVersionNumber()
- getTotalVersions()
- hasMultipleVersions()

// legalStore
- getCompliancePercentage(country)
- getComplianceStatus(country)
- getCountriesCompliant()
```

---

### 4.2 Services API - Integración Backend COMPLETA

**Archivos**: `frontend/src/services/*` | **Est. Líneas**: 50-100 LOC por service | **Criticidad**: 🔴 CRÍTICA

**productService.js**:
```javascript
// Métodos
- createSheet(data): POST /api/products
- getSheet(sku): GET /api/products/{sku}
- updateSheet(sku, data): PUT /api/products/{sku}
- deleteSheet(sku): DELETE /api/products/{sku}
- listSheets(filters, pagination): GET /api/products?...
- searchSheets(query): GET /api/products/search?q=query
```

**versionService.js**:
```javascript
- getVersions(sku): GET /api/products/{sku}/versions
- getSnapshot(sku, version): GET /api/products/{sku}/versions/{version}
- compareVersions(sku, v_from, v_to): GET /api/products/{sku}/versions/compare
- restoreVersion(sku, version): POST /api/products/{sku}/versions/{version}/restore
```

**legalService.js**:
```javascript
- getCountryRules(country): GET /api/legal/{country}/rules
- validateCompliance(sku, country): POST /api/legal/validate {sku, country}
- getComplianceStatus(sku): GET /api/products/{sku}/compliance
```

**importExportService.js**:
```javascript
- getTemplateExcel(): GET /api/import/template (returns blob)
- importExcel(file): POST /api/import/excel (multipart)
- exportPDF(sku): GET /api/export/pdf/{sku} (returns blob)
- exportMarkdown(sku): GET /api/export/markdown/{sku}
- exportHTML(sku): GET /api/export/html/{sku}
- exportCatalogExcel(filters): GET /api/export/catalog-excel?... (returns blob)
```

**imageService.js**:
```javascript
- searchImages(query): GET /api/images/search?q=query
- uploadImage(sku, imageType, file): POST /api/images/upload
- getImage(sku, imageType): GET /api/images/{sku}/{imageType}
- deleteImage(sku, imageType): DELETE /api/images/{sku}/{imageType}
```

**apiClient.js Configuration**:
```javascript
// Interceptors necesarios
- Request: Add Authorization header si existe token
- Request: Set Content-Type: application/json automáticamente
- Response: Si 401, redirigir a login
- Response: Si 4xx/5xx, dispatch error notification
- Response: Auto-retry en 503 con exponential backoff
```

---

### 4.3 Componentes Vue Faltantes

**Criticidad**: 🔴 CRÍTICA | **Total Líneas**: 1500-2000 LOC en todos

#### 4.3.1 LegalAlerts.vue

**Ubicación**: `frontend/src/components/LegalAlerts.vue` | **Est. Líneas**: 200-250

**Estructura**:
- 3 country cards en grid (PT/IT/ES con flags 🇵🇹🇮🇹🇪🇸)
- Card content:
  - Country name + flag + authority name
  - Status badge: 🔴 (NON_COMPLIANT), 🟡 (WARNING), 🟢 (COMPLIANT)
  - Compliance percentage (0-100%) con progress bar
  - Botón "Ver Detalles" → expandible con lista critical_issues
  - Si status=NON_COMPLIANT: highlight rojo, lista 5+ campos faltantes con error messages
  - Si status=WARNING: highlight amarillo, 2-3 warnings
  - Si status=COMPLIANT: highlight verde, checkmark

**Props**:
- `sku: string` (ProductSheet ID)

**Methods**:
- `computed compliance = versionStore.complianceStatus[country]`
- `toggleExpanded(country)`
- `watch sku: async validate compliance for all 3 countries`

**Lifecycle**:
- `onMounted`: Fetch compliance via `legalService.getComplianceStatus(sku)`

---

#### 4.3.2 VersionHistory.vue

**Ubicación**: `frontend/src/components/VersionHistory.vue` | **Est. Líneas**: 250-300

**Estructura**:
- Timeline vertical con conectores:
  - v2.3 (Current) → azul dot + connecting line
  - v2.2 (Archived) → gris dot + connecting line
  - v2.1 (Archived) → gris dot
- Cada versión:
  - Version number (v2.3)
  - Date + time (16 Dic 2025, 14:35)
  - Change summary (hasta 80 chars)
  - Author avatar + name (si existe)
  - Botones: "Ver Snapshot", "Comparar", "Restaurar" (solo si archived)
- Card expandible:
  - Click "Ver Snapshot" → muestra changes_array field by field
  - Format: `Field Name: old_value → new_value (severity_badge)`

**Props**:
- `sku: string`

**Data**:
- `versions: []` (sorted DESC by date)
- `expandedVersion: null`

**Methods**:
- `fetchVersions(sku)`: Call `versionService.getVersions(sku)` → update state
- `compareVersions(v1, v2)`: Open DiffViewer modal
- `restoreVersion(version)`: Confirm dialog → POST /api/products/{sku}/versions/{v}/restore → show success toast

**Lifecycle**:
- `onMounted`: `fetchVersions(sku)`

---

#### 4.3.3 DiffViewer.vue

**Ubicación**: `frontend/src/components/DiffViewer.vue` | **Est. Líneas**: 300-350

**Estructura**:
- 2 selectores horizontales (De | A):
  - Dropdown v1: [v1.0, v1.1, v2.0, ...] (sorted DESC)
  - Dropdown v2: [v1.1, v2.0, ...] (sorted DESC, default = current)
  - Botón "Comparar" (o auto-compare on change)
- Stats row: "3 Added | 2 Updated | 0 Deleted"
- Changes grid (3 columns: Field | Old Value | New Value):
  - Cada row:
    - ✚ badge verde si "added"
    - ~ badge amarillo si "updated"
    - ✗ badge rojo si "deleted"
    - Field name (bold)
    - Old value (gris si null)
    - New value (negrita)
    - Highlight inline si strings (fondo amarillo en diff parts)
  - Ejemplo row: `| ✚ title_short.pt | — | Crema Hidratante |`
  - Ejemplo row: `| ~ mode_of_use_es | Aplicar... | Aplicar pequeña cantidad... |`

**Props**:
- `sku: string`
- `v_from: string` (default = previous version)
- `v_to: string` (default = current)

**Data**:
- `changes: []`
- `stats: {added, updated, deleted}`
- `loading: false`

**Methods**:
- `compare()`: Call `versionService.compareVersions(sku, v_from, v_to)` → update changes/stats
- `restoreFrom(version)`: Confirm → Call `versionService.restoreVersion(sku, version)`

**Computed**:
- `changesGroupedBySeverity()`: Sort changes by severity (critical → important → minor)
- `isCurrentVersionTarget()`: v_to === current_version

---

#### 4.3.4 ImportExport.vue

**Ubicación**: `frontend/src/components/ImportExport.vue` | **Est. Líneas**: 350-400

**Estructura**:
- 2 tabs: "Importar" | "Exportar"

**TAB 1 - IMPORTAR**:
- Área drag-and-drop o file input
  - Accept: .xlsx
  - Texto: "Arrastra Excel aquí o click para seleccionar"
  - Botón "Descargar Template" → GET /api/import/template → trigger download
- Progress bar + log area mientras se importa
- Post-import status:
  - "✓ 23 productos importados"
  - "❌ 2 errores (ver detalles)"
  - Tabla errores: Row number | SKU | Error message
  - Botón "Ver Completitud" → abrir modal con stats (156/223 campos, 67 pendientes)

**TAB 2 - EXPORTAR**:
- Format selector (radio buttons):
  - ☐ PDF (Ficha individual, bonito)
  - ☐ Excel (Plantilla 60+ columnas)
  - ☐ Markdown (Formato texto)
  - ☐ HTML (Formato web)
  - ☐ Catálogo Masivo Excel
- Si "Catálogo Masivo":
  - Filters: Family, Brand, Status, Date range
  - Botón "Descargar {N} productos"
- Si individual:
  - Input SKU o dropdown (current product)
  - Botón "Exportar {format}"

**Methods**:
- `handleFileUpload(file)`: Validar .xlsx → POST /api/import/excel → show results
- `downloadTemplate()`: GET /api/import/template → trigger blob download
- `exportFormat(format, sku/filters)`: GET /api/export/{format} → trigger download
- `showImportDetails()`: Open modal con stats y log completo

---

#### 4.3.5 ProductSheetEditor.vue - Actualización COMPLETA

**Ubicación**: `frontend/src/components/ProductSheetEditor.vue` | **Est. Líneas**: 800-1000

**Issues Actuales**:
- ❌ Form inputs sin v-model binding
- ❌ No valida en real-time
- ❌ Tab structure presente pero contenido vacío
- ❌ No muestra compliance warnings
- ❌ No carga presets automático
- ❌ No integra ImageUpload
- ❌ No maneja traducción sugerencias

**Requerimientos Nuevos**:

1. **v-model Bindings Completos**:
   - Todos inputs deben estar bound a `currentProduct` store
   - Cambios deben ser tracked en real-time
   - Dirty flag para mostrar "Cambios sin guardar"

2. **Tabs Funcionales (9 tabs)**:
   - ✅ Tab 1: General (SKU, EAN, Title, Brand, Gama, Family)
   - ✅ Tab 2: Physical (Dimensions, Weight, Format, Material, Closure)
   - ✅ Tab 3: Packaging (Languages, Label positions)
   - ✅ Tab 4: Composition (INCI, Key Ingredients, Allergens)
   - ✅ Tab 5: Usage (Mode of Use, Application Area, Frequency)
   - ✅ Tab 6: Warnings (General, Specific, Storage)
   - ✅ Tab 7: Translation (Selector PT/IT + Editor for each language)
   - ✅ Tab 8: Images (Upload, Gallery, Drag-reorder)
   - ✅ Tab 9: Legal (Compliance cards para 3 países)

3. **Validaciones Real-Time**:
   - Character counter en cada textarea (red si > max)
   - Required field indicators (🔴 para critical)
   - EAN checksum validation
   - INCI validation (existencia en base INCI pública)
   - Min/max length warnings

4. **Preset Auto-Fill**:
   - Al seleccionar FAMILY: cargar preset vía PresetManager
   - Populate mode_of_use_es, warnings_es, allergens, etc.
   - Mostrar toast: "Preset cargado: X campos autollenados"
   - User puede clear/override

5. **Translation Tab**:
   - Language selector (dropdown PT, IT, EN, FR, BR)
   - Side-by-side: Original (ES) | Translation (selected lang)
   - Checklist de campos a traducir (con severity badges)
   - Al escribir en campo: mostrar sugerencias dropdown
   - Botón "Guardar Traducción" → POST /api/products/{sku}/translate

6. **Images Tab**:
   - Drag-and-drop upload area
   - Botón "Buscar en Web" → SearchImages component
   - Gallery grid con thumbs (3 columnas)
   - Cada imagen:
     - Type label (Frontal, Trasera, Lateral, etc.)
     - Delete button
     - Drag handle para reorder (stored en product_images order)
   - Upload progress bar

7. **Legal Tab**:
   - Embed LegalAlerts component
   - Mostrar compliance para 3 países
   - Si NON_COMPLIANT: highlight campos faltantes
   - "Auto-Fix" button para completar con defaults (si posible)

8. **Auto-Save**:
   - Debounce cambios por 2 segundos
   - PUT /api/products/{sku} en background
   - Show "Guardado" toast en success
   - Show "Error guardando" toast en failure

9. **Completion Percentage**:
   - Footer bar mostrando % completitud
   - Breakdown: General (25%), Composition (25%), Warnings (20%), Images (15%), Translation (15%)
   - Visual: progress bar con colores (rojo <50%, amarillo 50-75%, verde >75%)

---

### 4.4 Dashboard.vue - Stats FUNCIONALES

**Ubicación**: `frontend/src/components/Dashboard.vue` | **Est. Líneas**: 300-350

**Actualización Necesaria**:

1. **Stat Cards** (4 cards en grid):
   - Total Productos: valor + % cambio vs semana pasada (trend arrow)
   - Familias Activas: valor (pie chart de distribución)
   - Marcas: valor (word cloud preview)
   - Idiomas: (ES, PT, IT flags + %)

2. **Compliance Overview**:
   - 3 country cards (PT/IT/ES)
   - Cada una: banderu + % compliance + "X campos por completar"
   - Click → ir a LegalAlerts detail

3. **Recent Activity Timeline**:
   - Últimas 5 acciones (created, updated, exported, translated)
   - Format: "Usuario X creó Producto Y hace 2h"
   - Con avatars y timestamps

4. **Quick Actions**:
   - Botones: "+ Crear Ficha", "📤 Importar", "📥 Exportar"
   - Cada uno redirige a componente correspondiente

5. **Data Loading**:
   - `onMounted`: 
     - `productStore.fetchProducts()` (limit 5 para dashboard)
     - `legalStore.getComplianceStatus()` para 3 países
     - `versionStore.fetchVersions()` para activity timeline

---

### 4.5 CatalogView.vue - Filtros FUNCIONALES

**Ubicación**: `frontend/src/components/CatalogView.vue` | **Est. Líneas**: 350-400

**Actualización Necesaria**:

1. **Sidebar Filters** (izquierda):
   - Family dropdown (150 opciones, puede search typing)
   - Brand search (text input con autocomplete)
   - Status checkboxes (draft, in_review, approved, published)
   - Languages checkboxes (ES, PT, IT, EN, FR, BR con flags)
   - Date range picker (created desde-hasta)
   - Botón "Limpiar Filtros" (reset todo)

2. **Search Bar** (arriba):
   - Input con icono búsqueda
   - Placeholder: "Buscar por SKU, marca, titulo..."
   - `v-model` → `productStore.filters.search`
   - Debounce 500ms → trigger search

3. **Product Grid** (derecha):
   - Grid 4 columnas (responsive: 1 mobile, 2 tablet, 4 desktop)
   - ProductCard component por producto
   - Lazy load si scroll near bottom
   - Loading skeleton while fetching

4. **Pagination** (abajo):
   - Simple: Previous | Pages 1/N | Next
   - Per-page selector: 12, 20, 50
   - Total count: "Mostrando 1-20 de 248"

5. **State Management**:
   - watch filters → trigger API call
   - watch search query (debounce)
   - Handle loading/error states

---

## 5️⃣ RUTAS API BACKEND - Definición COMPLETA

**Criticidad**: 🔴 CRÍTICA | **Archivo**: `backend/routes/*.py`

**ProductSheet CRUD** (`/api/products`):
- `GET /api/products` → List with filters/pagination
- `POST /api/products` → Create new
- `GET /api/products/{sku}` → Get single
- `PUT /api/products/{sku}` → Update
- `DELETE /api/products/{sku}` → Delete
- `GET /api/products/search?q={query}` → Full-text search

**Versioning** (`/api/products/{sku}/versions`):
- `GET /api/products/{sku}/versions` → Get all versions timeline
- `GET /api/products/{sku}/versions/{version}` → Get snapshot
- `GET /api/products/{sku}/versions/compare?from={v1}&to={v2}` → Diff
- `POST /api/products/{sku}/versions/{version}/restore` → Restore

**Compliance** (`/api/legal`):
- `GET /api/legal/{country}/rules` → Get rules for country
- `POST /api/legal/validate` → Validate product compliance
- `GET /api/products/{sku}/compliance` → Get compliance status all countries

**Import/Export** (`/api/import-export`):
- `GET /api/import/template` → Download Excel template
- `POST /api/import/excel` → Bulk import
- `GET /api/export/pdf/{sku}` → PDF export
- `GET /api/export/markdown/{sku}` → Markdown export
- `GET /api/export/html/{sku}` → HTML export
- `GET /api/export/catalog-excel?filters` → Catalog bulk export

**Images** (`/api/images`):
- `GET /api/images/search?q={query}` → Search images web
- `POST /api/images/upload` → Upload image
- `GET /api/images/{sku}/{image_type}` → Get image
- `DELETE /api/images/{sku}/{image_type}` → Delete image

**Translations** (`/api/translations`):
- `GET /api/translations/suggest?source_text={text}&source_lang={lang}&target_lang={lang}` → Get suggestions
- `POST /api/translations/save` → Save translation to memory

---

## 6️⃣ TESTING STRATEGY (8 HORAS)

### 6.1 Backend Tests (pytest) - 80% Coverage Target

**Unit Tests** (`backend/tests/`):
- `test_version_manager.py` (40 tests): snapshot creation, diff calculation, restore, timeline
- `test_compliance_validator.py` (35 tests): country validation, field validation, percentage calc
- `test_translation_engine.py` (25 tests): suggestions, memory save/load, glossary lookup
- `test_import_export_manager.py` (30 tests): Excel generation, import validation, PDF export
- `test_image_scraper.py` (20 tests): search, download, validation, resize

**Integration Tests** (`backend/tests/integration/`):
- `test_product_creation_with_versioning.py`: Create → snapshot v1.0 → update → snapshot v1.1
- `test_compliance_workflow.py`: Create ficha → validate PT/IT/ES → missing issues
- `test_bulk_import_workflow.py`: Import 10 productos → each gets v1.0 snapshot
- `test_export_pdf_with_images.py`: Ficha con 3 images → PDF export with images embedded

**Coverage Report**:
- Target: ≥80% line coverage
- Critical paths: VersionManager (95%), ComplianceValidator (90%), ProductSheetManager (85%)

### 6.2 Frontend Tests (Vitest + @vue/test-utils)

**Component Tests** (`frontend/tests/components/`):
- `ProductSheetEditor.spec.js`: Form binding, validation, preset loading
- `CatalogView.spec.js`: Filter application, search, pagination
- `LegalAlerts.spec.js`: Compliance rendering, country badges
- `VersionHistory.spec.js`: Timeline rendering, version selection

**Store Tests** (`frontend/tests/stores/`):
- `productStore.spec.js`: Actions (fetch, create, update), getters
- `versionStore.spec.js`: Version management, diff storage
- `legalStore.spec.js`: Compliance status updates

**Service Tests** (`frontend/tests/services/`):
- `productService.spec.js`: API call mocking, response handling
- `versionService.spec.js`: API calls para versioning endpoints

### 6.3 E2E Tests (Playwright)

**Critical User Flows** (`frontend/e2e/`):
- `e2e/create-product.spec.js`: 
  1. Navegar a "Crear Ficha"
  2. Fill form: SKU, EAN, Title, Family (trigger preset)
  3. Click Save
  4. Verify v1.0 snapshot creado
  5. Verify en Dashboard

- `e2e/translate-product.spec.js`:
  1. Open existing product
  2. Click Translation tab
  3. Select PT language
  4. Fill 5 critical fields (trigger suggestions)
  5. Save
  6. Verify v1.1 snapshot con "Traducción PT"
  7. Check compliance PT = COMPLIANT

- `e2e/compliance.spec.js`:
  1. Open ficha incompleta
  2. Check LegalAlerts: PT NON_COMPLIANT (rojo)
  3. Click "Ver Detalles"
  4. Verify 5 critical fields faltando
  5. Edit → complete campos
  6. Save → verify PT = COMPLIANT (verde)

- `e2e/version-restore.spec.js`:
  1. Open ficha con v2.3
  2. Click "Historial"
  3. Select v2.0 → "Restaurar"
  4. Confirm dialog
  5. Verify restaurado a v2.0
  6. Check versión nueva v3.0 creada

- `e2e/bulk-import.spec.js`:
  1. Click "Importar Masivo"
  2. Download template
  3. Fill Excel (10 filas) localmente
  4. Upload
  5. Verify "✓ 10 productos importados"
  6. Click "Ver Completitud"
  7. Check stats

---

## 7️⃣ DOCUMENTACIÓN FINAL (2 HORAS)

### 7.1 README.md Completo

**Secciones**:
- 🎯 Overview (1 párrafo)
- ⚡ Features principales (6 bullets con emojis)
- 🔧 Tech Stack (Backend, Frontend, Database)
- 📋 Architecture Diagram (ASCII o markdown table)
- 🚀 Quick Start (3 pasos: clone, setup, run)
- 📖 Usage Guide (Screenshots, flujos principales)
- 🧪 Testing
- 📚 API Documentation (link a API_DOCUMENTATION.md)
- 🤝 Contributing
- 📝 License

### 7.2 API_DOCUMENTATION.md

**Formato OpenAPI-style**:
- `/api/products` - All endpoints con ejemplos request/response
- `/api/products/{sku}/versions` - Versioning endpoints
- `/api/legal/{country}/rules` - Compliance endpoints
- `/api/import-export` - Import/Export endpoints
- Error responses (400, 401, 404, 500 con ejemplo JSON)

### 7.3 ARCHITECTURE.md

**Diagrama Backend Layers**:
```
API Layer (FastAPI routes) 
  ↓
Service/Manager Layer (ProductSheetManager, VersionManager, ComplianceValidator, etc.)
  ↓
Model Layer (SQLAlchemy ORM - ProductSheet, ProductVersion, ProductChangelog, LegalRule, Preset)
  ↓
Database Layer (PostgreSQL con JSONB columns, indices optimizados)
```

**Diagrama Frontend Component Hierarchy**:
```
App.vue (Router)
  ├── Dashboard.vue (Stats + Quick Actions)
  ├── CatalogView.vue (Filters + Grid)
  ├── ProductSheetEditor.vue (9 tabs)
  │   ├── LegalAlerts.vue
  │   ├── VersionHistory.vue
  │   ├── DiffViewer.vue
  │   └── ImportExport.vue
  └── [otros]
```

**Data Flow**:
- User Action → Vue Component → Pinia Store (dispatch action) → Service (API call) → Backend Manager → SQLAlchemy Model → PostgreSQL
- Response: Backend → JSON → Service → Store (state update) → Component (reactive render)

---

## 8️⃣ CONFIGURACIÓN DOCKER & CI/CD (2 HORAS)

### 8.1 docker-compose.yml

**Services**:
- `postgres`: PostgreSQL 15, volumen persistence, env vars
- `backend`: FastAPI, depends_on postgres, port 8000, volume code mount
- `frontend`: Node 18, Vite server, port 5173, volume code mount

**Networks**: Internal bridge para inter-service communication

### 8.2 GitHub Actions CI/CD

**Archivo**: `.github/workflows/ci.yml`

**Steps**:
1. Checkout code
2. Setup Python 3.11 + Node 18
3. Install dependencies (pip + npm)
4. Lint: `flake8 backend/` + `eslint frontend/src/`
5. Backend Tests: `pytest backend/ --cov=80%`
6. Frontend Tests: `npm run test:unit`
7. E2E Tests: `npx playwright test`
8. Build: `docker build -f Dockerfile .`
9. Deploy (si main branch): Push a registry

---

## 9️⃣ ROADMAP FUTURO & PHASE 3+

**Phase 3 (Semanas 9-12)**: 
- Multi-user con roles (Admin/Editor/Traductor/Revisor)
- Comentarios en fichas + aprobación workflow
- WebSocket real-time notifications
- Redis caching

**Phase 4 (Q1 2026)**:
- API pública con rate limiting + OAuth2
- Soporte Francia, Alemania, UK
- Webhooks para integraciones ERP

**Phase 5 (Q2 2026)**:
- Traducción automática GPT-4 integration
- IA suggestions para compliance
- OCR en imágenes

**Phase 6 (Q3-Q4 2026)**:
- SaaS cloud (AWS/Azure)
- App móvil iOS/Android
- Offline sync

---

## 🎯 CHECKLIST EJECUCIÓN PARA EL AGENTE

### Fase 1: Setup & Diagnosis (Día 1, 2h)
- [ ] Clonar/actualizar repo
- [ ] Verificar estructura actual vs especificación
- [ ] Crear issue "Status Audit Report" con hallazgos
- [ ] Listar 8-10 archivos a crear/completar

### Fase 2: Backend Completion (Día 2-3, 16h)
- [ ] ✅ VersionManager: create_snapshot, calculate_diff, compare_versions, restore_version
- [ ] ✅ ComplianceValidator: validate_for_country, calculate_compliance_percentage + 3 YAML rules files
- [ ] ✅ PresetManager: load_preset, apply_preset, get_available_families + 150_families.yaml
- [ ] ✅ TranslationEngine: suggest_translation, save_translation, load glossaries + translation_memory.json
- [ ] ✅ ImportExportManager: generate_excel_template, import_from_excel, export_to_pdf, export_to_markdown
- [ ] ✅ ImageScraper + ImageStorage: search_images, download_image, validate_image
- [ ] ✅ API Routes: /api/products/versions, /api/legal/*, /api/import-export/*, /api/images/*
- [ ] ✅ Database migrations: Alembic para nuevas tablas/campos
- [ ] ✅ Tests backend: 80% coverage min (150+ tests)

### Fase 3: Frontend Integration (Día 4-5, 18h)
- [ ] ✅ Pinia Stores: productStore, versionStore, legalStore, uiStore (completos con actions/getters)
- [ ] ✅ API Services: productService, versionService, legalService, importExportService, imageService
- [ ] ✅ LegalAlerts.vue: 3 country cards, compliance badges, issue list
- [ ] ✅ VersionHistory.vue: Timeline visual, compare/restore funcional
- [ ] ✅ DiffViewer.vue: Side-by-side comparison, field highlighting
- [ ] ✅ ImportExport.vue: Tab import (upload, template download), tab export (formats)
- [ ] ✅ ProductSheetEditor.vue: Fix form binding, 9 tabs funcionales, validaciones, presets, translations, images
- [ ] ✅ Dashboard.vue: Stats cards, compliance overview, activity timeline
- [ ] ✅ CatalogView.vue: Filters sidebar, search, grid con lazy load, pagination
- [ ] ✅ Tests frontend: Vitest components + E2E Playwright (5 critical flows)

### Fase 4: Testing & Documentation (Día 6, 8h)
- [ ] ✅ Backend tests: pytest 80%+ coverage
- [ ] ✅ Frontend tests: Vitest component tests + E2E 5 flows
- [ ] ✅ Docker compose: Functional
- [ ] ✅ GitHub Actions CI: Lint + test + build passing
- [ ] ✅ README.md completo
- [ ] ✅ API_DOCUMENTATION.md
- [ ] ✅ ARCHITECTURE.md
- [ ] ✅ QUICKSTART.md (actualizado)

### Final Validation
- [ ] Crear 1 producto → v1.0 snapshot ✓
- [ ] Traducir a PT → v1.1 snapshot ✓
- [ ] Validar PT compliance → COMPLIANT ✓
- [ ] Comparar v1.0 vs v1.1 → diff visible ✓
- [ ] Exportar PDF → profesional ✓
- [ ] Importar Excel masivo (5 filas) → success ✓

---

## 📞 COMMUNICACIÓN CON EL AGENTE

**Cuando recibas updates**:
1. Reporta estado en cada checkpoint
2. Si bloqueado: pasa issue + contexto completo
3. Entrega pull requests pequeños (1-2 features per PR)
4. Tests included en cada PR
5. Actualiza PROJECT_STATUS.md después cada sesión

**Formato de commit**:
- `feat: Implement VersionManager with snapshots` (Backend)
- `feat: Implement LegalAlerts component` (Frontend)
- `test: Add 45 tests for ComplianceValidator` (Testing)
- `docs: Add API documentation` (Docs)

---

## ⚡ RESUMEN EJECUTIVO FINAL

**Estado Actual**: 65% prototipado (Backend: 70%, Frontend: 40%)

**Faltante Crítica**: 
- VersionManager (snapshots, diff, restore) ← BLOQUEADOR
- ComplianceValidator (validación regulatoria) ← BLOQUEADOR
- PresetManager (auto-fill) ← IMPORTANTE
- TranslationEngine (sugerencias) ← IMPORTANTE
- Frontend components (9) ← BLOQUEADOR
- Integración API completa ← BLOQUEADOR

**Timeline**: 4 FASES = 40-50h de trabajo continuo

**Outcome**: MVP 100% funcional que:
- ✅ Crea fichas con versionado automático
- ✅ Traduce a 6 idiomas con sugerencias
- ✅ Valida compliance PT/IT/ES automático
- ✅ Importa/exporta masivamente Excel/PDF
- ✅ Gestiona imágenes productos
- ✅ Timeline histórico con restore
- ✅ Dashboard + Catálogo responsivo
- ✅ Tests 80%+ coverage
- ✅ Documentación completa

**Listo para**: Entrega a cliente real, Q1 2026 multi-usuario + cloud deployment

---

**Última Actualización**: 16 Diciembre 2025, 12:47 PM CET | **Versión del Prompt**: 1.0.0 | **Status**: Ready for Agent Implementation