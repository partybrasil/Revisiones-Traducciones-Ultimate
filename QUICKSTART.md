# 🚀 Inicio Rápido - Revisiones-Traducciones-Ultimate

## Instalación Express

### 1. Clonar el Repositorio
```bash
git clone https://github.com/partybrasil/Revisiones-Traducciones-Ultimate.git
cd Revisiones-Traducciones-Ultimate
```

### 2. Configurar PostgreSQL

Asegúrate de tener PostgreSQL instalado y ejecutándose:

```bash
# Crear la base de datos
createdb revisiones_traducciones_db

# O usando psql
psql -U postgres
CREATE DATABASE revisiones_traducciones_db;
\q
```

### 3. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp backend/.env.example backend/.env

# Editar backend/.env con tus credenciales de PostgreSQL
# DATABASE_URL=postgresql://TU_USUARIO:TU_PASSWORD@localhost:5432/revisiones_traducciones_db
```

### 4. Instalar Dependencias

```bash
# Usar el launcher para instalar todo automáticamente
python launcher.py --install
```

### 5. Iniciar la Aplicación

```bash
# Iniciar el backend (modo por defecto)
python launcher.py
```

¡Eso es todo! El backend estará disponible en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Comandos del Launcher

```bash
# Iniciar backend con auto-reload (por defecto)
python launcher.py

# Iniciar backend sin auto-reload
python launcher.py --no-reload

# Iniciar backend en puerto personalizado
python launcher.py --port 8080

# Iniciar frontend (cuando esté disponible)
python launcher.py --frontend

# Instalar/actualizar dependencias
python launcher.py --install

# Ayuda
python launcher.py --help
```

## Próximos Pasos

1. Accede a http://localhost:8000/docs para ver la documentación interactiva de la API
2. Crea tu primera ficha de producto usando el endpoint POST /api/products
3. Consulta el README.md completo para información detallada sobre todas las funcionalidades

## Solución de Problemas

### Error: Base de datos no accesible

- Verifica que PostgreSQL está ejecutándose: `pg_isready`
- Verifica las credenciales en `backend/.env`
- Verifica que la base de datos existe: `psql -l`

### Error: Faltan dependencias

```bash
python launcher.py --install
```

### Error: Puerto en uso

```bash
# Usar un puerto diferente
python launcher.py --port 8080
```

## Desarrollo

Para contribuir al proyecto:

```bash
# Instalar dependencias de desarrollo
pip install -r backend/requirements.txt
pip install pytest pytest-cov black pylint

# Ejecutar tests
cd backend
pytest

# Formatear código
black .

# Linter
pylint *.py
```

---

**¿Necesitas ayuda?** Consulta el [README completo](README.md) o abre un [issue en GitHub](https://github.com/partybrasil/Revisiones-Traducciones-Ultimate/issues).
