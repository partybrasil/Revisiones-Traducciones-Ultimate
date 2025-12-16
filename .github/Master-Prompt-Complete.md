# 📚 MASTER-PROMPT-COMPLETE-UNIFIED | Revisiones-Traducciones-Ultimate v1.0.0

**Versión**: 1.0.0 | **Fecha**: 16 Diciembre 2025 | **Estado**: Especificación Completa - Detalles Implementación

---

## 📖 INTRODUCCIÓN

Este documento contiene la **especificación técnica COMPLETA y DETALLADA** del proyecto. Úsalo como **referencia arquitectónica, pseudocódigo, ejemplos y edge cases** mientras implementas basándote en el **Agent-Prompt-4000chars.md** (resumen ejecutivo).

**Estructura**: Especificaciones por manager, YAML rules completos, ejemplos SQLAlchemy, requests/responses API, pseudocódigo detallado, edge cases, testing strategies, roadmap futuro.

---

## 3️⃣ BACKEND MANAGERS - ESPECIFICACIONES COMPLETAS

### 3.1 VersionManager - Snapshots & Restore Detallado

#### Concepto
Cada vez que usuario guarda → snapshot automático JSONB completo de ProductSheet + changelog field-by-field + versionado inteligente (1.0→1.1 minor, →2.0 major).

#### Method: create_snapshot(sku: str, version_type: str, change_summary: str) → dict

```
PSEUDOCÓDIGO:
1. Query DB obtener ProductSheet actual con sku = sku
   - Si no existe: raise ProductNotFoundError
   - Si existe: obtener old_state = {todos campos serializados a dict}

2. Query DB obtener última ProductVersion para sku
   - Si existe: prev_version = last version
   - Si NO existe: prev_version = None

3. Calcular new_version_number:
   - Si prev_version = None: version_number = "1.0"
   - Si prev_version existe:
     - Si version_type = "major": 
       - major = int(prev_version.split(".")[0])
       - minor = 0
       - new_version_number = f"{major + 1}.0"
     - Si version_type = "minor":
       - major = int(prev_version.split(".")[0])
       - minor = int(prev_version.split(".")[1])
       - new_version_number = f"{major}.{minor + 1}"
     - Si version_type = "patch":
       - new_version_number = incrementar último dígito (fallback minor)

4. Serializar ProductSheet actual a JSONB dict:
   - nested_dict = {
     "sku": sheet.sku,
     "ean_list": sheet.ean_list,
     "brand": sheet.brand,
     "gama": sheet.gama (ya JSON),
     "family": sheet.family,
     "title_short": sheet.title_short (JSON multiidioma),
     "description_detailed": sheet.description_detailed (JSON),
     "made_in": sheet.made_in (JSON),
     "distributor": sheet.distributor (JSON),
     "responsible_person": sheet.responsible_person (JSON),
     "natural_origin_percentage": sheet.natural_origin_percentage (JSON),
     "net_weight_value": sheet.net_weight_value,
     "net_weight_unit": sheet.net_weight_unit,
     "format_type": sheet.format_type,
     "format_material": sheet.format_material,
     "format_closure": sheet.format_closure,
     "packaging_languages": sheet.packaging_languages,
     "inci_ingredients": sheet.inci_ingredients (Text array),
     "key_ingredients": sheet.key_ingredients (JSON),
     "allergens_present": sheet.allergens_present (JSON array),
     "allergens_may_contain": sheet.allergens_may_contain (JSON array),
     "mode_of_use": sheet.mode_of_use (JSON multiidioma),
     "warnings": sheet.warnings (JSON multiidioma),
     "storage_conditions": sheet.storage_conditions (JSON),
     "pao": sheet.pao,
     "pictograms": sheet.pictograms (JSON array),
     "certifications": sheet.certifications (JSON array),
     "product_images": sheet.product_images (JSON array),
     "status": sheet.status,
     "completion_percentage": sheet.completion_percentage,
     ... (todos los campos)
   }

5. SOLO si prev_version existe:
   changes_list = calculate_diff(prev_state, nested_dict)
   - Si len(changes_list) = 0:
     - log WARN: "No changes detected in snapshot"
     - version_type = SKIP (no crear snapshot)

6. Crear entrada ProductVersion:
   new_version = ProductVersion(
     sku=sku,
     version_number=new_version_number,
     version_type=version_type,
     snapshot_date=datetime.utcnow(),
     created_by=current_user_id,
     change_summary=change_summary,
     complete_snapshot=nested_dict  # JSONB SQLAlchemy auto-serializes
   )
   session.add(new_version)

7. Para cada change en changes_list (SOLO si prev_version existe):
   changelog_entry = ProductChangelog(
     sku=sku,
     version_from=prev_version.version_number,
     version_to=new_version_number,
     changed_by=current_user_id,
     changed_date=datetime.utcnow(),
     changes_array=[
       {
         "field_path": change["field_path"],
         "field_display_name": change["field_display_name"],
         "old_value": change["old_value"],
         "new_value": change["new_value"],
         "change_type": change["change_type"],
         "severity": change["severity"]
       }
     ],
     change_summary=change_summary
   )
   session.add(changelog_entry)

8. UPDATE products table:
   sheet.current_version = new_version_number
   sheet.updated_date = datetime.utcnow()
   sheet.updated_by = current_user_id
   session.commit()

9. RETORNAR response dict:
   {
     "sku": sku,
     "version_number": new_version_number,
     "changes_count": len(changes_list),
     "critical_changes": [c for c in changes_list if c["severity"] == "critical"],
     "timestamp": datetime.utcnow().isoformat(),
     "status_badge": "✅ v" + new_version_number,
     "message": f"Snapshot v{new_version_number} created successfully"
   }
```

#### Method: calculate_diff(old_state: dict, new_state: dict) → List[dict]

```
PSEUDOCÓDIGO:
1. HELPER FUNCTION flatten_dict(d, parent_key=''):
   items = []
   for key, value in d.items():
     new_key = f"{parent_key}.{key}" if parent_key else key
     if isinstance(value, dict):
       items.extend(flatten_dict(value, new_key).items())
     else:
       items.append((new_key, value))
   return dict(items)

2. Flatten ambos dicts:
   old_flat = flatten_dict(old_state)
   new_flat = flatten_dict(new_state)
   all_keys = set(old_flat.keys()).union(set(new_flat.keys()))

3. CONSTANT CRITICAL_FIELDS por país:
   PT_CRITICAL = ["title_short.pt", "description_detailed.pt", "inci_ingredients", 
                  "allergens_present", "mode_of_use.pt", "warnings.pt", "pao"]
   IT_CRITICAL = ["title_short.it", "description_detailed.it", "inci_ingredients",
                  "allergens_present", "mode_of_use.it", "warnings.it", "pao"]
   ES_CRITICAL = ["inci_ingredients", "allergens_present", "mode_of_use.es", 
                  "warnings.es", "pao"]
   ALL_CRITICAL_FIELDS = PT_CRITICAL + IT_CRITICAL + ES_CRITICAL

4. Iterar all_keys:
   changes = []
   for field_path in all_keys:
     old_value = old_flat.get(field_path, None)
     new_value = new_flat.get(field_path, None)
     
     if old_value == new_value:
       continue  # Sin cambios
     
     # Determinar change_type
     if old_value is None and new_value is not None:
       change_type = "added"
       is_critical = field_path in ALL_CRITICAL_FIELDS
       severity = "critical" if is_critical else "important"
     elif old_value is not None and new_value is None:
       change_type = "deleted"
       severity = "important"
     else:
       change_type = "updated"
       is_critical = field_path in ALL_CRITICAL_FIELDS
       severity = "critical" if is_critical else "minor"
     
     # Field display name mapping
     field_display_name = FIELD_DISPLAY_NAMES.get(field_path, field_path)
     
     changes.append({
       "field_path": field_path,
       "field_display_name": field_display_name,
       "old_value": old_value,
       "new_value": new_value,
       "change_type": change_type,
       "severity": severity,
       "timestamp": datetime.utcnow().isoformat()
     })

5. Sort changes:
   - PRIMARY: severity DESC (critical → important → minor)
   - SECONDARY: change_type ORDER (added → updated → deleted)
   - TERTIARY: field_path ASC (alphabetical)
   changes = sorted(changes, key=lambda x: (
     SEVERITY_ORDER[x["severity"]],
     CHANGE_TYPE_ORDER[x["change_type"]],
     x["field_path"]
   ))

6. RETORNAR changes list
```

