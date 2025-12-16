# 🚀 Inicio Rápido - Revisiones-Traducciones-Ultimate

## Instalación Express (2 Pasos)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/partybrasil/Revisiones-Traducciones-Ultimate.git
cd Revisiones-Traducciones-Ultimate
```

### 2. Instalar Dependencias y Arrancar

```bash
# Instalar dependencias del backend
python launcher.py --install

# Iniciar la aplicación (backend + frontend)
python launcher.py
```

¡Eso es todo! La aplicación estará disponible en:
- **Frontend**: http://localhost:5173 (si está configurado)
- **Backend API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### ✨ Características Automáticas

El launcher **automáticamente**:
- ✅ Verifica e instala dependencias faltantes
- ✅ Crea la base de datos SQLite si no existe
- ✅ Inicializa todas las tablas necesarias
- ✅ Ofrece cargar datos de ejemplo
- ✅ Inicia backend y frontend juntos
- ✅ No requiere PostgreSQL ni Docker

## Comandos del Launcher

```bash
# Iniciar backend + frontend juntos (modo por defecto)
python launcher.py
python launcher.py --both

# Iniciar solo el backend
python launcher.py --backend

# Iniciar solo el frontend
python launcher.py --frontend

# Iniciar sin auto-reload (producción)
python launcher.py --no-reload

# Usar puerto personalizado para el backend
python launcher.py --port 8080

# Instalar/actualizar dependencias
python launcher.py --install

# Saltar verificaciones (arranque rápido)
python launcher.py --skip-checks

# Ayuda completa
python launcher.py --help
```

## Base de Datos

Por defecto, la aplicación usa **SQLite** (sin configuración necesaria):
- Archivo: `./revisiones_traducciones.db`
- Se crea automáticamente en el primer arranque
- Ideal para desarrollo y máquinas con recursos limitados

### Usar PostgreSQL (Opcional)

Si prefieres PostgreSQL para producción:

1. Crear base de datos:
```bash
createdb revisiones_traducciones_db
```

2. Configurar variables de entorno:
```bash
cp backend/.env.example backend/.env
# Editar backend/.env
# DATABASE_URL=postgresql://usuario:password@localhost:5432/revisiones_traducciones_db
```

3. Iniciar normalmente:
```bash
python launcher.py
```

## Próximos Pasos

1. **Accede a la documentación interactiva**: http://localhost:8000/docs
2. **Crea tu primera ficha**: POST /api/products
3. **Explora los endpoints** de versiones, compliance y traducciones
4. **Consulta el README completo** para funcionalidades avanzadas

## Solución de Problemas

### La base de datos no se inicializa

```bash
# Eliminar base de datos y reiniciar
rm -f revisiones_traducciones.db
python launcher.py
```

### Error: Faltan dependencias

```bash
python launcher.py --install
```

### Puerto en uso

```bash
# Backend en puerto diferente
python launcher.py --port 8080
```

### Frontend no arranca

El frontend puede no estar configurado aún. El launcher automáticamente:
- Detecta si el frontend existe
- Instala dependencias de Node.js si faltan
- Si no existe frontend, solo arranca el backend

## Desarrollo

Para contribuir al proyecto:

```bash
# Instalar dependencias de desarrollo
pip install -r backend/requirements.txt
pip install pytest pytest-cov black ruff

# Ejecutar tests (cuando estén disponibles)
cd backend
pytest

# Formatear código
black .

# Linter
ruff check .
```

## Diferencias con Docker

Esta configuración **NO** requiere Docker:
- ✅ Más simple para desarrollo local
- ✅ Menor consumo de recursos
- ✅ Arranque instantáneo
- ✅ Fácil debugging

Si necesitas Docker para producción, consulta la documentación de deployment.

---

**¿Necesitas ayuda?** Consulta el [README completo](README.md) o abre un [issue en GitHub](https://github.com/partybrasil/Revisiones-Traducciones-Ultimate/issues).
