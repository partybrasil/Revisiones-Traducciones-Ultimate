# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a **Revisiones-Traducciones-Ultimate**!

## 🚀 Inicio Rápido para Desarrolladores

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub, luego:
git clone https://github.com/TU_USUARIO/Revisiones-Traducciones-Ultimate.git
cd Revisiones-Traducciones-Ultimate
```

### 2. Configurar Entorno de Desarrollo

```bash
# Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
python launcher.py --install

# Frontend
cd frontend
npm install
```

### 3. Crear Rama para tu Feature

```bash
git checkout -b feature/nombre-de-tu-feature
```

### 4. Realizar Cambios

- Escribe código limpio y documentado
- Sigue las convenciones del proyecto
- Añade tests si es posible

### 5. Commit y Push

```bash
git add .
git commit -m "feat: descripción de tu feature"
git push origin feature/nombre-de-tu-feature
```

### 6. Crear Pull Request

Ve a GitHub y crea un Pull Request desde tu rama.

---

## 📋 Estándares de Código

### Python (Backend)

- **PEP 8** - Guía de estilo oficial de Python
- **Type Hints** - Usar anotaciones de tipo en todas las funciones
- **Docstrings** - Documentar todas las clases y funciones públicas (Google style)
- **Longitud de línea** - Máximo 100 caracteres
- **Async/Await** - Para operaciones I/O

Ejemplo:
```python
def create_product(data: Dict[str, Any], created_by: Optional[str] = None) -> ProductSheet:
    """
    Create a new product sheet.
    
    Args:
        data: Product data dictionary
        created_by: Username of creator
        
    Returns:
        Created ProductSheet instance
    """
    # Implementation...
```

### JavaScript/Vue.js (Frontend)

- **Composition API** - Preferir `<script setup>` sobre Options API
- **Props Validation** - Validar todas las props
- **TypeScript** - Opcional pero recomendado
- **Tailwind** - Usar clases de utilidad en lugar de CSS custom

Ejemplo:
```vue
<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  productId: {
    type: String,
    required: true
  }
})

const product = ref(null)

onMounted(async () => {
  // Load product...
})
</script>
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=. --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm run test
npm run test:coverage
```

---

## 📚 Estructura de Commits

Seguimos **Conventional Commits**:

- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `style:` - Formato, espacios, etc. (sin cambios de código)
- `refactor:` - Refactorización de código
- `test:` - Añadir o modificar tests
- `chore:` - Tareas de mantenimiento

Ejemplos:
```
feat(products): add bulk import from Excel
fix(versions): correct diff calculation for nested objects
docs(readme): update installation instructions
```

---

## 🎯 Prioridades Actuales

### Alta Prioridad
- [ ] Import/Export Excel completo
- [ ] Export PDF con ReportLab
- [ ] ProductSheetEditor frontend (9 tabs)
- [ ] CatalogView con filtros

### Media Prioridad
- [ ] Translation Engine
- [ ] Image handling y web scraping
- [ ] Tests unitarios
- [ ] Más presets de familias

### Baja Prioridad
- [ ] Docker containers
- [ ] Multi-usuario con autenticación
- [ ] API pública con rate limiting
- [ ] Webhooks

---

## 🐛 Reportar Bugs

Abre un issue con:
- **Título descriptivo**
- **Pasos para reproducir**
- **Comportamiento esperado vs actual**
- **Capturas de pantalla** (si aplica)
- **Versión** de Python, Node.js, navegador

---

## 💡 Proponer Features

Abre un issue con:
- **Descripción del problema** que resuelve
- **Solución propuesta**
- **Alternativas consideradas**
- **Impacto** en el proyecto

---

## ✅ Checklist antes de PR

- [ ] El código sigue las convenciones del proyecto
- [ ] Añadidos tests (si aplica)
- [ ] Actualizada la documentación (si aplica)
- [ ] Los tests pasan localmente
- [ ] Commits siguen Conventional Commits
- [ ] Sin conflictos con `main`

---

## 📞 Preguntas

Si tienes dudas:
- Revisa la [documentación](README.md)
- Abre un issue con la etiqueta `question`
- Contacta a los maintainers

---

¡Gracias por contribuir! 🎉