#### Method: compare_versions(sku: str, v_from: str, v_to: str) → dict

```
1. snapshot_from = get_snapshot(sku, v_from)  # Deserializar JSONB
2. snapshot_to = get_snapshot(sku, v_to)
3. changes_list = calculate_diff(snapshot_from, snapshot_to)

4. Stats:
   stats = {
     "total_changes": len(changes_list),
     "added": len([c for c in changes_list if c["change_type"] == "added"]),
     "updated": len([c for c in changes_list if c["change_type"] == "updated"]),
     "deleted": len([c for c in changes_list if c["change_type"] == "deleted"]),
     "critical": len([c for c in changes_list if c["severity"] == "critical"]),
     "important": len([c for c in changes_list if c["severity"] == "important"]),
     "minor": len([c for c in changes_list if c["severity"] == "minor"])
   }

5. RETORNAR:
   {
     "from_version": v_from,
     "to_version": v_to,
     "stats": stats,
     "changes": changes_list,
     "comparison_date": datetime.utcnow().isoformat()
   }
```

#### Method: restore_version(sku: str, version: str) → dict

```
1. snapshot_dict = get_snapshot(sku, version)  # JSONB desserializado

2. sheet = Query ProductSheet WHERE sku = sku
   
3. Restaurar TODOS los fields desde snapshot:
   for field_name, field_value in snapshot_dict.items():
     setattr(sheet, field_name, field_value)
   
4. Llamar create_snapshot():
   restore_result = create_snapshot(
     sku=sku,
     version_type="major",
     change_summary=f"Restored from v{version} by {current_user_id}"
   )

5. RETORNAR restore_result con nueva version creada
```

#### SQLAlchemy Integration

```python
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Integer, JSON, DateTime, ForeignKey
from datetime import datetime
from models.product import ProductSheet, ProductVersion, ProductChangelog

class VersionManager:
    def __init__(self, session: Session):
        self.session = session
    
    def create_snapshot(self, sku: str, version_type: str, change_summary: str, user_id: str):
        try:
            product = self.session.query(ProductSheet).filter_by(sku=sku).first()
            if not product:
                raise ValueError(f"Product {sku} not found")
            
            # Obtener versión anterior si existe
            prev_version = self.session.query(ProductVersion)\
                .filter_by(sku=sku)\
                .order_by(ProductVersion.snapshot_date.desc())\
                .first()
            
            # Calcular new version
            new_version_number = self._calculate_version_number(prev_version, version_type)
            
            # Serializar estado actual
            old_state = prev_version.complete_snapshot if prev_version else None
            new_state = product.to_dict()  # Método en ProductSheet model
            
            # Calcular diff
            changes = calculate_diff(old_state, new_state) if prev_version else []
            
            # Crear snapshot
            new_version = ProductVersion(
                sku=sku,
                version_number=new_version_number,
                version_type=version_type,
                snapshot_date=datetime.utcnow(),
                created_by=user_id,
                change_summary=change_summary,
                complete_snapshot=new_state,
                status="current"
            )
            self.session.add(new_version)
            
            # Marcar versión anterior como archived
            if prev_version:
                prev_version.status = "archived"
            
            # Crear changelog entries
            for change in changes:
                changelog = ProductChangelog(
                    sku=sku,
                    version_from=prev_version.version_number if prev_version else None,
                    version_to=new_version_number,
                    changed_by=user_id,
                    changed_date=datetime.utcnow(),
                    changes_array=[change],
                    change_summary=change_summary
                )
                self.session.add(changelog)
            
            # Update product
            product.current_version = new_version_number
            product.updated_date = datetime.utcnow()
            product.updated_by = user_id
            
            self.session.commit()
            
            return {
                "sku": sku,
                "version_number": new_version_number,
                "changes_count": len(changes),
                "status": "success"
            }
        
        except Exception as e:
            self.session.rollback()
            raise e

    def _calculate_version_number(self, prev_version, version_type: str) -> str:
        if not prev_version:
            return "1.0"
        
        parts = prev_version.version_number.split(".")
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        
        if version_type == "major":
            return f"{major + 1}.0"
        else:  # minor
            return f"{major}.{minor + 1}"
```

#### Testing Strategy (40 tests)

```python
# test_version_manager.py

def test_create_snapshot_first_time_creates_v1_0():
    """Crear snapshot en producto nuevo → v1.0 creada"""
    manager = VersionManager(session)
    result = manager.create_snapshot("CF-HYD-001", "major", "Initial version", "user1")
    assert result["version_number"] == "1.0"
    assert result["changes_count"] == 0  # Primera vez sin cambios

def test_create_snapshot_increments_minor_version():
    """Edit sin cambios críticos → v1.0 → v1.1"""
    # Setup: crear v1.0
    # Edit: cambiar description_es (minor field)
    # Expect: v1.1 creada con severity=minor

def test_create_snapshot_increments_major_version():
    """Edit con cambios críticos → v1.0 → v2.0"""
    # Setup: crear v1.0
    # Edit: cambiar title_short_pt (critical field PT)
    # Expect: v2.0 creada con severity=critical

def test_calculate_diff_added_field_critical():
    """Nuevo field crítico add → severity=critical"""
    old = {"title_short": {"es": "Crema"}}
    new = {"title_short": {"es": "Crema", "pt": "Creme"}}
    diff = calculate_diff(old, new)
    assert any(c["field_path"] == "title_short.pt" and 
              c["severity"] == "critical" for c in diff)

def test_calculate_diff_updated_field_minor():
    """Update field no-crítico → severity=minor"""
    old = {"brand": "MarcaA"}
    new = {"brand": "MarcaB"}
    diff = calculate_diff(old, new)
    assert any(c["field_path"] == "brand" and 
              c["change_type"] == "updated" and 
              c["severity"] == "minor" for c in diff)

def test_calculate_diff_sorts_by_severity():
    """Changes ordered: critical → important → minor"""
    # Create mock diff con múltiples severities
    diff = calculate_diff(old_state, new_state)
    severities = [c["severity"] for c in diff]
    # Verify orden descending de severity

def test_compare_versions_returns_correct_stats():
    """Compare v1.0 vs v1.1 → correct counts"""
    stats = manager.compare_versions("CF-HYD-001", "1.0", "1.1")
    assert stats["stats"]["total_changes"] > 0
    assert stats["stats"]["added"] + stats["stats"]["updated"] + stats["stats"]["deleted"] == stats["stats"]["total_changes"]

def test_get_timeline_returns_ordered_versions():
    """Timeline retorna versiones order DESC by snapshot_date"""
    timeline = manager.get_timeline("CF-HYD-001")
    assert timeline[0]["version_number"] == "1.1"  # Latest
    assert timeline[-1]["version_number"] == "1.0"  # Oldest

def test_restore_version_reverts_all_fields():
    """Restore v1.0 → todos fields revertidos"""
    manager.restore_version("CF-HYD-001", "1.0")
    current = manager.get_snapshot("CF-HYD-001", "1.0")
    assert current["title_short"]["es"] == original_value_v1_0

def test_restore_creates_new_major_version():
    """Restore v1.0 from v1.1 → crea v2.0"""
    result = manager.restore_version("CF-HYD-001", "1.0")
    assert result["version_number"] == "2.0"

def test_restore_audit_trail_recorded():
    """Restore registra quién y cuándo"""
    result = manager.restore_version("CF-HYD-001", "1.0", "user1")
    assert result["created_by"] == "user1"
    assert result["timestamp"] != None

# ... + 30 más edge cases
```

