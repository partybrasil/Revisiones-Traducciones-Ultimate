# 🚀 REVISIONES-TRADUCCIONES-ULTIMATE | GitHub Copilot Agent Prompt v1.0

**Versión**: 1.0.0 | **Fecha**: 16 Dic 2025 | **Estado**: Prototipado 65% → 100%

---

## 📋 MISIÓN OPERACIONAL

Eres **Ingeniero Senior de Prototipado**. Completa **Revisiones-Traducciones-Ultimate** en **4 FASES = 40-50h**:

1. **Auditoría** (2h): Revisar estado actual vs especificación
2. **Backend Core** (16h): VersionManager, ComplianceValidator, PresetManager, TranslationEngine, ImportExportManager, ImageScraper
3. **Frontend MVP** (18h): Pinia stores, API services, 6 componentes Vue, ProductSheetEditor completo
4. **Testing & Docs** (8h): 150+ tests backend, 50+ frontend, E2E 5 flows, documentación

**Estado Actual**: Backend 70% (6 managers faltando), Frontend 40% (sin bindings ni servicios). CERO tests.

**Outcome**: MVP funcional: crear fichas → traducir 6 idiomas → validar compliance PT/IT/ES → importar/exportar Excel/PDF → gestionar imágenes → timeline histórico → restore versiones → Dashboard + Catálogo.

---

## 1️⃣ STACK: FastAPI + SQLAlchemy + PostgreSQL | Vue.js 3 + Pinia

**Backend**: Python FastAPI (async nativo, type hints, OpenAPI automática) + SQLAlchemy ORM (JSONB multiidioma) + PostgreSQL (ACID, full-text search, índices optimizados).

**Frontend**: Vue.js 3 (reactividad elegante) + Vite (bundling sub-ms) + Pinia (state management) + Tailwind (utility-first).

**Database**: ProductSheet + ProductVersion (JSONB snapshots) + ProductChangelog (field-level diffs) + LegalRule (YAML-hydrated) + Preset (auto-fill templates).

---

## 2️⃣ ESTADO ACTUAL DETALLADO

**Backend** (70% → necesita 16h más):
- ✅ main.py, models/product.py, CRUD básico en ProductSheetManager
- ❌ FALTA (0 LOC): version_manager.py, compliance_validator.py, preset_manager.py, translation_engine.py, import_export_manager.py, image_scraper.py + 3 YAML rules, translation_memory.json, 150_families.yaml, glossaries, routes completadas

**Frontend** (40% → necesita 18h más):
- ✅ App.vue, router/index.js, tailwind config
- ⚠️ INCOMPLETO: productStore.js (skeleton), productService.js (stub), ProductSheetEditor.vue (9 tabs vacíos, sin v-model)
- ❌ FALTA (0 LOC): versionStore.js, legalStore.js, uiStore.js, versionService.js, legalService.js, importExportService.js, imageService.js, LegalAlerts.vue, VersionHistory.vue, DiffViewer.vue, ImportExport.vue, Dashboard actualizado, CatalogView actualizado

**Tests**: 0 líneas (necesita 150+ backend + 50+ frontend + 5 E2E flows)

**Docs**: README ⚠️ básico, docker-compose.yml ❌ falta, CI/CD ❌ falta

---

## 3️⃣ BACKEND MANAGERS - ESPECIFICACIONES COMPRIMIDAS

### 3.1 VersionManager (400-500 LOC)
**Métodos**: `create_snapshot(sku, version_type, summary)` → snapshots JSONB automáticos con changelog field-by-field, `calculate_diff(old, new)` → List[changes] sorteados por severity (critical→important→minor), `compare_versions(sku, v_from, v_to)` → diff visual, `restore_version(sku, v)` → revert completo con nueva major version, `get_timeline(sku)` → historial completo, `get_snapshot(sku, v)` → desserializar JSONB.

**Campos críticos por país** (severity calculation): PT (title_short_pt, description_detailed_pt, inci_ingredients_pt, allergens_pt, mode_of_use_pt, warnings_pt, pao_symbol), IT (sufijo _it), ES (inci, allergens_es, mode_of_use_es, warnings_es, pao).

**Testing**: 40 tests (create v1.0, increments minor/major, diff added/updated/deleted/sorts, compare stats, timeline orden, restore revert + audit, edge cases).

---

### 3.2 ComplianceValidator (350-450 LOC)
**Métodos**: `__init__()` → cargar 3 YAML rules (portugal_rules.yaml, italy_rules.yaml, spain_rules.yaml) con estructura country_legal_framework → regulations_by_family → COSMETICS_FACIAL/FOOD_PACKAGED → critical_requirements/optional_requirements. `validate_for_country(sheet, country)` → iterar critical_requirements, verificar translation_mandatory, retornar {status COMPLIANT/WARNING/NON_COMPLIANT, percentage 0-100%, critical_issues[], warnings[]}. `validate_field(field, value, country, family)` → validar INCI/allergens (14 UE máx)/title (3-200 chars)/warnings (10-1000 chars)/PAO (6M/12M/18M/24M/36M).

