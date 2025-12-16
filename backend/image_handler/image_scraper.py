"""
Image Scraper - Búsqueda y descarga de imágenes

Funcionalidades:
- search_images(): Buscar imágenes en la web (Bing API o scraping)
- download_image(): Descargar y validar imágenes
- validate_image(): Validar formato, tamaño y resolución
- resize_image(): Redimensionar imágenes manteniendo aspect ratio
"""

import os
import re
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from PIL import Image
from datetime import datetime
import hashlib


class ImageScraper:
    """
    Scraper de imágenes con búsqueda y descarga.
    
    Nota: Para producción, se recomienda usar Bing Image Search API.
    Esta implementación usa búsqueda básica sin API key.
    """
    
    def __init__(self, storage_dir: str = "backend/storage/images"):
        """
        Inicializar ImageScraper.
        
        Args:
            storage_dir: Directorio base para almacenar imágenes
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Headers para requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_images(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Buscar imágenes en la web.
        
        Args:
            query: Término de búsqueda
            max_results: Número máximo de resultados
        
        Returns:
            Lista de dicts con información de imágenes:
            [
                {
                    "url": "https://example.com/image.jpg",
                    "title": "Product Image",
                    "source": "example.com",
                    "resolution": (800, 600)  # Estimado
                },
                ...
            ]
        """
        # NOTA: Esta es una implementación simplificada
        # Para producción, usar Bing Image Search API:
        # https://www.microsoft.com/en-us/bing/apis/bing-image-search-api
        
        results = []
        
        try:
            # Simulación de resultados (en producción usar API real)
            # Aquí podrías implementar scraping de Google Images, Unsplash, etc.
            
            # Ejemplo con URLs de placeholder
            placeholder_urls = [
                f"https://via.placeholder.com/800x600.png?text={query.replace(' ', '+')}+{i}"
                for i in range(min(max_results, 5))
            ]
            
            for idx, url in enumerate(placeholder_urls):
                results.append({
                    "url": url,
                    "title": f"{query} - Image {idx + 1}",
                    "source": "placeholder.com",
                    "resolution": (800, 600),
                    "estimated_size_kb": 150
                })
        
        except Exception as e:
            print(f"Error searching images: {e}")
        
        return results
    
    def download_image(self, 
                      url: str, 
                      sku: str, 
                      image_type: str = "general",
                      timeout: int = 10) -> Optional[str]:
        """
        Descargar imagen desde URL con validaciones.
        
        Args:
            url: URL de la imagen
            sku: SKU del producto
            image_type: Tipo de imagen (frontal, trasera, lateral, general, etc.)
            timeout: Timeout en segundos
        
        Returns:
            Path local del archivo descargado, o None si falla
        """
        try:
            # Descargar imagen
            response = requests.get(url, headers=self.headers, timeout=timeout, stream=True)
            response.raise_for_status()
            
            # Validar content-type
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"Invalid content-type: {content_type}")
                return None
            
            # Validar tamaño (< 10MB)
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > 10 * 1024 * 1024:
                print(f"Image too large: {content_length} bytes")
                return None
            
            # Crear directorio para SKU
            sku_dir = self.storage_dir / sku / image_type
            sku_dir.mkdir(parents=True, exist_ok=True)
            
            # Generar filename único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            
            # Detectar extensión
            ext = self._detect_image_extension(url, content_type)
            filename = f"image_{timestamp}_{url_hash}{ext}"
            filepath = sku_dir / filename
            
            # Guardar archivo
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Validar imagen
            if not self.validate_image(str(filepath)):
                os.remove(filepath)
                return None
            
            # Redimensionar si es muy grande
            self.resize_image(str(filepath), max_width=3000)
            
            return str(filepath)
        
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")
            return None
    
    def _detect_image_extension(self, url: str, content_type: str) -> str:
        """Detectar extensión de imagen desde URL o content-type."""
        # Intentar desde URL
        match = re.search(r'\.(jpg|jpeg|png|gif|webp|bmp)(\?.*)?$', url, re.IGNORECASE)
        if match:
            return f".{match.group(1).lower()}"
        
        # Intentar desde content-type
        type_map = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/bmp': '.bmp'
        }
        
        return type_map.get(content_type, '.jpg')
    
    def validate_image(self, file_path: str) -> bool:
        """
        Validar imagen: formato, tamaño, resolución.
        
        Args:
            file_path: Path del archivo
        
        Returns:
            True si la imagen es válida, False otherwise
        """
        try:
            # Validar que el archivo existe
            if not os.path.exists(file_path):
                return False
            
            # Validar tamaño < 10MB
            file_size = os.path.getsize(file_path)
            if file_size > 10 * 1024 * 1024:
                print(f"Image too large: {file_size} bytes")
                return False
            
            # Validar formato con PIL
            with Image.open(file_path) as img:
                # Validar formato soportado
                if img.format not in ['JPEG', 'PNG', 'GIF', 'WEBP', 'BMP']:
                    print(f"Unsupported format: {img.format}")
                    return False
                
                # Validar resolución mínima (> 100x100px)
                width, height = img.size
                if width < 100 or height < 100:
                    print(f"Resolution too small: {width}x{height}")
                    return False
                
                # Validar que no está corrupta
                img.verify()
            
            return True
        
        except Exception as e:
            print(f"Error validating image {file_path}: {e}")
            return False
    
    def resize_image(self, 
                    file_path: str, 
                    max_width: int = 3000, 
                    max_height: int = 3000,
                    quality: int = 85):
        """
        Redimensionar imagen manteniendo aspect ratio.
        
        Args:
            file_path: Path del archivo
            max_width: Ancho máximo en pixels
            max_height: Alto máximo en pixels
            quality: Calidad JPEG (0-100)
        """
        try:
            with Image.open(file_path) as img:
                # Obtener dimensiones actuales
                width, height = img.size
                
                # Calcular si necesita redimensionar
                if width <= max_width and height <= max_height:
                    return  # No necesita redimensionar
                
                # Calcular nuevo tamaño manteniendo aspect ratio
                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                
                # Redimensionar
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Guardar según formato
                if img.format == 'JPEG' or file_path.lower().endswith('.jpg'):
                    img_resized.save(file_path, 'JPEG', quality=quality, optimize=True)
                elif img.format == 'PNG':
                    img_resized.save(file_path, 'PNG', optimize=True)
                else:
                    img_resized.save(file_path, img.format)
        
        except Exception as e:
            print(f"Error resizing image {file_path}: {e}")
    
    def get_image_info(self, file_path: str) -> Dict:
        """
        Obtener información de una imagen.
        
        Args:
            file_path: Path del archivo
        
        Returns:
            Dict con información de la imagen
        """
        try:
            with Image.open(file_path) as img:
                return {
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size,
                    "width": img.size[0],
                    "height": img.size[1],
                    "file_size_bytes": os.path.getsize(file_path),
                    "file_size_kb": os.path.getsize(file_path) / 1024,
                    "file_path": file_path
                }
        
        except Exception as e:
            print(f"Error getting image info: {e}")
            return {}