---

### 3.2 ComplianceValidator - Validación Regulatoria Completa

#### YAML Rules Files

**backend/legal_framework/rules/portugal_rules.yaml**:
```yaml
country_legal_framework:
  country: "Portugal"
  code: "PT"
  authority: "INFARMED - Instituto Nacional da Farmácia e do Medicamento"
  
  regulations_by_family:
    COSMETICS_FACIAL:
      regulations:
        - "Regulamento (CE) nº 1223/2009"
        - "Decreto-Lei nº 189/2008"
        - "Portaria nº 1102/2010"
      
      critical_requirements:
        - field: "title_short_pt"
          name: "Título Curto PT"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Designação do produto em português obrigatória por INFARMED"
          error_message: "O título em português está ausente ou vazio - OBRIGATÓRIO"
          example: "Creme Hidratante Facial 24h"
          field_type: "string"
          min_length: 3
          max_length: 200
        
        - field: "description_detailed_pt"
          name: "Descrição Detalhada PT"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Descrição completa em português para conformidade INFARMED"
          error_message: "A descrição em português é obrigatória"
          example: "Creme facial hidratante com ácido hialurônico, vitamina E e aloe vera. Apropriado para peles normais a secas..."
          field_type: "text"
          min_length: 20
          max_length: 2000
        
        - field: "inci_ingredients_pt"
          name: "Ingredientes INCI"
          translation_mandatory: false
          severity: "🔴 CRÍTICO"
          description: "Lista INCI completa (idioma não importa, contanto que seja válida segundo nomenclatura INCI)"
          error_message: "INCI ausente ou inválida"
          example: "WATER, GLYCERIN, PHENOXYETHANOL, SODIUM HYALURONATE, TOCOPHEROL, ALOE BARBADENSIS LEAF JUICE"
          field_type: "inci_list"
          validation_rules:
            - "must_be_array"
            - "each_item_valid_inci_code"
            - "min_items_1"
        
        - field: "allergens_present_pt"
          name: "Alérgenos Declarados"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Declaração clara de 14 alérgenos UE 1169/2011 em português"
          error_message: "Declaração de alérgenos obrigatória segundo Regulamento UE 1169/2011"
          example: "Contém: Amendoim, Frutos de casca rija (Amêndoa, Avelã). Pode conter trazas de: Leite, Ovo"
          field_type: "allergen_declaration"
          eu_allergen_list: ["Celery", "Cereals containing gluten", "Crustaceans", "Eggs", "Fish", "Lupin", 
                            "Milk", "Molluscs", "Mustard", "Peanuts", "Sesame", "Shellfish", "Soy", "Tree nuts"]
          validation_rules:
            - "max_14_allergens"
            - "portuguese_language_required"
        
        - field: "mode_of_use_pt"
          name: "Modo de Emprego"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Instruções claras de uso em português"
          error_message: "Instruções de uso obrigatórias"
          example: "Aplicar pequena quantidade na face limpa e massajar suavemente até absorção completa. Usar mañana y noite. Para otimizar os resultados, usar com protetor solar SPF 30+."
          field_type: "text"
          min_length: 10
          max_length: 500
        
        - field: "warnings_pt"
          name: "Avisos e Precauções"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          description: "Avisos obligatorios en portugués según INFARMED"
          error_message: "Avisos obrigatórios ausentes"
          example: "Evitar contacto com olhos. Uso externo. Se irritação, suspender uso imediatamente. Manter fora do alcance das crianças. Usar sempre com protetor solar (SPF 30+) durante o dia."
          field_type: "text"
          min_length: 10
          max_length: 500
        
        - field: "pao_symbol"
          name: "PAO (Período Após Abertura)"
          translation_mandatory: false
          severity: "🔴 CRÍTICO"
          description: "Símbolo obrigatório PAO: quantos meses após abertura o produto é seguro"
          error_message: "PAO não especificado - campo obrigatório"
          example: "12M"
          field_type: "enum"
          valid_values: ["6M", "12M", "18M", "24M", "36M"]
      
      optional_requirements:
        - field: "made_in_pt"
          name: "Origem PT"
          translation_mandatory: true
          severity: "🟡 RECOMENDADO"
          description: "País de origem em português - não obrigatório mas recomendado para transparência"
          example: "Fabricado em Portugal"
        
        - field: "natural_origin_percentage"
          name: "% Origem Natural"
          translation_mandatory: false
          severity: "🟡 RECOMENDADO"
          description: "Percentagem de ingredientes de origem natural certificada"
          example: "92% de ingredientes de origem natural certificada"
          field_type: "percentage"

    FOOD_PACKAGED:
      regulations:
        - "Regulamento (UE) 1169/2011"
        - "Decreto-Lei nº 75/2010"
      
      critical_requirements:
        - field: "title_short_pt"
          name: "Nome Produto PT"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          error_message: "Nome do produto em português obrigatório"
          example: "Chocolate Negro 70% Cacau"
        
        - field: "allergens_pt"
          name: "Alérgenos 1169/2011"
          translation_mandatory: true
          severity: "🔴 CRÍTICO"
          error_message: "Alérgenos segundo 1169/2011 obrigatórios em português"
          example: "Contém: Cacau, Leite. Pode conter trazas de: Frutos secos (Avelã)"
          field_type: "allergen_declaration"
        
        - field: "net_weight_value"
          name: "Peso Líquido"
          translation_mandatory: false
          severity: "🔴 CRÍTICO"
          error_message: "Peso líquido obrigatório"
          example: 250
          field_type: "float"
          validation_rules: ["must_be_positive", "realistic_range"]
        
        - field: "net_weight_unit"
          name: "Unidade Peso"
          translation_mandatory: false
          severity: "🔴 CRÍTICO"
          error_message: "Unidade peso obrigatória"
          example: "g"
          field_type: "enum"
          valid_values: ["g", "ml", "kg", "L"]
```

**backend/legal_framework/rules/italy_rules.yaml** (sufijo _it):
```yaml
# Structure identical a portugal_rules.yaml pero con:
# - country: Italy, code: IT, authority: "Ministero della Salute"
# - Rules específicas italiane
# - field suffixes: _it en lugar de _pt
# - Italian language legal references
```