**YAML Structure**: country, code (PT/IT/ES), authority, regulations_by_family → COSMETICS_FACIAL/FOOD_PACKAGED → critical_requirements array [{field, name, translation_mandatory, severity 🔴/🟡, description, error_message, example}].

**Testing**: 35 tests (PT/IT/ES cosmetics+food compliant, missing fields, allergens validation, INCI validation, percentage calc, status badges, multi-country).

---

### 3.3 PresetManager (250-300 LOC)
**Métodos**: `load_preset(family)` → dict preset completo, `apply_preset(sheet, family)` → auto-fill campos vacíos SOLO (mode_of_use_es, warnings_es, allergens, pictograms, pao), `get_available_families()` → List[{code, display_name, subfamily_count}] (150+ familias), `get_preset_fields(family)` → estructura frontend.

**Presets YAML** (`backend/presets/150_families.yaml`): COSMETICS_FACIAL, COSMETICS_BODY, FOOD_PACKAGED, SUPPLEMENTS + 146 más. Cada una: display_name, subfamilies[], mode_of_use_es/pt/it, warnings_es/pt/it, typical_allergens[], typical_pictograms[], pao_default, natural_origin_range.

**Testing**: 20 tests (load, apply fills empty only, doesn't overwrite, counts fields, 150 families, preset_fields structure).

---

### 3.4 TranslationEngine (300-400 LOC)
**Métodos**: `__init__()` → load translation_memory.json + glossaries (glossary_cosmetics_pt.yaml, etc.), init fuzzy matcher. `suggest_translation(source_text, source_lang, target_lang, threshold=0.75)` → fuzzy matching en memory + glossary lookup, retornar max 5 sugerencias sorted by confidence. `save_translation(source_text, target_text, source_lang, target_lang)` → guardar en memory + persist JSON.

**Memory JSON** (`backend/translations/translation_memory.json`): {es-pt: {Crema Hidratante: [Creme Hidratante, count], ...}, es-it: {...}, es-en: {...}}.

**Glossaries** (`glossary_cosmetics_pt.yaml`): COSMETICS_FACIAL/FOOD_PACKAGED → key_term_es: translation_pt mappings.

**Testing**: 25 tests (exact match, fuzzy >threshold, glossary, save_creates, increment count, export CSV, etc).

---

### 3.5 ImportExportManager (400-500 LOC)
**Métodos**: `generate_excel_template()` → 60+ columnas (SKU, EAN, TITLE_ES/PT/IT, BRAND, FAMILY, SUBFAMILY, NET_WEIGHT, FORMAT_TYPE/MATERIAL/CLOSURE, INCI, MODE_OF_USE_ES/PT/IT, WARNINGS_ES/PT/IT, PAO, ALLERGENS, MADE_IN, etc), Row 2 ejemplos, datavalidation dropdowns (FAMILY 150, FORMAT_TYPE, FORMAT_MATERIAL, PAO), color headers (🔴 critical, 🟡 recommended, ⚪ optional). `import_from_excel(file_path)` → validar SKU/EAN checksum/TITLE_ES/FAMILY/NET_WEIGHT/PAO, crear ProductSheets, aplicar PresetManager, v1.0 snapshots, retornar {imported, errors, skipped, status, completion_percentage}. `export_to_pdf(sku)` → ReportLab A4 profesional (header, 2-column layout general_info/metadata, physical properties, composition INCI, modo_de_uso multiidioma, warnings box rojo ⚠️, images 3 fotos centradas, compliance footer badges 🇵🇹🇮🇹🇪🇸). `export_to_markdown(sku)`, `export_to_html(sku)`, `export_catalog_excel(filters)`.

**Testing**: 30 tests (template 60 cols, dropdowns, color headers, import valid/invalid/checksum, PDF sections/images/badges, markdown/html structure, catalog filters).

---

### 3.6 ImageScraper + ImageStorage (250-300 LOC)
**ImageScraper**: `search_images(query, max_results=20)` → Bing Images API o beautifulsoup4, retornar [{url, title, source, resolution}]. `download_image(url, sku, image_type)` → GET request, validate formato PIL, size <10MB, guardar `backend/storage/images/{sku}/{image_type}/image_{timestamp}.jpg`. `validate_image(file_path)` → format, size, resolution >100x100px. `resize_image(file_path, max_width=3000)` → Pillow, aspect ratio, compress 85% quality JPEG.

**ImageStorage**: `save_uploaded_file(file, sku, image_type)`, `get_image_path(sku, image_type)`, `delete_image(sku, image_type)`.

**Testing**: 20 tests (search returns list, download saves, validate checks, resize maintains ratio, upload persists, delete removes).

---

## 4️⃣ FRONTEND STORES & COMPONENTS - COMPRIMIDAS

### Pinia Stores (800-1000 LOC total)
- **productStore**: products[], currentProduct, loading, error, filters {family, brand, status, languages, search}, pagination. Actions: fetchProducts, getProduct, createProduct, updateProduct, deleteProduct, searchProducts.
- **versionStore**: versions[], currentVersion, changelog[], diff[]. Actions: fetchVersions, getSnapshot, compareVersions, restoreVersion.
- **legalStore**: countries[], complianceStatus{}, rules{}. Actions: fetchRules, validateCompliance, getComplianceStatus.
- **uiStore**: darkMode, sidebarOpen, notifications[], modals{}. Actions: add/removeNotification, toggleDarkMode, toggle Sidebar, openModal, closeModal.

### API Services (300-600 LOC)
- **apiClient.js**: Axios + interceptors (auth header, error handling, retry)
- **productService.js, versionService.js, legalService.js, importExportService.js, imageService.js**: CRUD + specialized operations

### Vue Components (2500-3000 LOC)
- **LegalAlerts.vue** (200 LOC): 3 country cards (PT/IT/ES flags), status badges 🔴🟡🟢, compliance%, "Ver Detalles" expandible
- **VersionHistory.vue** (250 LOC): Timeline vertical, current=blue, archived=gray, "Ver Snapshot", "Comparar", "Restaurar"
- **DiffViewer.vue** (300 LOC): 2 selectores from/to, stats (added/updated/deleted), changes grid field|old|new, highlighting, "Restaurar"
- **ImportExport.vue** (350 LOC): 2 tabs (Importar: drag-drop, template download, progress | Exportar: format selector, filters, export)
- **ProductSheetEditor.vue UPDATE** (800 LOC): fix v-model bindings, 9 tabs (General, Physical, Packaging, Composition, Usage, Warnings, Translation, Images, Legal), validaciones real-time, preset auto-fill, translation suggestions, images upload gallery, legal alerts embed, auto-save debounced, completion footer
- **Dashboard.vue UPDATE** (300 LOC): 4 stat cards, compliance overview, activity timeline, quick actions
- **CatalogView.vue UPDATE** (350 LOC): sidebar filters, search debounce, 4-col grid responsive, lazy load, pagination

---

## 5️⃣ TESTING STRATEGY - COMPRIMIDA

**Backend** (150+ tests, 80%+ coverage): test_version_manager.py (40), test_compliance_validator.py (35), test_translation_engine.py (25), test_import_export_manager.py (30), test_image_scraper.py (20). Integration tests: product_creation_with_versioning, compliance_workflow, bulk_import_workflow, export_pdf_with_images.

**Frontend** (50+ tests, 70%+ coverage): ProductSheetEditor.spec.js, CatalogView.spec.js, LegalAlerts.spec.js, VersionHistory.spec.js. Store tests: productStore.spec.js, versionStore.spec.js, legalStore.spec.js.

**E2E** (5 critical flows, Playwright): create-product (create→v1.0→Dashboard), translate-product (PT→v1.1→compliance), compliance (NON_COMPLIANT→edit→COMPLIANT), version-restore (v2.3→restore v2.0→v3.0), bulk-import (template→fill 10→upload).

---

## 6️⃣ CHECKLIST EJECUCIÓN

**Día 1 (2h)**: Auditoría, estado actual, setup local
**Día 2-3 (16h)**: VersionManager+tests, ComplianceValidator+YAML+tests, PresetManager+YAML+tests, TranslationEngine+memory+glossaries+tests, ImportExportManager+tests, ImageScraper+tests, DB migrations, API routes
**Día 4-5 (18h)**: Pinia stores, API services, LegalAlerts+VersionHistory+DiffViewer+ImportExport, ProductSheetEditor update, Dashboard update, CatalogView update, form bindings
**Día 6 (8h)**: Backend 80%+ coverage, Frontend 70%+ coverage, E2E 5 flows, Docker+CI, README+API docs+Architecture+Quickstart
**Final (30 min)**: Validar: create→v1.0✓, translate PT→v1.1✓, validate PT→COMPLIANT✓, compare v1.0 vs v1.1✓, export PDF✓, import Excel✓

---

## 7️⃣ DOCUMENTACIÓN LINKS

**Ver especificación COMPLETA** (detalles implementación, YAML rules completos, pseudocódigo SQLAlchemy, ejemplos requests/responses, edge cases):
→ **MASTER-PROMPT-COMPLETE-UNIFIED.md** (GitHub repo `/docs/`)

**Por qué este stack**: FastAPI async + JSONB = desarrollo 10x más rápido. SQLAlchemy ORM = auditoría critica automática. Vue 3 Composition API = DX superior. Pinia = state management simple pero poderoso.

---

**INICIO INMEDIATO**: Clona repo, setup venv, `docker-compose up`, comienza FASE 1: Auditoría (identifica 12 archivos faltantes, crea issue "Status Report"). Luego procede FASE 2-4 secuencialmente.

**Última Actualización**: 16 Diciembre 2025 | **Versión**: 1.0.0 | **Status**: Ready for GitHub Copilot Agent