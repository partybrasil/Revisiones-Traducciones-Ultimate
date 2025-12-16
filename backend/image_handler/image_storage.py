"""
Image Storage - Gestión de almacenamiento de imágenes

Funcionalidades:
- save_uploaded_file(): Guardar archivo subido por usuario
- get_image_path(): Obtener ruta de imagen
- delete_image(): Eliminar imagen
- list_images(): Listar imágenes de un producto
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from PIL import Image
import hashlib


class ImageStorage:
    """
    Gestor de almacenamiento de imágenes de productos.
    
    Estructura de directorios:
    backend/storage/images/
        ├── {sku}/
        │   ├── frontal/
        │   │   └── image_{timestamp}.jpg
        │   ├── trasera/
        │   │   └── image_{timestamp}.jpg
        │   ├── lateral/
        │   │   └── image_{timestamp}.jpg
        │   └── general/
        │       └── image_{timestamp}.jpg
    """
    
    # Tipos de imagen válidos
    VALID_IMAGE_TYPES = ['frontal', 'trasera', 'lateral', 'superior', 'inferior', 'general', 'detail', 'lifestyle']
    
    # Extensiones permitidas
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    def __init__(self, storage_dir: str = "backend/storage/images"):
        """
        Inicializar ImageStorage.
        
        Args:
            storage_dir: Directorio base para almacenar imágenes
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save_uploaded_file(self, 
                          file_bytes: bytes,
                          filename: str,
                          sku: str, 
                          image_type: str = "general") -> Optional[str]:
        """
        Guardar archivo subido por usuario.
        
        Args:
            file_bytes: Bytes del archivo
            filename: Nombre original del archivo
            sku: SKU del producto
            image_type: Tipo de imagen
        
        Returns:
            Path relativo del archivo guardado, o None si falla
        """
        try:
            # Validar image_type
            if image_type not in self.VALID_IMAGE_TYPES:
                raise ValueError(f"Invalid image_type: {image_type}. Must be one of {self.VALID_IMAGE_TYPES}")
            
            # Validar extensión
            ext = Path(filename).suffix.lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                raise ValueError(f"Invalid file extension: {ext}. Allowed: {self.ALLOWED_EXTENSIONS}")
            
            # Crear directorio para SKU e image_type
            sku_dir = self.storage_dir / sku / image_type
            sku_dir.mkdir(parents=True, exist_ok=True)
            
            # Generar filename único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_hash = hashlib.md5(file_bytes).hexdigest()[:8]
            new_filename = f"image_{timestamp}_{file_hash}{ext}"
            filepath = sku_dir / new_filename
            
            # Guardar archivo
            with open(filepath, 'wb') as f:
                f.write(file_bytes)
            
            # Validar que es una imagen válida
            if not self._validate_image_file(filepath):
                os.remove(filepath)
                raise ValueError("Invalid image file")
            
            # Redimensionar si es muy grande
            self._resize_if_needed(filepath)
            
            # Retornar path relativo
            return str(filepath.relative_to(self.storage_dir.parent))
        
        except Exception as e:
            print(f"Error saving uploaded file: {e}")
            return None
    
    def get_image_path(self, sku: str, image_type: str, filename: Optional[str] = None) -> Optional[str]:
        """
        Obtener path de imagen.
        
        Args:
            sku: SKU del producto
            image_type: Tipo de imagen
            filename: Nombre específico del archivo (opcional). Si no se provee, retorna el primero encontrado.
        
        Returns:
            Path absoluto del archivo, o None si no existe
        """
        sku_dir = self.storage_dir / sku / image_type
        
        if not sku_dir.exists():
            return None
        
        if filename:
            # Buscar archivo específico
            filepath = sku_dir / filename
            return str(filepath) if filepath.exists() else None
        else:
            # Retornar el primero encontrado
            images = list(sku_dir.glob("*"))
            if images:
                return str(images[0])
            return None
    
    def list_images(self, sku: str, image_type: Optional[str] = None) -> List[Dict]:
        """
        Listar imágenes de un producto.
        
        Args:
            sku: SKU del producto
            image_type: Tipo de imagen (opcional). Si no se provee, lista todas.
        
        Returns:
            Lista de dicts con información de imágenes:
            [
                {
                    "filename": "image_20251216_120000.jpg",
                    "path": "backend/storage/images/CF-HYD-001/frontal/image_20251216_120000.jpg",
                    "type": "frontal",
                    "size_kb": 250.5,
                    "created_at": "2025-12-16T12:00:00"
                },
                ...
            ]
        """
        images = []
        
        sku_dir = self.storage_dir / sku
        if not sku_dir.exists():
            return images
        
        # Determinar tipos a buscar
        types_to_search = [image_type] if image_type else self.VALID_IMAGE_TYPES
        
        for img_type in types_to_search:
            type_dir = sku_dir / img_type
            if not type_dir.exists():
                continue
            
            for filepath in type_dir.glob("*"):
                if filepath.is_file() and filepath.suffix.lower() in self.ALLOWED_EXTENSIONS:
                    images.append({
                        "filename": filepath.name,
                        "path": str(filepath),
                        "relative_path": str(filepath.relative_to(self.storage_dir.parent)),
                        "type": img_type,
                        "size_kb": filepath.stat().st_size / 1024,
                        "created_at": datetime.fromtimestamp(filepath.stat().st_ctime).isoformat()
                    })
        
        # Ordenar por fecha de creación DESC
        images.sort(key=lambda x: x['created_at'], reverse=True)
        
        return images
    
    def delete_image(self, sku: str, image_type: str, filename: Optional[str] = None) -> bool:
        """
        Eliminar imagen(es).
        
        Args:
            sku: SKU del producto
            image_type: Tipo de imagen
            filename: Nombre específico del archivo (opcional). Si no se provee, elimina todas del tipo.
        
        Returns:
            True si se eliminó exitosamente, False otherwise
        """
        try:
            sku_dir = self.storage_dir / sku / image_type
            
            if not sku_dir.exists():
                return False
            
            if filename:
                # Eliminar archivo específico
                filepath = sku_dir / filename
                if filepath.exists():
                    os.remove(filepath)
                    return True
                return False
            else:
                # Eliminar todo el directorio del tipo
                shutil.rmtree(sku_dir)
                return True
        
        except Exception as e:
            print(f"Error deleting image: {e}")
            return False
    
    def delete_all_images(self, sku: str) -> bool:
        """
        Eliminar todas las imágenes de un producto.
        
        Args:
            sku: SKU del producto
        
        Returns:
            True si se eliminó exitosamente, False otherwise
        """
        try:
            sku_dir = self.storage_dir / sku
            
            if sku_dir.exists():
                shutil.rmtree(sku_dir)
                return True
            
            return False
        
        except Exception as e:
            print(f"Error deleting all images for {sku}: {e}")
            return False
    
    def move_image(self, 
                   sku: str, 
                   from_type: str, 
                   to_type: str, 
                   filename: str) -> bool:
        """
        Mover imagen de un tipo a otro.
        
        Args:
            sku: SKU del producto
            from_type: Tipo origen
            to_type: Tipo destino
            filename: Nombre del archivo
        
        Returns:
            True si se movió exitosamente, False otherwise
        """
        try:
            from_path = self.storage_dir / sku / from_type / filename
            to_dir = self.storage_dir / sku / to_type
            to_dir.mkdir(parents=True, exist_ok=True)
            to_path = to_dir / filename
            
            if from_path.exists():
                shutil.move(str(from_path), str(to_path))
                return True
            
            return False
        
        except Exception as e:
            print(f"Error moving image: {e}")
            return False
    
    def _validate_image_file(self, filepath: Path) -> bool:
        """Validar que el archivo es una imagen válida."""
        try:
            with Image.open(filepath) as img:
                img.verify()
            return True
        except Exception:
            return False
    
    def _resize_if_needed(self, filepath: Path, max_width: int = 3000, max_height: int = 3000):
        """Redimensionar imagen si excede dimensiones máximas."""
        try:
            with Image.open(filepath) as img:
                width, height = img.size
                
                if width <= max_width and height <= max_height:
                    return
                
                # Calcular nuevo tamaño
                ratio = min(max_width / width, max_height / height)
                new_size = (int(width * ratio), int(height * ratio))
                
                # Redimensionar
                img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Guardar
                if img.format == 'JPEG':
                    img_resized.save(filepath, 'JPEG', quality=85, optimize=True)
                else:
                    img_resized.save(filepath, img.format, optimize=True)
        
        except Exception as e:
            print(f"Error resizing image: {e}")
    
    def get_storage_stats(self, sku: Optional[str] = None) -> Dict:
        """
        Obtener estadísticas de almacenamiento.
        
        Args:
            sku: SKU específico (opcional). Si no se provee, stats globales.
        
        Returns:
            Dict con estadísticas
        """
        stats = {
            "total_images": 0,
            "total_size_mb": 0,
            "images_by_type": {},
            "skus_count": 0
        }
        
        search_dir = self.storage_dir / sku if sku else self.storage_dir
        
        if not search_dir.exists():
            return stats
        
        if sku:
            # Stats para un SKU específico
            for img_type in self.VALID_IMAGE_TYPES:
                type_dir = search_dir / img_type
                if type_dir.exists():
                    images = list(type_dir.glob("*"))
                    count = len(images)
                    size_mb = sum(img.stat().st_size for img in images) / (1024 * 1024)
                    
                    stats["total_images"] += count
                    stats["total_size_mb"] += size_mb
                    stats["images_by_type"][img_type] = {
                        "count": count,
                        "size_mb": round(size_mb, 2)
                    }
        else:
            # Stats globales
            for sku_dir in search_dir.iterdir():
                if sku_dir.is_dir():
                    stats["skus_count"] += 1
                    
                    for img_type_dir in sku_dir.iterdir():
                        if img_type_dir.is_dir():
                            img_type = img_type_dir.name
                            images = list(img_type_dir.glob("*"))
                            count = len(images)
                            size_mb = sum(img.stat().st_size for img in images) / (1024 * 1024)
                            
                            stats["total_images"] += count
                            stats["total_size_mb"] += size_mb
                            
                            if img_type not in stats["images_by_type"]:
                                stats["images_by_type"][img_type] = {"count": 0, "size_mb": 0}
                            
                            stats["images_by_type"][img_type]["count"] += count
                            stats["images_by_type"][img_type]["size_mb"] += size_mb
        
        # Redondear total_size_mb
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)
        
        # Redondear sizes en images_by_type
        for img_type in stats["images_by_type"]:
            stats["images_by_type"][img_type]["size_mb"] = round(stats["images_by_type"][img_type]["size_mb"], 2)
        
        return stats