**backend/legal_framework/rules/spain_rules.yaml** (sufijo _es):
```yaml
# Structure identical pero:
# - country: Spain, code: ES, authority: "AEMPS - Agencia Española de Medicamentos"
# - Rules específicas españolas
# - Énfasis en INCI (cualquier idioma válido pero obligatorio)
# - field suffixes: _es
```

#### Method: validate_for_country(sheet: ProductSheet, country: str) → dict

```
PSEUDOCÓDIGO:
1. Validar country en lista soportada (PT, IT, ES)

2. Obtener lista critical_requirements para (country, sheet.family):
   rules = self.rules_cache.get((country, sheet.family, "critical"), [])

3. issues = []
4. ITERAR CADA rule en rules:
   field_name = rule.field_name
   field_value = getattr(sheet, field_name, None)
   
   SI rule.translation_mandatory = True:
     # Para fields multiidioma: verificar value[lang] no vacío
     if field_name contains "title_short" o "description" o "mode_of_use" o "warnings":
       LANG_SUFFIX = _pt, _it, _es según country
       field_with_lang = field_name + LANG_SUFFIX
       if field_value is None or field_value == "" or len(field_value.strip()) == 0:
         issues.append({
           "field_name": field_name,
           "error_message": rule.error_message,
           "severity": rule.severity,
           "example": rule.example
         })
   ELSE:
     # Field obligatorio aunque sea en any idioma
     if field_value is None or field_value == "":
       issues.append({...})

5. Contar campos válidos:
   valid_count = len(rules) - len(issues)
   percentage = (valid_count / len(rules)) * 100

6. Determinar status:
   if percentage == 100:
     status = "COMPLIANT"
   elif percentage >= 60:
     status = "WARNING"
   else:
     status = "NON_COMPLIANT"

7. RETORNAR:
   {
     "country": country,
     "status": status,
     "percentage": int(percentage),
     "critical_issues": issues,
     "warnings": [],  # Optional requirements
     "valid_count": valid_count,
     "total_critical_fields": len(rules)
   }
```

#### Method: validate_field(field_name: str, value: any, country: str, family: str) → bool

```
PSEUDOCÓDIGO:
1. Lookup rule para (country, family, field_name)

2. Según field_type en rule, aplicar validaciones:
   
   IF field_type == "string":
     - Check min_length, max_length
     - Check no caracteres inválidos (<, >, &, {, })
     - RETURN len(value) >= min_length AND len(value) <= max_length
   
   IF field_type == "text":
     - Check min_length, max_length
     - RETURN value != "" AND len(value) >= min_length
   
   IF field_type == "inci_list":
     - HELPER validate_inci_code(code: str) → bool:
       - INCI codes son uppercase ASCII alphanum + espacios
       - Check contra database INCI válidos (internacional standard)
       - RETURN code.isupper() AND is_valid_inci_code(code)
     
     - SI value is array:
       FOR EACH item in value:
         IF NOT validate_inci_code(item):
           RETURN False
       RETURN len(value) > 0
   
   IF field_type == "allergen_declaration":
     - SI rule.translation_mandatory == True:
       - Verificar texto está en idioma correcto (heuristic: palabras clave)
     - Verificar que contiene máx 14 alérgenos UE específicos
     - RETURN True si estructura correcta
   
   IF field_type == "enum":
     - RETURN value in rule.valid_values
   
   IF field_type == "float":
     - RETURN isinstance(value, (int, float)) AND value > 0
   
   IF field_type == "percentage":
     - RETURN isinstance(value, (int, float)) AND 0 <= value <= 100

3. RETORNAR result
```

#### SQLAlchemy Integration

```python
from sqlalchemy.orm import Session
import yaml

class ComplianceValidator:
    def __init__(self, rules_dir: str = "backend/legal_framework/rules"):
        self.rules = {}
        self.rules_cache = {}
        self._load_rules(rules_dir)
    
    def _load_rules(self, rules_dir: str):
        """Load all YAML rules"""
        for country_file in ["portugal_rules.yaml", "italy_rules.yaml", "spain_rules.yaml"]:
            with open(f"{rules_dir}/{country_file}") as f:
                country_rules = yaml.safe_load(f)
                country_code = country_rules["country_legal_framework"]["code"]
                self.rules[country_code] = country_rules
                
                # Build cache
                for family, family_rules in country_rules["country_legal_framework"]["regulations_by_family"].items():
                    for req_type in ["critical_requirements", "optional_requirements"]:
                        if req_type in family_rules:
                            for rule in family_rules[req_type]:
                                key = (country_code, family, rule["field"])
                                self.rules_cache[key] = rule
    
    def validate_for_country(self, sheet: ProductSheet, country: str) -> dict:
        try:
            # Get critical requirements
            country_rules = self.rules[country]
            family_rules = country_rules["country_legal_framework"]["regulations_by_family"].get(sheet.family, {})
            critical_reqs = family_rules.get("critical_requirements", [])
            
            issues = []
            for rule in critical_reqs:
                field_name = rule["field"]
                
                # Get field value
                if "." in field_name:  # Nested field (e.g., "title_short.pt")
                    parts = field_name.split(".")
                    value = getattr(sheet, parts[0], {})
                    if isinstance(value, dict):
                        value = value.get(parts[1], None)
                else:
                    value = getattr(sheet, field_name, None)
                
                # Validate
                is_valid = self.validate_field(field_name, value, country, sheet.family)
                
                if not is_valid:
                    issues.append({
                        "field_name": field_name,
                        "error_message": rule.get("error_message", "Invalid"),
                        "severity": rule.get("severity", "🔴 CRÍTICO"),
                        "example": rule.get("example", "N/A")
                    })
            
            # Calculate percentage
            valid_count = len(critical_reqs) - len(issues)
            percentage = int((valid_count / len(critical_reqs) * 100) if critical_reqs else 0)
            
            # Determine status
            if percentage == 100:
                status = "COMPLIANT"
            elif percentage >= 60:
                status = "WARNING"
            else:
                status = "NON_COMPLIANT"
            
            return {
                "country": country,
                "status": status,
                "percentage": percentage,
                "critical_issues": issues,
                "valid_count": valid_count,
                "total_critical_fields": len(critical_reqs)
            }
        
        except Exception as e:
            raise ValueError(f"Validation error for {country}: {str(e)}")
    
    def validate_field(self, field_name: str, value: any, country: str, family: str) -> bool:
        key = (country, family, field_name)
        rule = self.rules_cache.get(key)
        
        if not rule:
            return True  # Si no hay rule, asumir válido
        
        # Validaciones según type
        field_type = rule.get("field_type", "string")
        
        if field_type == "string":
            if value is None:
                return False
            return rule.get("min_length", 0) <= len(value) <= rule.get("max_length", 10000)
        
        elif field_type == "inci_list":
            if not isinstance(value, list):
                return False
            return all(self._is_valid_inci(item) for item in value) and len(value) > 0
        
        elif field_type == "enum":
            return value in rule.get("valid_values", [])
        
        elif field_type == "float":
            try:
                return float(value) > 0
            except:
                return False
        
        return True
    
    def _is_valid_inci(self, code: str) -> bool:
        """Validate INCI code"""
        # Implement INCI validation logic
        # INCI codes: uppercase, specific nomenclature
        return code.isupper() and len(code) > 0
```

