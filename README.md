# Revisiones-Traducciones-Ultimate

**Sistema Web Profesional para Gestión de Fichas de Producto Multiidioma con Compliance Regulatorio**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg) ![Python](https://img.shields.io/badge/python-3.11+-blue.svg) ![Vue.js](https://img.shields.io/badge/vue.js-3.4+-green.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-teal.svg)

---

## ⚡ Inicio Rápido (2 Comandos)

```bash
# 1. Instalar dependencias
python launcher.py --install

# 2. Iniciar aplicación (backend + frontend automático)
python launcher.py
```

**¡Listo!** La aplicación creará automáticamente la base de datos SQLite, inicializará las tablas y arrancará en:
- **Backend API**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173 (si está configurado)

**Sin Docker. Sin PostgreSQL. Sin configuración manual.** 🎉

[Ver Guía Completa de Instalación →](QUICKSTART.md)

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características Principales](#características-principales)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Arquitectura](#arquitectura)
- [API REST](#api-rest)
- [Tests](#tests)
- [Contribuir](#contribuir)
- [Roadmap](#roadmap)
- [Licencia](#licencia)

---

## 🎯 Descripción

**Revisiones-Traducciones-Ultimate** es una aplicación web de calidad profesional diseñada para **centralizar y automatizar la gestión de fichas de producto** con enfoque en: ✅ **Traducción multiidioma**: ES, PT, IT, EN, FR, BR ✅ **Compliance regulatorio automático**: Portugal (INFARMED), Italia (Ministero della Salute), España (AEMPS) ✅ **Versionado completo**: Snapshots, changelog, diff visual, timeline interactiva ✅ **Catalogación avanzada**: 150+ familias de productos con presets automáticos ✅ **Importación/Exportación masiva**: Excel, PDF, Markdown ✅ **Web scraping de imágenes**: Búsqueda automática en internet ✅ **Interfaz profesional**: Design system corporativo, animaciones suaves, responsive

### ¿Para quién es?

- Fabricantes de cosméticos que necesitan traducir fichas técnicas
- Distribuidores de alimentos con productos multicategoría
- Importadores/Exportadores con cumplimiento regulatorio
- Equipos de compliance regulatorio
- Traductores especializados en etiquetado

### Problema que Resuelve

❌ Traducciones manuales inconsistentes ❌ Pérdida de versiones anteriores ❌ Desconocimiento de regulaciones locales ❌ Falta de trazabilidad de cambios ❌ Exportación manual a múltiples formatos

✅ **Revisiones-Traducciones-Ultimate** automatiza, valida y centraliza todo el proceso

---

## ✨ Características Principales

### 🌍 Sistema Multiidioma Avanzado

- **6 idiomas soportados**: ES, PT, IT, EN, FR, BR
- **Translation Memory**: Reutiliza traducciones previas automáticamente
- **Glossarios especializados**: Por familia de producto (cosmética, alimentación, suplementos, etc.)
- **Validación de traducciones críticas**: Alertas para campos obligatorios por país

### ⚖️ Marco Legal Integrado

- **3 países soportados**: Portugal (INFARMED), Italia (Ministero della Salute), España (AEMPS)
- **150+ reglas de compliance** pre-configuradas
- **Validación automática** de requisitos críticos y opcionales
- **Alertas visuales**: 🔴 Crítico, 🟡 Warning, 🟢 OK
- **Exportación de reportes** de compliance por país

### 📦 Gestión Completa de Fichas

**Información General:**
- SKU (código único), EAN (hasta 20), Marca, Gama, Familia (150+ categorías)
- Títulos cortos y descripciones detalladas multiidioma

**Propiedades Físicas:**
- Peso neto/bruto, dimensiones, volumen
- Tipo de formato (botella, tubo, tarro, caja, etc.)
- Material y tipo de cierre

**Envase y Etiquetado:**
- Visualización 3D interactiva del envase
- 6 posiciones de etiqueta: Frontal, Trasera, Lateral izq/dcha, Superior, Inferior
- 40+ pictogramas estándar (reciclaje, advertencias, certificaciones)
- PAO (Period After Opening): 6M, 12M, 18M, 24M, 36M

**Composición:**
- Lista INCI completa
- Alérgenos (presentes, trazas, libre de)
- % de ingredientes de origen natural con certificación

**Modo de Empleo:**
- Instrucciones multiidioma
- Frecuencia y zona de aplicación

**Precauciones:**
- Advertencias generales y específicas
- Condiciones de almacenamiento
- Restricciones especiales

**Metadata Regulatorio:**
- Made In (país con auto-traducción a 5 idiomas)
- Distribuidor (empresa, CIF, direcciones)
- Persona Responsable (R.P.)
- Certificaciones (Orgánico, Cruelty-Free, Vegan, ISO, etc.)

### 🔄 Sistema de Versionado Completo

- **Snapshots automáticos**: Captura estado completo en cada cambio
- **Changelog granular**: Qué cambió exactamente (field-level)
- **Timeline visual**: Historial gráfico de revisiones
- **Comparador Diff**: Visualización side-by-side con highlighting
- **Restauración**: Volver a versiones anteriores
- **Auditoría**: Quién cambió qué y cuándo

### 📊 Catálogo y Dashboard

- **Vista Grid profesional**: Cards con thumbnails, badges de idiomas, status de compliance
- **Filtros avanzados**: Familia, marca, estado, idioma, país
- **Búsqueda instantánea**: Por SKU, EAN, título
- **Estadísticas en tiempo real**: Productos, familias, marcas, idiomas
- **Compliance Dashboard**: Estado por país con porcentajes

### 📥 Importación/Exportación

**Importación:**
- Template Excel generado automáticamente
- Importación masiva (100+ fichas en segundos)
- Validación en import (campos obligatorios)
- Status post-import (indica campos pendientes)

**Exportación:**
- PDF: Fichas profesionales con imágenes y pictogramas
- Excel: Catálogo completo exportable
- Markdown: Para documentación o GitHub
- HTML: Fichas responsive para web

### 🖼️ Gestión de Imágenes

- Upload manual (drag & drop)
- Web Scraping automático con preview
- 6 tipos de imagen: Frontal, Trasera, Laterales, Superior, Inferior, Lifestyle
- Validación (resolución mínima, formato, tamaño)

### 🎨 Interfaz Web Profesional

- **Design System corporativo**: Paleta consistente, tipografía, espaciado
- **40+ Pictogramas SVG**: Reciclaje, advertencias, certificaciones, PAO
- **Animaciones suaves**: Transitions 150-400ms
- **Responsive Design**: Desktop-first, adaptable a tablets
- **Micro-interactions**: Tooltips, hover effects, loading states

---

## 💻 Requisitos del Sistema

### Software Requerido

**Backend:**
- Python 3.11 o superior
- PostgreSQL 14 o superior
- pip (gestor de paquetes)

**Frontend:**
- Node.js 18 o superior
- npm 9 o superior

**Opcional:**
- Git (control de versiones)
- Docker (containerización)

### Hardware Recomendado

- **CPU**: 4 cores
- **RAM**: 8 GB mínimo (16 GB recomendado)
- **Almacenamiento**: 10 GB libres
- **Conexión**: Internet para web scraping

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/partybrasil/Revisiones-Traducciones-Ultimate.git
cd Revisiones-Traducciones-Ultimate
```

### 2. Backend Setup

#### 2.1. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.2. Instalar Dependencias

Opción 1 - Usar el launcher (recomendado):
```bash
python launcher.py --install
```

Opción 2 - Manual:
```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

**Dependencias principales:**
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pydantic==2.5.3
pydantic-settings==2.1.0
alembic==1.13.1
openpyxl==3.1.2
reportlab==4.0.9
python-markdown==3.5.2
beautifulsoup4==4.12.3
selenium==4.17.2
aiofiles==23.2.1
pytest==7.4.4
pytest-asyncio==0.23.3
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pyyaml==6.0.1
```

#### 2.3. Configurar Base de Datos

```bash
# Crear PostgreSQL
createdb revisiones_traducciones_db

# O usando psql
psql -U postgres
CREATE DATABASE revisiones_traducciones_db;
\q
```

#### 2.4. Variables de Entorno

Crear `backend/.env`:

```bash
cp backend/.env.example backend/.env
```

Editar el archivo `.env`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/revisiones_traducciones_db
SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760
HOST=0.0.0.0
PORT=8000
```

#### 2.5. Inicializar Base de Datos

```bash
cd backend
python init_db.py
```

Esto creará las tablas, cargará los presets y creará un producto de ejemplo.

#### 2.6. Iniciar Backend

Opción 1 - Usar el launcher (recomendado):
```bash
python launcher.py
```

Opción 2 - Manual:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend disponible en: **http://localhost:8000**
Documentación API (Swagger): **http://localhost:8000/docs**

### 3. Frontend Setup

#### 3.1. Instalar Dependencias

```bash
cd frontend
npm install
```

#### 3.2. Variables de Entorno

Crear `frontend/.env`:

```bash
cp frontend/.env.example frontend/.env
```

El archivo ya tiene la configuración por defecto:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_ENABLE_WEB_SCRAPING=true
VITE_MAX_IMAGE_SIZE=10485760
```

#### 3.3. Iniciar Frontend

```bash
npm run dev
```

Frontend disponible en: **http://localhost:5173**

---

## 🎮 Uso del Launcher

El launcher simplifica el inicio de la aplicación. Comandos disponibles:

```bash
# Iniciar backend (por defecto)
python launcher.py

# Iniciar backend sin auto-reload
python launcher.py --no-reload

# Iniciar backend en puerto personalizado
python launcher.py --port 8080

# Iniciar frontend
python launcher.py --frontend

# Instalar/actualizar todas las dependencias
python launcher.py --install

# Saltar verificaciones de inicio
python launcher.py --skip-checks

# Ver ayuda
python launcher.py --help
```

**Ejecución Completa:**

En Terminal 1:
```bash
python launcher.py
```

En Terminal 2:
```bash
python launcher.py --frontend
```

---

## ⚙️ Configuración

### Marco Legal

Archivos YAML en `backend/legal_framework/`:

```yaml
# portugal_rules.yaml
portugal_legal_framework:
  country: "Portugal"
  code: "PT"
  authority: "INFARMED"
  cosmetics_facial:
    critical_requirements:
      - field: "title_short_pt"
        translation_mandatory: true
        tag: "🔴 CRÍTICO"
        error_message: "Falta título en português"
```

### Presets

Archivos YAML en `backend/presets/`:

```yaml
# cosmetics_facial_presets.yaml
cosmetics_facial_preset:
  family: "COSMETICS_FACIAL"
  mode_of_use:
    es: "Aplicar una cantidad adecuada sobre el rostro limpio..."
    pt: "Aplicar quantidade adequada sobre o rosto limpo..."
```

### Translation Memory

Editar `backend/translations/translation_memory.json`:

```json
{
  "glossary": {
    "Crema hidratante": {
      "pt": "Creme hidratante",
      "it": "Crema idratante"
    }
  }
}
```

---

## 📖 Uso

### Crear Nueva Ficha

1. **Dashboard** → "➕ Crear Nueva Ficha"
2. **Pestaña General**: SKU, EAN, Título ES, Familia (carga preset automático)
3. **Pestaña Envase**: Editar posiciones 3D, seleccionar idiomas, pictogramas, PAO
4. **Pestaña Composición**: INCI, alérgenos, % natural origin
5. **Pestaña Legal**: Made In, Distribuidor, R.P., revisar compliance por país
6. **Pestaña Imágenes**: Subir o buscar imágenes
7. **Guardar** → Se crea versión 1.0 automáticamente

### Traducir a Portugués

1. **Abrir ficha** en editor
2. **Pestaña Traducción** → Seleccionar Portugués (PT)
3. **Completar campos críticos**:
   - Título Corto PT (🔴 CRÍTICO para Portugal)
   - Descripción Detallada PT
   - Modo de Empleo PT
   - Alérgenos PT
   - Precauciones PT
4. **Guardar** → Nueva versión automática (v1.1)

### Ver Historial de Versiones

1. **Abrir ficha** → "Historial de Versiones"
2. **Timeline muestra**:
   - v2.3 (Actual) - Actualización de Traducción
   - v2.2 (Archivado) - Traducción Completa a Portugués
   - v2.1 (Archivado) - Revisión de Compliance España
   - v2.0 (Original) - Ficha Inicial Creada
3. **Acciones**: Ver Snapshot, Comparar, Restaurar

### Comparar Versiones

1. **Historial** → "Comparar con anterior"
2. **Seleccionar versiones** (v2.2 → v2.3)
3. **Diff Viewer muestra**:
   - 5 cambios totales
   - 3 añadidos (verde), 2 actualizados (amarillo)
   - Detalles de cada cambio con highlighting

### Importar Masivamente

1. **Dashboard** → "📥 Importar Masivo"
2. **Descargar template Excel** con columnas
3. **Rellenar template** (cada fila = 1 producto)
4. **Subir Excel** → Sistema valida y importa
5. **Resultado** → Indica productos importados y campos pendientes

### Exportar Catálogo

1. **Catálogo** → "📤 Exportar"
2. **Seleccionar formato**: PDF, Excel, Markdown
3. **Configurar**: productos, idiomas, incluir imágenes
4. **Descargar** archivo generado

---

## 🏗️ Arquitectura

### Diagrama de Arquitectura

```
┌──────────────────────────────────────────┐
│          FRONTEND (Vue.js 3)             │
│  Dashboard | Catalog | Editor | Legal    │
│     ↑                                    │
│     └─ Axios HTTP Client                │
└──────────────────────────────────────────┘
                    │ REST API
                    ↓
┌──────────────────────────────────────────┐
│        BACKEND (FastAPI + Python)        │
│  Routes → Managers → Models → Database   │
└──────────────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────┐
│      PostgreSQL + JSONB Storage          │
│  products | versions | changelog | rules │
└──────────────────────────────────────────┘
```

### Estructura de Directorios

```
Revisiones-Traducciones-Ultimate/
├── backend/
│   ├── core/
│   │   ├── product_sheet_manager.py
│   │   ├── version_manager.py
│   │   ├── preset_manager.py
│   │   ├── legal_framework_engine.py
│   │   └── import_export_manager.py
│   ├── models/
│   │   ├── product_sheet.py
│   │   ├── product_version.py
│   │   └── legal_rule.py
│   ├── legal_framework/
│   │   ├── portugal_rules.yaml
│   │   ├── italy_rules.yaml
│   │   ├── spain_rules.yaml
│   │   └── compliance_validator.py
│   ├── presets/
│   │   ├── cosmetics_facial_presets.yaml
│   │   ├── food_packaged_presets.yaml
│   │   └── [150+ presets]
│   ├── translations/
│   │   ├── translation_memory.json
│   │   ├── glossary_cosmetics.yaml
│   │   └── translation_engine.py
│   ├── import_export/
│   │   ├── excel_template_generator.py
│   │   ├── bulk_importer.py
│   │   ├── pdf_exporter.py
│   │   ├── markdown_exporter.py
│   │   └── html_exporter.py
│   ├── image_handler/
│   │   ├── image_scraper.py
│   │   ├── image_storage.py
│   │   └── web_search.py
│   ├── api/
│   │   ├── routes_products.py
│   │   ├── routes_versions.py
│   │   ├── routes_legal.py
│   │   ├── routes_import.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProductSheetEditor.vue
│   │   │   ├── CatalogViewer.vue
│   │   │   ├── LegalAlerts.vue
│   │   │   ├── VersionHistory.vue
│   │   │   └── DiffViewer.vue
│   │   ├── views/
│   │   │   ├── Dashboard.vue
│   │   │   ├── CreateSheet.vue
│   │   │   ├── EditSheet.vue
│   │   │   └── CatalogView.vue
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── versionService.js
│   │   │   └── legalService.js
│   │   └── App.vue
│   ├── .env.example
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── .github/
│   ├── extended_memory.md
│   └── workflows/
│       └── ci.yml
│
├── docker-compose.yml
├── Dockerfile
├── README.md
└── LICENSE
```

---

## 🔌 API REST

### Documentación Completa

Accede a **http://localhost:8000/docs** para Swagger UI interactivo

### Endpoints Principales

**Products:**
```http
GET    /api/products                    # Listar productos
POST   /api/products                    # Crear producto
GET    /api/products/{sku}              # Obtener producto
PUT    /api/products/{sku}              # Actualizar producto
DELETE /api/products/{sku}              # Eliminar producto
```

**Versions:**
```http
GET    /api/products/{sku}/versions     # Listar versiones
GET    /api/products/{sku}/versions/{v} # Obtener snapshot
POST   /api/products/{sku}/versions     # Crear snapshot
GET    /api/products/{sku}/changelog/compare?from=X&to=Y  # Comparar
```

**Legal:**
```http
GET    /api/legal/{country}/rules       # Obtener reglas país
POST   /api/legal/validate              # Validar compliance
GET    /api/products/{sku}/compliance/{country}  # Estado compliance
```

**Import/Export:**
```http
GET    /api/import/template             # Template Excel
POST   /api/import/excel                # Importar
GET    /api/export/pdf/{sku}            # Exportar PDF
GET    /api/export/markdown/{sku}       # Exportar Markdown
```

### Ejemplo: Comparar Versiones

```bash
curl -X GET "http://localhost:8000/api/products/CF-HYD-001/changelog/compare?from=2.1&to=2.2"
```

**Response:**
```json
{
  "version_from": "2.1",
  "version_to": "2.2",
  "total_changes": 12,
  "changes": [
    {
      "field": "regulatory_metadata.made_in.country_code",
      "old_value": null,
      "new_value": "FR",
      "change_type": "added",
      "severity": "critical"
    }
  ]
}
```

---

## 🧪 Tests

### Backend

```bash
cd backend
pytest

# Con coverage
pytest --cov=. --cov-report=html

# Tests específicos
pytest tests/test_version_manager.py
pytest tests/test_compliance_validator.py
```

### Frontend

```bash
cd frontend
npm run test

# Con UI
npm run test:ui

# Coverage
npm run test:coverage
```

### E2E

```bash
npm run test:e2e
```

---

## 🤝 Contribuir

1. **Fork** el repositorio
2. **Crea rama** (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** (`git commit -am 'feat: añadir nueva funcionalidad'`)
4. **Push** (`git push origin feature/nueva-funcionalidad`)
5. **Pull Request**

### Convención de Commits

```
feat(scope): mensaje
fix(scope): mensaje
docs(scope): mensaje
style(scope): mensaje
refactor(scope): mensaje
test(scope): mensaje
chore(scope): mensaje
```

---

## 🗺️ Roadmap

### v1.0.0 - Core Features ✅ (Actual)
- Sistema de fichas completo
- Versionado con snapshots
- Marco legal PT, IT, ES
- Import/Export
- Interface web profesional

### v1.1.0 - Extensiones (Q1 2026)
- [ ] Más países (Francia, Alemania, UK)
- [ ] API pública con rate limiting
- [ ] Webhooks para integraciones
- [ ] OAuth2

### v1.2.0 - Colaboración (Q2 2026)
- [ ] Multi-usuario con roles (Admin, Editor, Traductor, Revisor)
- [ ] Comentarios en fichas
- [ ] Workflow de aprobación
- [ ] Notificaciones real-time

### v1.3.0 - IA (Q3 2026)
- [ ] Traducción automática con GPT-4
- [ ] Sugerencias de compliance con IA
- [ ] OCR para imágenes
- [ ] Análisis de sentimiento en claims

### v2.0.0 - Cloud & Mobile (Q4 2026)
- [ ] Versión SaaS cloud
- [ ] App móvil (iOS + Android)
- [ ] Sincronización offline
- [ ] Backups automáticos en cloud

---

## 📄 Licencia

Proyecto bajo licencia **MIT**. Ver archivo [LICENSE](LICENSE) para detalles.

```
MIT License

Copyright (c) 2025 Party Brasil

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## 💬 Soporte

**Canales:**
- Issues GitHub: [github.com/partybrasil/Revisiones-Traducciones-Ultimate/issues](https://github.com/partybrasil/Revisiones-Traducciones-Ultimate/issues)
- Discusiones: [github.com/partybrasil/Revisiones-Traducciones-Ultimate/discussions](https://github.com/partybrasil/Revisiones-Traducciones-Ultimate/discussions)
- Email: support@revisiones-traducciones-ultimate.com

**FAQ:**
- ¿Funciona sin conexión? Sí, excepto web scraping
- ¿Agregar más idiomas? Edita `backend/translations/`
- ¿Agregar países al marco legal? Crea YAML en `backend/legal_framework/`
- ¿Datos encriptados? Sí, bcrypt para contraseñas, HTTPS en producción
- ¿Exportar catálogo completo? Sí, desde dashboard

---

## 🙏 Agradecimientos

- **FastAPI** - Framework backend
- **Vue.js** - Frontend reactivity
- **Tailwind CSS** - Design system
- **PostgreSQL** - Base de datos robusta
- Todos los contribuidores y usuarios

---

**Desarrollado con ❤️ por Party Brasil**

**Última actualización**: 16 de Diciembre, 2025
**Versión**: 1.0.0
