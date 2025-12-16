# 🎯 ÍNDICE DE DOCUMENTACIÓN | Revisiones-Traducciones-Ultimate

**Status**: Prototipado 65% → 100% en 40-50 horas | **Última actualización**: 16 Diciembre 2025

---

## 📚 ESTRUCTURA DE DOCUMENTOS

### 1️⃣ **Agent-Prompt-4000chars.md** ⭐ (USA ESTE PRIMERO)
**Para**: GitHub Copilot Agent, VS Code Copilot Chat, ChatGPT, Claude

**Contenido**: Resumen ejecutivo comprimido (4000 chars máximo)
- ✅ Misión operacional clara (4 fases = 40-50h)
- ✅ Stack técnico justificado (FastAPI + Vue.js)
- ✅ Estado actual detallado (qué falta)
- ✅ Especificaciones comprimidas (VersionManager, ComplianceValidator, etc.)
- ✅ Frontend Pinia stores + componentes resumen
- ✅ Testing strategy resumida
- ✅ Checklist ejecución día por día

**Cómo usarlo**:
```
Opción 1: Copiar TODO en GitHub Copilot Chat
Opción 2: Crear Custom Agent con contenido completo
Opción 3: Copiar en Cursor IDE como instructions.md
```

---

### 2️⃣ **Master-Prompt-Complete.md** 📖 (REFERENCIA TÉCNICA)
**Para**: Arquitectos, revisión técnica, edge cases, pseudocódigo detallado

**Contenido**: 5000+ palabras con detalles completos
- ✅ VersionManager - pseudocódigo completo + SQLAlchemy integration + 40 tests
- ✅ ComplianceValidator - YAML rules PT/IT/ES completos + validación fields + 35 tests
- ✅ PresetManager - 150 families YAML + apply logic + 20 tests
- ✅ TranslationEngine - fuzzy matching + glossaries + 25 tests
- ✅ ImportExportManager - Excel template 60+ cols + PDF generation + 30 tests
- ✅ ImageScraper + ImageStorage - web scraping + validation + 20 tests
- ✅ API routes - GET/POST/DELETE endpoints completos
- ✅ Frontend components - Vue.js código ejemplo (LegalAlerts, etc.)
- ✅ Testing comprehensive - pytest + vitest + playwright
- ✅ Roadmap futuro - v1.1 → v2.0 timeline

**Cómo usarlo**:
```
Consultar como REFERENCIA mientras implementas
Buscar sección específica (Ctrl+F "VersionManager")
Copiar pseudocódigo como base para desarrollo
Usar YAML rules como template exacto
```

---

## 🎯 FLUJO RECOMENDADO

### ANTES DE EMPEZAR
1. ✅ Lee este índice (5 min)
2. ✅ Lee **Agent-Prompt-4000chars.md** completo (20 min)
3. ✅ Entiende misión + estado actual + stack

### DURANTE DESARROLLO
1. **Fase 1 (2h)**: Auditoría → Usa Agent-Prompt
2. **Fase 2 (16h)**: Backend → Consulta Master-Prompt secciones VersionManager, ComplianceValidator, etc.
3. **Fase 3 (18h)**: Frontend → Consulta Master-Prompt sección Frontend components
4. **Fase 4 (8h)**: Testing + Docs → Consulta Master-Prompt Testing strategy

### DURANTE CODING CON GITHUB COPILOT
```
Opción A (Recomendado):
1. Abre Agent-Prompt-4000chars.md en lado izquierdo
2. Abre Master-Prompt-Complete.md en pestaña separada
3. Pregunta a Copilot: "Based on Agent-Prompt, implement VersionManager method..."
4. Copilot context-aware genera código

Opción B (Quick):
1. Copia sección específica de Master-Prompt
2. Pega en Chat de Copilot
3. Pide: "Implement based on this pseudocode..."
4. Copilot genera código production-ready
```

---

## 📊 COMPARATIVA DOCUMENTOS