#### Testing Strategy (35 tests)

```python
# test_compliance_validator.py

def test_validate_cosmetics_facial_portugal_compliant():
    """Ficha completa PT → COMPLIANT (100%)"""
    sheet = ProductSheet(family="COSMETICS_FACIAL", title_short_pt="Crema", description_detailed_pt="Desc", ...)
    result = validator.validate_for_country(sheet, "PT")
    assert result["status"] == "COMPLIANT"
    assert result["percentage"] == 100

def test_validate_cosmetics_facial_portugal_missing_title_pt():
    """Ficha sin title_short_pt → NON_COMPLIANT"""
    sheet = ProductSheet(family="COSMETICS_FACIAL", title_short_pt="", ...)
    result = validator.validate_for_country(sheet, "PT")
    assert result["status"] == "NON_COMPLIANT"
    assert any(c["field_name"] == "title_short_pt" for c in result["critical_issues"])

def test_validate_allergens_max_14_eu():
    """Alérgenos > 14 → inválido"""
    allergen_list = [f"Allergen{i}" for i in range(15)]  # 15 items
    assert not validator.validate_field("allergens_present", allergen_list, "PT", "FOOD_PACKAGED")

def test_validate_inci_valid_codes():
    """INCI válidos → True"""
    valid_inci = ["WATER", "GLYCERIN", "PHENOXYETHANOL"]
    assert validator.validate_field("inci_ingredients", valid_inci, "PT", "COSMETICS_FACIAL")

def test_validate_inci_empty_fails():
    """INCI vacía → False"""
    assert not validator.validate_field("inci_ingredients", [], "PT", "COSMETICS_FACIAL")

def test_validate_pao_valid_values():
    """PAO 6M/12M/18M/24M/36M → True"""
    for pao in ["6M", "12M", "18M", "24M", "36M"]:
        assert validator.validate_field("pao_symbol", pao, "PT", "COSMETICS_FACIAL")

def test_validate_pao_invalid_value():
    """PAO 5M → False"""
    assert not validator.validate_field("pao_symbol", "5M", "PT", "COSMETICS_FACIAL")

def test_compliance_percentage_100_when_all_critical_present():
    """100% when all critical fields present"""
    # Full sheet
    result = validator.validate_for_country(complete_sheet, "PT")
    assert result["percentage"] == 100

def test_compliance_percentage_60_when_half_missing():
    """60% when half critical fields missing"""
    # Half-complete sheet
    result = validator.validate_for_country(half_sheet, "PT")
    assert result["percentage"] == 50  # O similar

# ... + 25 más
```

---

### 3.3 PresetManager Completo

**backend/presets/150_families.yaml** (estructura simplificada con 10 ejemplos, expandir a 150):

```yaml
presets:
  COSMETICS_FACIAL:
    display_name: "Cosméticos Faciales"
    subfamilies:
      - "Cremas Hidratantes"
      - "Sérums"
      - "Máscaras"
      - "Limpiadoras"
      - "Tónicos"
    mode_of_use_es: "Aplicar pequeña cantidad en la cara limpia y masajear suavemente hasta absorción completa. Usar mañana y noche. Para otimizar resultados, combinar con serum y protetor solar."
    mode_of_use_pt: "Aplicar pequena quantidade no rosto limpo e massagiar suavemente até absorção completa. Usar manhã e noite. Para otimizar resultados, combinar com sérum e protetor solar."
    mode_of_use_it: "Applicare una piccola quantità sul viso pulito e massaggiare delicatamente fino al completo assorbimento. Utilizzare mattina e sera. Per risultati ottimali, combinare con siero e filtro solare."
    warnings_es: "Uso externo. Evitar contacto con los ojos. Si es irritante, suspender el uso inmediatamente. Mantener fuera del alcance de los niños. Usar siempre protetor solar SPF 30+ durante el día."
    warnings_pt: "Uso externo. Evitar contacto com os olhos. Se irritante, suspender o uso imediatamente. Manter fuera do alcance das crianças. Usar sempre protetor solar SPF 30+ durante o dia."
    warnings_it: "Uso esterno. Evitare il contatto con gli occhi. Se irritante, sospendere l'uso immediatamente. Tenere fuori dalla portata dei bambini. Utilizzare sempre filtro solare SPF 30+ durante il giorno."
    typical_allergens:
      - "PARFUM"
      - "LIMONENE"
      - "BENZYL ALCOHOL"
      - "PHENOXYETHANOL"
      - "SODIUM HYALURONATE"
    typical_pictograms:
      - "skin_irritation"
      - "eye_irritation"
      - "sensitive_skin"
    pao_default: "12M"
    natural_origin_range: "50-100%"

  COSMETICS_BODY:
    display_name: "Cosméticos Corporales"
    subfamilies:
      - "Cremas Corporales"
      - "Lociones Corporales"
      - "Geles de Ducha"
      - "Exfoliantes"
    mode_of_use_es: "Aplicar sobre la piel limpia y humedecida. Masajear suavemente hasta absorción completa. Usar diariamente, preferentemente por la noche."
    mode_of_use_pt: "Aplicar sobre a pele limpa e humedecida. Massagiar suavemente até absorção completa. Usar diariamente, preferencialmente à noite."
    mode_of_use_it: "Applicare sulla pelle pulita e inumidita. Massaggiare delicatamente fino al completo assorbimento. Utilizzare quotidianamente, preferibilmente di sera."
    warnings_es: "Uso externo. En caso de irritación, suspender el uso. Mantener fuera del alcance de los niños."
    warnings_pt: "Uso externo. Em caso de irritação, suspender o uso. Manter fuera do alcance das crianças."
    warnings_it: "Uso esterno. In caso di irritazione, sospendere l'uso. Tenere fuori dalla portata dei bambini."
    typical_allergens:
      - "PARFUM"
      - "LIMONENE"
      - "GLYCERIN"
    pao_default: "18M"
    natural_origin_range: "0-50%"

  FOOD_PACKAGED:
    display_name: "Alimentos Empaquetados"
    subfamilies:
      - "Snacks Salados"
      - "Bebidas"
      - "Conservas"
      - "Congelados"
      - "Chocolates"
    mode_of_use_es: "Almacenar en lugar fresco y seco, alejado de la luz solar directa. Consumir preferentemente antes de la fecha indicada en el envase."
    mode_of_use_pt: "Armazenar em local fresco e seco, afastado da luz solar direta. Consumir preferencialmente antes da data indicada na embalagem."
    mode_of_use_it: "Conservare in luogo fresco e asciutto, lontano dalla luce solare diretta. Consumare preferibilmente prima della data indicata sull'imballaggio."
    warnings_es: "Puede contener trazas de frutos secos (avellas, almendras), gluten y soja. No apto para celíacos. Contiene azúcar añadido."
    warnings_pt: "Pode conter trazas de frutos secos (avelãs, amêndoas), glúten e soja. Não adequado para celíacos. Contém açúcar adicionado."
    warnings_it: "Può contenere tracce di frutta secca (nocciole, mandorle), glutine e soia. Non adatto ai celiaci. Contiene zuccheri aggiunti."
    typical_allergens:
      - "Gluten"
      - "Frutos de cáscara"
      - "Soja"
      - "Leite"
      - "Ovos"
    pao_default: "24M"
    natural_origin_range: "0-50%"

  SUPPLEMENTS:
    display_name: "Suplementos Nutricionales"
    subfamilies:
      - "Vitaminas"
      - "Minerales"
      - "Aminoácidos"
      - "Probióticos"
    mode_of_use_es: "Tomar 1-2 cápsulas diarias con agua. No exceder la dosis recomendada. Consultar con un profesional sanitario antes de usar si está embarazada o en período de lactancia."
    mode_of_use_pt: "Tomar 1-2 cápsulas diárias com água. Não exceder a dose recomendada. Consultar um profissional de saúde antes de usar se estiver grávida ou amamentando."
    mode_of_use_it: "Assumere 1-2 capsule al giorno con acqua. Non superare la dose consigliata. Consultare un professionista della salute prima dell'uso se sei in gravidanza o allattamento."
    warnings_es: "Suplemento alimenticio, no medicamento. Consultar médico si está embarazada, lactancia o toma medicamentos. No recomendado en menores de 18 años."
    warnings_pt: "Suplemento alimentar, não medicamento. Consultar médico se está grávida, amamentando ou toma medicamentos. Não recomendado em menores de 18 anos."
    warnings_it: "Integratore alimentare, non un farmaco. Consultare un medico se sei in gravidanza, allattamento o assumi farmaci. Non consigliato per i minori di 18 anni."
    typical_allergens:
      - "Soja"
      - "Gluten"
      - "Leite"
    pao_default: "36M"

  # ... 146 familias más (COSMETICS_EYES, PERFUMES, SHAMPOOS, CONDITIONERS, TOOTHPASTES, etc.)
```

