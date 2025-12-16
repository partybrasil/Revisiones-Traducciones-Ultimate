---
name: Revisiones_Traducciones_Ultimate_Agent
description: |
    Agente especializado en desarrollo de sistema web profesional para gestión de fichas de producto multiidioma con versionado, compliance regulatorio y traducción asistida
version: 1.0.0
enabled: true
---

# Revisiones-Traducciones-Ultimate Development Agent

## 🎯 Propósito del Agente

Este agente especializado desarrolla **Revisiones-Traducciones-Ultimate**, una aplicación web SaaS-grade para gestión integral de fichas de producto multiidioma (ES, PT, IT, EN, FR, BR) con compliance regulatorio (Portugal, Italia, España), versionado completo con snapshots, y exportación masiva.

## 📚 Recursos Principales

**Consulta siempre:**
- `README.md` - Documentación completa, instalación, uso
- `.github/extended_memory.md` - Especificación técnica extendida, arquitectura detallada, modelos de datos completos

## 🏗️ Stack Tecnológico

**Backend:** FastAPI (Python 3.11+), SQLAlchemy 2.0+ ORM, PostgreSQL 14+, Pydantic validación

**Frontend:** Vue.js 3.4+ (Composition API), Vite 5.0+, Tailwind CSS 3.4+, Pinia state management

**Integraciones:** openpyxl (Excel), ReportLab (PDF), BeautifulSoup+Selenium (scraping), aiofiles (async I/O)

## 🛠️ Comandos Principales

**Scaffolding:** `@agent scaffold backend` | `@agent scaffold frontend` | `@agent create model ProductSheet` | `@agent create component ProductSheetEditor` | `@agent create api route products`

**Code Quality:** `@agent review` (revisar código) | `@agent lint` (pylint/ESLint) | `@agent format` (Black/Prettier) | `@agent test` (ejecutar tests)

**Legal Framework:** `@agent validate legal PT` | `@agent generate compliance report` | `@agent check translations`

**Versionado:** `@agent create snapshot` | `@agent compare versions 2.0 2.1` | `@agent restore version 2.0`

**Documentación:** `@agent docs api` | `@agent docs models` | `@agent update readme`

## ✅ Fases de Desarrollo

1. **Setup & CRUD** (Semanas 1-2): FastAPI setup, modelos SQLAlchemy, endpoints REST básicos, Dashboard Vue.js
2. **Legal Framework** (Semanas 3-4): Reglas PT/IT/ES YAML, ComplianceValidator, alertas UI
3. **Versionado** (Semanas 5-6): Snapshots JSONB, changelog, timeline visual, diff viewer
4. **Import/Export** (Semanas 7-8): Template Excel generator, bulk importer, PDF/Markdown exporters
5. **Advanced** (Semanas 9-10): Web scraping imágenes, translation memory, presets 150+, 3D box
6. **Testing & Deploy** (Semanas 11-12): 80%+ test coverage, optimización performance, documentación completa

## 📋 Estándares de Código

**Python:** PEP 8, type hints obligatorios, docstrings Google style, líneas ≤100 chars, async/await para I/O

**Vue.js:** Composition API con `<script setup lang="ts">`, props validation, TypeScript strict, Tailwind scoped styles

## 📞 Contacto

Para dudas técnicas: revisa README.md (setup, uso, API) y extended_memory.md (especificación completa, modelos, flujos)

**Última actualización:** 16 de Diciembre, 2025 | **Versión:** 1.0.0