| Aspecto | Agent-Prompt | Master-Prompt |
|---------|--------------|---------------|
| **Tamaño** | 4000 chars | 10,000+ words |
| **Propósito** | Ejecución rápida | Referencia detallada |
| **Audiencia** | Desarrollador | Arquitecto + Desarrollador |
| **Detalle** | Comprimido | Exhaustivo |
| **Pseudocódigo** | Resumido | Completo con SQLAlchemy |
| **YAML rules** | No incluyen | PT/IT/ES completos |
| **Ejemplos código** | Mínimos | Extensos (Vue, pytest, etc.) |
| **Testing** | Resumen | 150+ tests detallados |
| **Roadmap** | No | Sí, v1.1-v2.0 |

---

## 🚀 CASO DE USO: IMPLEMENTAR VersionManager

### Con Agent-Prompt (Quick Start)
```
1. Abre Agent-Prompt-4000chars.md
2. Busca sección "VersionManager (400-500 LOC)"
3. Lee métodos: create_snapshot, calculate_diff, compare_versions, restore_version
4. Propósito claro: snapshots JSONB + changelog field-by-field
5. Pide a Copilot: "Implement VersionManager class based on Agent-Prompt specification..."
6. Copilot entiende: async methods, SQLAlchemy models, JSONB serialization
7. Genera código en 3-5 min
```

### Con Master-Prompt (Deep Dive)
```
1. Abre Master-Prompt-Complete.md
2. Busca "### 3.1 VersionManager - Snapshots & Restore Detallado"
3. Lee pseudocódigo detallado para create_snapshot() (15 líneas de pseudocódigo)
4. Lee ejemplo SQLAlchemy integration (40+ líneas código)
5. Lee 40 tests específicos (cada test documenta edge case)
6. Pide a Copilot: "Implement this pseudocode with 100% coverage..."
7. Copilot genera código + tests en 10-15 min
8. Copilot también entiende: critical_fields por país, JSONB serialization, changelog entries
```

---

## 📋 CHECKLIST: ANTES DE COPIAR A GITHUB

```
Antes de pasar estos docs al repo GitHub:

☑️ Cambiar [YOUR_REPO_PATH] → repo actual URL
☑️ Cambiar [YOUR_USERNAME] → tu usuario GitHub
☑️ Cambiar [PROJECT_YEAR] → 2025 (si necesario)
☑️ Verificar rutas archivos (backend/, frontend/) coinciden con estructura
☑️ Actualizar links si docs están en subcarpetas (docs/)
☑️ Sincronizar dates con fecha actual
☑️ Si agregar a GitHub Copilot Agent: comprime Master-Prompt → version 2000 chars
☑️ Si crear GitHub Copilot Space: usa Agent-Prompt-4000chars como "instructions"
```

---

## 🔗 INTEGRACIÓN CON GITHUB COPILOT AGENT

### Opción 1: GitHub Copilot Space (Recomendado)
```yaml
# GitHub Settings > Copilot > Create Space

Title: Revisiones-Traducciones-Ultimate Development
Description: AutoDEV prototipado completion - 4 fases, 40-50h, backend core + frontend MVP
Custom Instructions: [Copiar contenido Agent-Prompt-4000chars.md completo aquí]
Enabled: true

Cuando abres Space:
→ Copilot carga Agent-Prompt automáticamente
→ Sabe estado actual, stack, managers faltantes
→ Genera código coherente con especificación
```

### Opción 2: Custom Instruction en VS Code
```
Crear archivo: .vscode/copilot-instructions.md

Contenido: [Copiar Agent-Prompt-4000chars.md]

Cuando usas Copilot en VS Code:
→ Ctrl+I en editor → Copilot context-aware
→ Entiende project state
→ Genera código siguiendo especificación
```

### Opción 3: ChatGPT/Claude Custom GPT
```
Upload files: Agent-Prompt-4000chars.md + Master-Prompt-Complete.md
Set: "You are GitHub Copilot Agent for Revisiones-Traducciones-Ultimate"
Prompt: "Based on these specifications, implement [feature]..."
```

---

## 🎓 EJEMPLO: FASE 2 COMPLETA CON AGENTE

### Fase 2: Backend Core (16 horas)