**Testing** (20 tests):
```python
def test_load_preset_returns_all_fields():
    """load_preset("COSMETICS_FACIAL") → completo"""
    preset = manager.load_preset("COSMETICS_FACIAL")
    assert "mode_of_use_es" in preset
    assert "warnings_pt" in preset
    assert "typical_allergens" in preset

def test_apply_preset_fills_empty_fields():
    """apply_preset rellena campos vacíos"""
    sheet = ProductSheet(family="COSMETICS_FACIAL", mode_of_use_es="")
    manager.apply_preset(sheet, "COSMETICS_FACIAL")
    assert sheet.mode_of_use_es != ""
    assert "masajear" in sheet.mode_of_use_es.lower()

def test_apply_preset_does_not_overwrite_existing():
    """apply_preset NO sobrescribe valores existentes"""
    original_text = "Custom mode of use"
    sheet = ProductSheet(family="COSMETICS_FACIAL", mode_of_use_es=original_text)
    manager.apply_preset(sheet, "COSMETICS_FACIAL")
    assert sheet.mode_of_use_es == original_text

def test_get_available_families_returns_150_families():
    """get_available_families() → 150+ familias"""
    families = manager.get_available_families()
    assert len(families) >= 150

def test_get_available_families_structure_correct():
    """Cada familia tiene código, display_name, subfamilies"""
    families = manager.get_available_families()
    for fam in families:
        assert "code" in fam
        assert "display_name" in fam
        assert "subfamilies" in fam

# ... + 15 más
```

---

### 3.4 TranslationEngine Completo

**backend/translations/translation_memory.json**:
```json
{
  "es-pt": {
    "Crema Hidratante": {
      "translations": ["Creme Hidratante"],
      "count": 5,
      "confidence": 0.98
    },
    "Modo de Empleo": {
      "translations": ["Modo de Emprego"],
      "count": 3,
      "confidence": 0.99
    },
    "Advertencia": {
      "translations": ["Aviso"],
      "count": 2,
      "confidence": 0.95
    },
    "Sin Gluten": {
      "translations": ["Sem Glúten"],
      "count": 1,
      "confidence": 0.90
    }
  },
  "es-it": {
    "Crema Hidratante": {
      "translations": ["Crema Idratante"],
      "count": 4,
      "confidence": 0.97
    },
    "Aviso": {
      "translations": ["Avvertenza"],
      "count": 2,
      "confidence": 0.93
    }
  },
  "es-en": {
    "Crema": {
      "translations": ["Cream"],
      "count": 10,
      "confidence": 0.99
    },
    "Modo de Empleo": {
      "translations": ["Instructions for use", "How to use"],
      "count": 5,
      "confidence": 0.98
    }
  }
}
```

**backend/translations/glossaries/glossary_cosmetics_pt.yaml**:
```yaml
COSMETICS_FACIAL:
  "Crema Hidratante": "Creme Hidratante"
  "Crema Antiarrugas": "Creme Anti-rugas"
  "Sérum": "Sérum"
  "Máscara": "Máscara"
  "Limpiadora": "Limpadora"
  "Modo de Empleo": "Modo de Emprego"
  "Aviso": "Aviso"
  "Alérgeno": "Alergénio"
  "Ingrediente": "Ingrediente"
  "Composición": "Composição"
  "Aplicar": "Aplicar"
  "Absorción": "Absorção"
  "Irritación": "Irritação"

FOOD_PACKAGED:
  "Sin Gluten": "Sem Glúten"
  "Alérgeno": "Alergénio"
  "Conservante": "Conservante"
  "Azúcar": "Açúcar"
  "Sal": "Sal"
  "Almacenamiento": "Armazenamento"
  "Caducidad": "Data de Validade"
```

**Methods**:
```python
class TranslationEngine:
    def __init__(self):
        self.memory = self._load_translation_memory()
        self.glossaries = self._load_glossaries()
    
    def suggest_translation(self, source_text: str, source_lang: str, target_lang: str, threshold: float = 0.75) -> List[str]:
        """Suggest translations with fuzzy matching"""
        suggestions = []
        key = f"{source_lang}-{target_lang}"
        
        if key not in self.memory:
            return []
        
        # Exact match
        if source_text in self.memory[key]:
            return self.memory[key][source_text]["translations"]
        
        # Fuzzy match
        for stored_text, data in self.memory[key].items():
            ratio = difflib.SequenceMatcher(None, source_text.lower(), stored_text.lower()).ratio()
            if ratio >= threshold:
                suggestions.extend([(t, ratio) for t in data["translations"]])
        
        # Sort by confidence descending
        suggestions = sorted(suggestions, key=lambda x: x[1], reverse=True)
        return [s[0] for s in suggestions[:5]]  # Top 5
    
    def save_translation(self, source_text: str, target_text: str, source_lang: str, target_lang: str):
        """Save translation to memory"""
        key = f"{source_lang}-{target_lang}"
        
        if key not in self.memory:
            self.memory[key] = {}
        
        if source_text not in self.memory[key]:
            self.memory[key][source_text] = {
                "translations": [],
                "count": 0,
                "confidence": 0.0
            }
        
        self.memory[key][source_text]["translations"].append(target_text)
        self.memory[key][source_text]["count"] += 1
        
        # Persist
        with open("backend/translations/translation_memory.json", "w") as f:
            json.dump(self.memory, f, indent=2)
    
    def get_glossary(self, family: str, target_lang: str) -> dict:
        """Get glossary for family and language"""
        file_path = f"backend/translations/glossaries/glossary_{family.lower()}_{target_lang.lower()}.yaml"
        if family.lower() in self.glossaries and target_lang.lower() in self.glossaries[family.lower()]:
            return self.glossaries[family.lower()][target_lang.lower()]
        return {}
```

---

### 3.5 ImportExportManager Completo

**Methods - Pseudocódigo**:

#### generate_excel_template()
```
1. Usar openpyxl.Workbook()
2. Crear sheet "Productos"
3. Row 1 - Headers (60+ columnas):
   SKU, EAN_PRIMARY, EAN_SECONDARY, TITLE_ES_SHORT, TITLE_PT_SHORT, TITLE_IT_SHORT, BRAND, GAMA_ES, FAMILY, SUBFAMILY, NET_WEIGHT_VALUE, NET_WEIGHT_UNIT, GROSS_WEIGHT_VALUE, GROSS_WEIGHT_UNIT, HEIGHT_CM, WIDTH_CM, DEPTH_CM, FORMAT_TYPE, FORMAT_MATERIAL, FORMAT_CLOSURE, PACKAGING_LANGUAGES, INCI_INGREDIENTS, KEY_INGREDIENTS, MODE_OF_USE_ES, MODE_OF_USE_PT, MODE_OF_USE_IT, WARNINGS_ES, WARNINGS_PT, WARNINGS_IT, ALLERGENS_PRESENT, ALLERGENS_MAY_CONTAIN, PAO, PICTOGRAMS, CERTIFICATIONS, MADE_IN_TEXT, DISTRIBUTOR_NAME, DISTRIBUTOR_CIF, RESPONSIBLE_PERSON_NAME, RESPONSIBLE_PERSON_EMAIL, NATURAL_ORIGIN_PERCENTAGE, ... (60+ total)

4. Row 2 - Ejemplos (datos demo)

5. Datavalidation dropdowns:
   - FAMILY (col 10): 150 opciones
   - FORMAT_TYPE (col 19): Botella, Tubo, Tarro, Caja, Bolsa
   - FORMAT_MATERIAL (col 20): Plástico, Vidrio, Aluminio, Cartón, Metal
   - PAO (col 32): 6M, 12M, 18M, 24M, 36M
   - NET_WEIGHT_UNIT (col 12): g, ml, kg, L

6. Color-coding headers:
   - Red fill (#FF0000) para critical fields (SKU, TITLE_ES, INCI, ALLERGENS)
   - Yellow fill (#FFFF00) para recommended
   - White para optional

7. Freeze header row: ws.freeze_panes = "A2"
8. Autosize columns: for col in ws.columns: ws.column_dimensions[col[0].column_letter].width = 20

9. RETORNAR bytes via BytesIO()
```

#### import_from_excel(file_path: str) → dict
```
1. ws = openpyxl.load_workbook(file_path).active
2. errors = []
3. skipped = 0
4. imported = 0

5. ITERAR filas (skip header+ejemplo, start from row 3):
   FOR row_idx, row in enumerate(ws.iter_rows(min_row=3), start=3):
     row_data = {header[col_idx].value: row[col_idx].value 
                 for col_idx, header in enumerate(ws[1])}
     
     # Validaciones básicas
     sku = row_data.get("SKU")
     if not sku or len(str(sku).strip()) == 0:
       errors.append({"row": row_idx, "error": "SKU vacío"})
       continue
     
     if not re.match(r'^[A-Z]{2}-[A-Z0-9]{3}-[0-9]{3}$', sku):  # Ej: CF-HYD-001
       errors.append({"row": row_idx, "sku": sku, "error": "SKU formato inválido"})
       continue
     
     # Validar EAN
     ean = row_data.get("EAN_PRIMARY")
     if ean:
       if not validate_ean13_checksum(ean):
         errors.append({"row": row_idx, "sku": sku, "error": "EAN checksum inválido"})
         continue
     
     # Validar FAMILY
     family = row_data.get("FAMILY")
     if family not in VALID_FAMILIES_150:
       errors.append({"row": row_idx, "sku": sku, "error": f"FAMILY '{family}' no válida"})
       continue
     
     # Validar campos requeridos
     title_es = row_data.get("TITLE_ES_SHORT")
     if not title_es or len(str(title_es).strip()) < 3:
       errors.append({"row": row_idx, "sku": sku, "error": "TITLE_ES_SHORT min 3 chars"})
       continue
     
     # Si todas validaciones OK:
     try:
       sheet = ProductSheet(
         sku=sku,
         ean_list=[ean] if ean else [],
         brand=row_data.get("BRAND"),
         family=family,
         subfamily=row_data.get("SUBFAMILY"),
         title_short={
           "es": row_data.get("TITLE_ES_SHORT"),
           "pt": row_data.get("TITLE_PT_SHORT"),
           "it": row_data.get("TITLE_IT_SHORT")
         },
         net_weight_value=float(row_data.get("NET_WEIGHT_VALUE", 0)) or None,
         net_weight_unit=row_data.get("NET_WEIGHT_UNIT"),
         # ... (mapear todos los campos)
       )
       
       # Aplicar preset
       preset_manager.apply_preset(sheet, family)
       
       # Guardar en DB
       session.add(sheet)
       session.flush()  # Para obtener ID
       
       # Crear v1.0 snapshot
       version_manager.create_snapshot(sku, "major", "Imported from Excel", current_user_id)
       
       imported += 1
     except Exception as e:
       errors.append({"row": row_idx, "sku": sku, "error": str(e)})
       session.rollback()

6. session.commit()

7. # Calcular completion percentage
   if imported > 0:
     total_fields_possible = imported * 60  # 60 campos por producto
     total_fields_filled = sum(count_non_empty_fields(sheet) for sheet in imported_sheets)
     completion_percentage = int((total_fields_filled / total_fields_possible) * 100)
   else:
     completion_percentage = 0

8. RETORNAR:
   {
     "imported": imported,
     "errors": errors,
     "skipped": skipped,
     "status": "SUCCESS" if imported > 0 else "FAILED",
     "completion_percentage": completion_percentage,
     "message": f"{imported} productos importados exitosamente. {len(errors)} errores."
   }
```

#### export_to_pdf(sku: str) → bytes
```
Usar ReportLab library (reportlab.pdfgen, reportlab.platypus):

1. Crear Canvas A4 (210x297mm)
2. Header section (top 40mm):
   - Logo placeholder 20x20mm top-left
   - Título "FICHA DE PRODUCTO"
   - SKU + EAN
3. Body 2-column layout (60% | 40%):
   LEFT (60%):
     - General Info table (SKU, EAN, Brand, Family, Subfamily)
     - Physical Properties table (dimensions, weight, format)
     - Composition table (INCI list)
     - Mode of Use section (multiidioma justified text)
   RIGHT (40%):
     - Metadata (Made In con flags, Distributor, Responsible Person)
     - Natural Origin %
     - Certifications list
4. Warnings section (highlight rojo con ⚠️ icon)
5. Images section (3 product photos centradas)
6. Compliance footer (3 badges 🇵🇹 | 🇮🇹 | 🇪🇸 con percentages)
7. Page numbers, date generated

RETORNAR bytes via BytesIO()
```

---

## 6️⃣ API ROUTES COMPLETADAS

