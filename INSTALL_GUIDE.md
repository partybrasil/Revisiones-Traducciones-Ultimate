# 📦 Guía de Instalación Rápida

## Instalación de Dependencias

### Opción 1: Desde la raíz del proyecto (Recomendado)

```bash
# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar todas las dependencias desde la raíz
pip install -r requirements.txt
```

### Opción 2: Desde el directorio backend

```bash
# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias del backend
cd backend
pip install -r requirements.txt
```

## Inicialización de la Base de Datos

Una vez instaladas las dependencias y configurada PostgreSQL:

```bash
# Asegúrate de estar en el directorio backend
cd backend

# Ejecutar el script de inicialización
python init_db.py
```

Este script creará:
- ✅ Todas las tablas necesarias en la base de datos
- ✅ Presets automáticos para diferentes familias de productos
- ✅ **5 productos de ejemplo** con datos variados:
  - `CF-HYD-001` - Crema Hidratante Facial (Cosmética Facial)
  - `CS-AGE-002` - Sérum Anti-Edad Intensivo (Cosmética Facial)
  - `FP-ORG-003` - Pasta Orgánica de Trigo Integral (Alimento Envasado)
  - `FS-VIT-004` - Vitamina C 1000mg (Suplemento Alimenticio)
  - `CB-LOT-005` - Loción Corporal Aloe Vera (Cosmética Corporal)

## Características de los Productos de Ejemplo

Los productos de ejemplo incluyen:
- Traducciones completas en múltiples idiomas (ES, PT, IT, EN, FR)
- Diferentes estados: `approved`, `in_review`, `draft`
- Diferentes familias de productos
- Diferentes formatos: botellas, frascos, paquetes
- Información completa de distribuidores y fabricación
- Ingredientes, alérgenos y advertencias
- Instrucciones de uso y almacenamiento

## Próximos Pasos

Después de la inicialización:

1. **Iniciar el servidor backend:**
   ```bash
   python launcher.py
   ```

2. **Acceder a la documentación de la API:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Probar los productos de ejemplo:**
   ```bash
   # Listar todos los productos
   curl http://localhost:8000/api/products
   
   # Obtener un producto específico
   curl http://localhost:8000/api/products/CF-HYD-001
   ```

## Eliminar Productos de Ejemplo

Los productos de ejemplo pueden ser eliminados más adelante usando:

```bash
# Usando la API
curl -X DELETE http://localhost:8000/api/products/CF-HYD-001
curl -X DELETE http://localhost:8000/api/products/CS-AGE-002
curl -X DELETE http://localhost:8000/api/products/FP-ORG-003
curl -X DELETE http://localhost:8000/api/products/FS-VIT-004
curl -X DELETE http://localhost:8000/api/products/CB-LOT-005
```

O directamente desde la base de datos:

```sql
DELETE FROM products WHERE sku IN (
  'CF-HYD-001', 'CS-AGE-002', 'FP-ORG-003', 'FS-VIT-004', 'CB-LOT-005'
);
```

## Solución de Problemas

### Error: ModuleNotFoundError

Asegúrate de haber instalado las dependencias:
```bash
pip install -r requirements.txt
```

### Error: Base de datos no existe

Crea la base de datos primero:
```bash
createdb revisiones_traducciones_db
```

### Error: Productos ya existen

El script detecta automáticamente si los productos ya existen y los omite. Si deseas recrearlos, elimínalos primero de la base de datos.

---

**Última actualización:** 16 de Diciembre, 2025