**Hora 1-2: VersionManager**
```
Prompt a Copilot:
"Based on Agent-Prompt specification section 'VersionManager (400-500 LOC)',
implement the complete VersionManager class with all 6 methods:
create_snapshot, calculate_diff, get_snapshot, compare_versions, get_timeline, restore_version.

Include:
- SQLAlchemy models integration
- JSONB serialization
- Field-level diff calculation
- Critical fields per country (PT/IT/ES)
- Complete docstrings with examples
- Type hints"

Copilot output: VersionManager class 450 LOC + docstrings + type hints
Time: ~3-5 min
Quality: Production-ready

Then:
Prompt: "Generate 40 pytest tests for VersionManager covering all methods and edge cases"
Copilot output: 40 tests @ 80%+ coverage
Time: ~5-7 min
```

**Hora 3-4: ComplianceValidator**
```
Prompt: "Implement ComplianceValidator with 350-450 LOC as specified in Agent-Prompt.
Start by loading the YAML rules from backend/legal_framework/rules/
Then implement validate_for_country() method.

Use this YAML structure for Portugal rules:
[Copiar YAML ejemplo de Master-Prompt]"

Copilot output: ComplianceValidator + YAML rules loading + all methods
Time: ~5-7 min

Then: 35 tests with 100% coverage
```

**Hora 5-6: PresetManager**
```
Prompt: "Based on Agent-Prompt, implement PresetManager with 250-300 LOC.
Load presets from YAML file with 150 product families (provide 10 examples, expand).
Implement apply_preset() method that auto-fills empty fields ONLY.
Include all 6 methods."

Copilot output: PresetManager + presets YAML + 20 tests
Time: ~3-4 min
```

**Hora 7-10: TranslationEngine, ImportExportManager, ImageScraper**
```
Same pattern for each:
1. Copy specification from Agent-Prompt
2. Copilot implements class + methods + tests
3. Time: 3-4 min per manager
```

**Hora 11-12: Database Migrations + API Routes**
```
Prompt: "Generate Alembic migrations for ProductVersion, ProductChangelog tables.
Create all indexes as specified.
Then generate all API routes in backend/routes/ for versions, legal, import_export, images"

Copilot output: Complete migrations + routes
```

**Hora 13-16: Integration + Testing**
```
Run: pytest backend/ --cov=backend -v
Target: 80%+ coverage
Fix any gaps → Copilot refine
Final: All 150+ tests passing
```

**RESULTADO**: Fase 2 COMPLETA en 16 horas con Copilot

---

## ✅ VALIDACIÓN FINAL

Después de implementar todos:
```
✓ VersionManager: Snapshots, diffs, restore working
✓ ComplianceValidator: PT/IT/ES validation 95%+ accurate
✓ PresetManager: 150 families loading, auto-fill working
✓ TranslationEngine: Fuzzy matching + glossaries working
✓ ImportExportManager: Excel template, bulk import, PDF export working
✓ ImageScraper: Web scraping + storage working
✓ Frontend: Pinia stores + Vue components + form bindings working
✓ Tests: 150+ backend (80%+ coverage) + 50+ frontend (70%+ coverage) passing
✓ E2E: 5 critical flows passing (create→translate→validate→restore→export)
✓ Docs: README + API docs + Architecture docs complete
✓ Docker: docker-compose up -d working
✓ CI/CD: GitHub Actions running lint + test + build

OUTCOME: MVP 100% funcional, production-ready, fully tested
```

---

## 📞 SOPORTE

Si necesitas:
- **Clarificar especificación**: Consulta Master-Prompt sección específica
- **Quick implementation**: Usa Agent-Prompt-4000chars.md
- **Edge case handling**: Busca "testing" en Master-Prompt
- **Roadmap future**: Ver sección "🚀 ROADMAP FUTURO" en Master-Prompt

---

**PRÓXIMOS PASOS**:
1. ✅ Lees este índice
2. ✅ Copias Agent-Prompt-4000chars.md → GitHub Copilot Chat
3. ✅ Comenzas Fase 1: Auditoría
4. ✅ Copias Master-Prompt secciones específicas según necesites
5. ✅ Implementas FASE 2 → FASE 3 → FASE 4 secuencialmente

**¡Listo para codear!** 🚀