**backend/routes/versions.py**:
```python
@router.get("/api/products/{sku}/versions")
def get_versions(sku: str, session: Session) → List[dict]:
    """GET /api/products/CF-HYD-001/versions
    RESPONSE: [{version_number: "1.1", snapshot_date, created_by, change_summary, changes_count}, ...]"""

@router.get("/api/products/{sku}/versions/{version}")
def get_snapshot(sku: str, version: str, session: Session) → dict:
    """GET /api/products/CF-HYD-001/versions/1.0
    RESPONSE: {sku, version_number, complete snapshot fields...}"""

@router.get("/api/products/{sku}/versions/compare")
def compare_versions(sku: str, from_version: str, to_version: str, session: Session) → dict:
    """GET /api/products/CF-HYD-001/versions/compare?from_version=1.0&to_version=1.1
    RESPONSE: {from_version, to_version, stats: {added, updated, deleted, critical}, changes: List[...]}"""

@router.post("/api/products/{sku}/versions/{version}/restore")
def restore_version(sku: str, version: str, session: Session, current_user: User) → dict:
    """POST /api/products/CF-HYD-001/versions/1.0/restore
    RESPONSE: {sku, new_version_number, message}"""
```

**backend/routes/legal.py**, **routes/import_export.py**, **routes/images.py**: similar structure

---

## 7️⃣ FRONTEND IMPLEMENTATION DETAILS

### Pinia Stores - Actions

```javascript
// stores/productStore.js

const productStore = defineStore('product', () => {
  const products = ref([])
  const currentProduct = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const filters = ref({
    family: '',
    brand: '',
    status: '',
    languages: [],
    search: ''
  })
  const pagination = ref({
    page: 1,
    perPage: 12,
    total: 0
  })

  const fetchProducts = async (newFilters = {}, page = 1) => {
    loading.value = true
    try {
      const params = { ...filters.value, ...newFilters, page, per_page: pagination.value.perPage }
      const response = await productService.listSheets(params)
      products.value = response.data.products
      pagination.value.total = response.data.total
      filters.value = { ...filters.value, ...newFilters }
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const getProduct = async (sku) => {
    loading.value = true
    try {
      const response = await productService.getSheet(sku)
      currentProduct.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const createProduct = async (data) => {
    try {
      const response = await productService.createSheet(data)
      products.value.unshift(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const updateProduct = async (sku, data) => {
    try {
      const response = await productService.updateSheet(sku, data)
      const index = products.value.findIndex(p => p.sku === sku)
      if (index !== -1) products.value[index] = response.data
      if (currentProduct.value?.sku === sku) currentProduct.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const deleteProduct = async (sku) => {
    try {
      await productService.deleteSheet(sku)
      products.value = products.value.filter(p => p.sku !== sku)
      if (currentProduct.value?.sku === sku) currentProduct.value = null
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return {
    products,
    currentProduct,
    loading,
    error,
    filters,
    pagination,
    fetchProducts,
    getProduct,
    createProduct,
    updateProduct,
    deleteProduct
  }
})
```

### Vue Component Example - LegalAlerts

```vue
<template>
  <div v-if="!loading" class="legal-alerts-grid">
    <div v-for="country in ['PT', 'IT', 'ES']" :key="country" class="compliance-card">
      <div class="card-header">
        <span :class="`flag flag-${country.toLowerCase()}`">🚩</span>
        <h3>{{ countryNames[country] }}</h3>
      </div>
      
      <div class="compliance-percentage">
        <div class="percentage-value">
          {{ complianceData[country]?.percentage || 0 }}%
        </div>
        <div class="progress-bar">
          <div :style="{ width: (complianceData[country]?.percentage || 0) + '%' }" 
               :class="`progress-fill status-${complianceData[country]?.status.toLowerCase()}`"></div>
        </div>
      </div>
      
      <div class="status-badge" :class="`status-${complianceData[country]?.status.toLowerCase()}`">
        {{ complianceData[country]?.status }}
      </div>
      
      <button v-if="complianceData[country]?.critical_issues.length" 
              @click="expandedCountry = expandedCountry === country ? null : country"
              class="btn btn-secondary btn-sm">
        Ver Detalles ({{ complianceData[country]?.critical_issues.length }} issues)
      </button>
      
      <div v-if="expandedCountry === country" class="issues-list">
        <div v-for="issue in complianceData[country]?.critical_issues" :key="issue.field_name" class="issue-item">
          <span class="severity">{{ issue.severity }}</span>
          <span class="field">{{ issue.field_name }}</span>
          <p class="error">{{ issue.error_message }}</p>
          <p class="example">Ej: {{ issue.example }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useLegalStore } from '@/stores/legalStore'

const props = defineProps({ sku: String })

const legalStore = useLegalStore()
const loading = ref(false)
const expandedCountry = ref(null)
const complianceData = ref({})

const countryNames = {
  PT: 'Portugal (INFARMED)',
  IT: 'Italia (Ministero)',
  ES: 'España (AEMPS)'
}

const fetchCompliance = async () => {
  loading.value = true
  try {
    const countries = ['PT', 'IT', 'ES']
    for (const country of countries) {
      const result = await legalStore.validateCompliance(props.sku, country)
      complianceData.value[country] = result
    }
  } finally {
    loading.value = false
  }
}

onMounted(fetchCompliance)
watch(() => props.sku, fetchCompliance)
</script>

<style scoped>
.legal-alerts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.compliance-card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  background: var(--color-surface);
}

.compliance-percentage {
  margin: 1rem 0;
}

.progress-bar {
  height: 6px;
  background: var(--color-secondary);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s;
}

.progress-fill.status-compliant { background: var(--color-success); }
.progress-fill.status-warning { background: var(--color-warning); }
.progress-fill.status-non_compliant { background: var(--color-critical); }

.status-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-full);
  font-weight: 500;
  margin-top: 1rem;
}

.status-badge.status-compliant {
  background: rgba(16, 185, 129, 0.15);
  color: var(--color-success);
}

.issues-list {
  margin-top: 1rem;
  border-top: 1px solid var(--color-border);
  padding-top: 1rem;
}

.issue-item {
  margin-bottom: 1rem;
}

.issue-item .severity { margin-right: 0.5rem; }
.issue-item .field { font-weight: 500; }
.issue-item .error { font-size: 0.875rem; color: var(--color-critical); margin: 0.5rem 0; }
.issue-item .example { font-size: 0.75rem; color: var(--color-text-secondary); font-style: italic; margin: 0; }
</style>
```

---

## 8️⃣ TESTING COMPREHENSIVE

**Backend Testing Setup**:
```bash
# pytest.ini
[pytest]
testpaths = backend/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=backend --cov-report=html --cov-report=term-missing

# Run: pytest backend/ --cov=backend -v
# Target: 80%+ coverage
```

**Frontend Testing Setup**:
```bash
# vitest.config.js
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'frontend/dist/']
    }
  }
})

# Run: npm run test:unit -- --coverage
# Target: 70%+ coverage
```

---

## 9️⃣ ROADMAP FUTURO (DESPUÉS MVP)

**v1.1.0 (Q1 2026)**:
- Multi-usuario con roles (Admin/Editor/Traductor/Revisor)
- Comentarios en fichas
- Workflow aprobación
- WebSocket notifications real-time
- Redis caching

**v1.2.0 (Q2 2026)**:
- Francia, Alemania, UK legal frameworks
- API pública + rate limiting + OAuth2
- Webhooks integraciones ERP

**v1.3.0 (Q3 2026)**:
- Traducción automática GPT-4
- IA suggestions compliance
- OCR para imágenes

**v2.0.0 (Q4 2026)**:
- SaaS cloud AWS/Azure
- App móvil iOS/Android
- Offline sync
- Backups automáticos cloud

---

**ÚLTIMA ACTUALIZACIÓN**: 16 Diciembre 2025 | **VERSIÓN**: 1.0.0 | **STATUS**: Especificación Completa