#!/usr/bin/env python3
"""
Launcher for Revisiones-Traducciones-Ultimate
Simple script to start the application without manual uvicorn commands.
"""
import os
import sys
import subprocess
import argparse
import signal
import multiprocessing
from pathlib import Path


class Color:
    """ANSI color codes for terminal output."""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header():
    """Print application header."""
    print(f"""
{Color.BLUE}{Color.BOLD}╔═══════════════════════════════════════════════════════════════╗
║   Revisiones-Traducciones-Ultimate v1.0.0                    ║
║   Sistema de Gestión de Fichas de Producto Multiidioma       ║
╚═══════════════════════════════════════════════════════════════╝{Color.END}
""")


def check_python_version():
    """Check if Python version is 3.11 or higher."""
    if sys.version_info < (3, 11):
        print(f"{Color.RED}❌ Error: Python 3.11+ es requerido. Versión actual: {sys.version}{Color.END}")
        sys.exit(1)
    print(f"{Color.GREEN}✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}{Color.END}")


def check_requirements():
    """Check if required packages are installed."""
    print(f"\n{Color.BOLD}Verificando dependencias...{Color.END}")
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print(f"{Color.GREEN}✓ Dependencias instaladas{Color.END}")
        return True
    except ImportError as e:
        print(f"{Color.YELLOW}⚠ Faltan dependencias: {e}{Color.END}")
        print(f"{Color.YELLOW}Ejecuta: pip install -r backend/requirements.txt{Color.END}")
        return False


def check_frontend_setup():
    """Check if frontend is set up and install dependencies if needed."""
    print(f"\n{Color.BOLD}Verificando frontend...{Color.END}")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not (frontend_dir / "package.json").exists():
        print(f"{Color.YELLOW}⚠ Frontend no está configurado aún{Color.END}")
        return False
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print(f"{Color.YELLOW}⚠ Dependencias del frontend no instaladas{Color.END}")
        print(f"{Color.BLUE}📦 Instalando dependencias del frontend...{Color.END}")
        
        try:
            result = subprocess.run(
                ["npm", "install"],
                cwd=frontend_dir,
                capture_output=True,
                text=True
            )
        except FileNotFoundError:
            print(f"{Color.RED}❌ No se encontró 'npm'. Por favor instala Node.js y npm y asegúrate de que estén en tu PATH.{Color.END}")
            return False
        
        if result.returncode != 0:
            print(f"{Color.RED}❌ Error instalando dependencias del frontend{Color.END}")
            print(f"{Color.YELLOW}Salida: {result.stderr}{Color.END}")
            return False
        
        print(f"{Color.GREEN}✓ Dependencias del frontend instaladas{Color.END}")
    else:
        print(f"{Color.GREEN}✓ Frontend configurado correctamente{Color.END}")
    
    return True


def check_and_init_database():
    """Check if database exists and initialize it if needed."""
    print(f"\n{Color.BOLD}Verificando base de datos...{Color.END}")
    
    try:
        from backend.config import settings
        from backend.database import engine, Base
        from sqlalchemy import text, inspect
        from sqlalchemy.engine import make_url
        import os
        
        # Check if it's SQLite and if the file exists
        db_url = settings.database_url
        is_sqlite = db_url.startswith("sqlite")
        
        if is_sqlite:
            # Extract database file path from URL using SQLAlchemy's URL parser
            parsed_url = make_url(db_url)
            db_file = parsed_url.database
            
            # Handle special cases
            if db_file == ":memory:":
                print(f"{Color.GREEN}✓ Usando base de datos SQLite en memoria{Color.END}")
                db_exists = True
            elif not db_file:
                print(f"{Color.RED}❌ URL de base de datos SQLite inválida: {db_url}{Color.END}")
                return False
            else:
                # Make path absolute if relative
                if not os.path.isabs(db_file):
                    db_file = os.path.join(os.getcwd(), db_file)
                
                db_exists = os.path.exists(db_file)
                
                if not db_exists:
                    print(f"{Color.YELLOW}⚠ Base de datos no existe: {db_file}{Color.END}")
                    print(f"{Color.BLUE}📦 Creando nueva base de datos...{Color.END}")
        
        # Try to connect and check if tables exist
        try:
            with engine.connect() as conn:
                # Test connection
                conn.execute(text("SELECT 1"))
                
                # Check if tables exist
                inspector = inspect(engine)
                tables = inspector.get_table_names()
                
                if not tables:
                    print(f"{Color.YELLOW}⚠ Base de datos vacía. Inicializando tablas...{Color.END}")
                    # Import models to register them with Base
                    from backend.models.product_sheet import ProductSheet, Preset
                    # Create all tables
                    Base.metadata.create_all(bind=engine)
                    print(f"{Color.GREEN}✓ Tablas de base de datos creadas{Color.END}")
                    
                    # Check if running in interactive environment
                    import sys
                    if sys.stdin.isatty():
                        # Ask if user wants to load sample data
                        print(f"\n{Color.YELLOW}¿Deseas cargar datos de ejemplo? (s/n): {Color.END}", end="")
                        try:
                            response = input().strip().lower()
                            if response in ['s', 'si', 'sí', 'y', 'yes']:
                                print(f"{Color.BLUE}📦 Cargando datos de ejemplo...{Color.END}")
                                load_sample_data()
                        except (EOFError, KeyboardInterrupt):
                            print(f"\n{Color.YELLOW}Saltando carga de datos de ejemplo{Color.END}")
                    else:
                        print(f"{Color.YELLOW}⚠ Entorno no interactivo detectado. Usa --load-sample-data para cargar datos de ejemplo.{Color.END}")
                else:
                    print(f"{Color.GREEN}✓ Base de datos encontrada con {len(tables)} tablas{Color.END}")
                
                return True
                
        except Exception as e:
            print(f"{Color.RED}❌ Error conectando a base de datos: {e}{Color.END}")
            print(f"{Color.YELLOW}Intentando inicializar base de datos...{Color.END}")
            
            # Import models and create tables
            from backend.models.product_sheet import ProductSheet, Preset
            Base.metadata.create_all(bind=engine)
            print(f"{Color.GREEN}✓ Base de datos inicializada correctamente{Color.END}")
            return True
            
    except Exception as e:
        print(f"{Color.RED}❌ Error al verificar/crear base de datos: {e}{Color.END}")
        import traceback
        traceback.print_exc()
        return False


def load_sample_data():
    """Load sample presets and products into the database."""
    try:
        from backend.database import SessionLocal
        from backend.models.product_sheet import ProductSheet
        
        db = SessionLocal()
        
        try:
            # Create a few sample products
            sample_products = [
                ProductSheet(
                    sku="DEMO-001",
                    ean_list=["1234567890123"],
                    brand="Demo Brand",
                    family="COSMETICS_FACIAL",
                    title_short={
                        "es": "Crema Hidratante Demo",
                        "pt": "Creme Hidratante Demo",
                        "it": "Crema Idratante Demo",
                    },
                    description_detailed={
                        "es": "Producto de demostración para probar el sistema",
                        "pt": "Produto de demonstração para testar o sistema",
                        "it": "Prodotto dimostrativo per testare il sistema",
                    },
                    net_weight_value=50,
                    net_weight_unit="ml",
                    current_version="1.0",
                    status="draft",
                    created_by="system",
                    updated_by="system"
                )
            ]
            
            created_skus = []
            for product in sample_products:
                existing = db.query(ProductSheet).filter(ProductSheet.sku == product.sku).first()
                if not existing:
                    db.add(product)
                    created_skus.append(product.sku)
            
            db.commit()
            
            # Print success messages only after successful commit
            for sku in created_skus:
                print(f"  ✓ Producto demo creado: {sku}")
            
            print(f"{Color.GREEN}✓ Datos de ejemplo cargados{Color.END}")
        
        finally:
            # Always close the database session
            db.close()
        
    except Exception as e:
        print(f"{Color.YELLOW}⚠ No se pudieron cargar datos de ejemplo: {e}{Color.END}")


def check_database():
    """Check if database is accessible (deprecated - use check_and_init_database)."""
    return check_and_init_database()


def start_backend(reload=True, host="0.0.0.0", port=8000):
    """Start the backend server."""
    print(f"\n{Color.BOLD}🚀 Iniciando Backend Server...{Color.END}")
    print(f"{Color.BLUE}Host: {host}:{port}{Color.END}")
    print(f"{Color.BLUE}Reload: {'Activado' if reload else 'Desactivado'}{Color.END}")
    print(f"{Color.BLUE}Docs: http://localhost:{port}/docs{Color.END}")
    print(f"\n{Color.YELLOW}Presiona Ctrl+C para detener el servidor{Color.END}\n")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    
    # Build uvicorn command
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "main:app",
        "--host", host,
        "--port", str(port),
    ]
    
    if reload:
        cmd.append("--reload")
    
    # Start the server
    try:
        process = subprocess.run(cmd, cwd=backend_dir)
        return process.returncode
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}👋 Servidor detenido por el usuario{Color.END}")
        return 0


def start_frontend():
    """Start the frontend development server."""
    print(f"\n{Color.BOLD}🚀 Iniciando Frontend Server...{Color.END}")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not (frontend_dir / "package.json").exists():
        print(f"{Color.RED}❌ Frontend no está configurado aún{Color.END}")
        return 1
    
    print(f"{Color.BLUE}URL: http://localhost:5173{Color.END}")
    print(f"\n{Color.YELLOW}Presiona Ctrl+C para detener el servidor{Color.END}\n")
    
    try:
        process = subprocess.run(["npm", "run", "dev"], cwd=frontend_dir)
        return process.returncode
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}👋 Servidor detenido por el usuario{Color.END}")
        return 0


def start_both():
    """Start both backend and frontend servers in parallel using multiprocessing."""
    import time
    import requests
    
    print(f"\n{Color.BOLD}🚀 Iniciando Backend + Frontend...{Color.END}")
    
    # Check frontend setup first
    if not check_frontend_setup():
        print(f"\n{Color.YELLOW}⚠ No se puede iniciar el frontend. Iniciando solo backend...{Color.END}")
        return start_backend(reload=True, host="0.0.0.0", port=8000)
    
    def run_backend():
        """Run backend server in subprocess."""
        backend_dir = Path(__file__).parent / "backend"
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        try:
            subprocess.run(cmd, cwd=backend_dir)
        except FileNotFoundError as e:
            print(f"{Color.RED}❌ Error: No se encontró 'uvicorn'. Asegúrate de que las dependencias estén instaladas.{Color.END}")
            print(f"{Color.YELLOW}Ejecuta: pip install -r backend/requirements.txt{Color.END}")
        except Exception as e:
            print(f"{Color.RED}❌ Error ejecutando backend: {e}{Color.END}")
    
    def run_frontend():
        """Run frontend server in subprocess."""
        frontend_dir = Path(__file__).parent / "frontend"
        
        # Wait for backend health check instead of fixed sleep
        print(f"{Color.BLUE}Esperando a que el backend esté listo...{Color.END}")
        backend_url = "http://localhost:8000/health"
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                response = requests.get(backend_url, timeout=1)
                if response.status_code == 200:
                    print(f"{Color.GREEN}✓ Backend está listo{Color.END}")
                    break
            except requests.RequestException:
                pass
            time.sleep(1)
        else:
            print(f"{Color.YELLOW}⚠ Backend no respondió después de {max_attempts} segundos, iniciando frontend de todos modos...{Color.END}")
        
        try:
            subprocess.run(["npm", "run", "dev"], cwd=frontend_dir)
        except FileNotFoundError:
            print(f"{Color.RED}❌ Error: No se encontró 'npm'. Asegúrate de que Node.js esté instalado.{Color.END}")
        except Exception as e:
            print(f"{Color.RED}❌ Error ejecutando frontend: {e}{Color.END}")
    
    # Create processes - Windows requires this to be inside main guard
    backend_process = multiprocessing.Process(target=run_backend, name="Backend")
    frontend_process = multiprocessing.Process(target=run_frontend, name="Frontend")
    
    try:
        # Start both processes
        print(f"{Color.GREEN}✓ Iniciando Backend en http://localhost:8000{Color.END}")
        backend_process.start()
        
        print(f"{Color.GREEN}✓ Iniciando Frontend en http://localhost:5173{Color.END}")
        frontend_process.start()
        
        print(f"\n{Color.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Color.END}")
        print(f"{Color.BOLD}  Aplicación ejecutándose:{Color.END}")
        print(f"  {Color.GREEN}• Backend:{Color.END}  http://localhost:8000")
        print(f"  {Color.GREEN}• API Docs:{Color.END} http://localhost:8000/docs")
        print(f"  {Color.GREEN}• Frontend:{Color.END} http://localhost:5173")
        print(f"{Color.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Color.END}")
        print(f"\n{Color.YELLOW}Presiona Ctrl+C para detener ambos servidores{Color.END}\n")
        
        # Wait for both processes
        backend_process.join()
        frontend_process.join()
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}👋 Deteniendo servidores...{Color.END}")
        
        # Terminate both processes
        if backend_process.is_alive():
            backend_process.terminate()
            backend_process.join(timeout=5)
            # Force kill if still alive
            if backend_process.is_alive():
                print(f"{Color.YELLOW}⚠ Forzando cierre del backend...{Color.END}")
                backend_process.kill()
                backend_process.join()
        
        if frontend_process.is_alive():
            frontend_process.terminate()
            frontend_process.join(timeout=5)
            # Force kill if still alive
            if frontend_process.is_alive():
                print(f"{Color.YELLOW}⚠ Forzando cierre del frontend...{Color.END}")
                frontend_process.kill()
                frontend_process.join()
        
        print(f"{Color.GREEN}✓ Servidores detenidos{Color.END}")
        return 0
    
    except Exception as e:
        print(f"{Color.RED}❌ Error: {e}{Color.END}")
        
        # Clean up processes
        if backend_process.is_alive():
            backend_process.terminate()
            backend_process.join(timeout=5)
            if backend_process.is_alive():
                backend_process.kill()
                backend_process.join()
        if frontend_process.is_alive():
            frontend_process.terminate()
            frontend_process.join(timeout=5)
            if frontend_process.is_alive():
                frontend_process.kill()
                frontend_process.join()
        
        return 1


def install_dependencies():
    """Install all dependencies."""
    print(f"\n{Color.BOLD}📦 Instalando dependencias...{Color.END}")
    
    # Backend dependencies
    print(f"\n{Color.BLUE}Instalando dependencias del backend...{Color.END}")
    backend_dir = Path(__file__).parent / "backend"
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=backend_dir
    )
    
    if result.returncode != 0:
        print(f"{Color.RED}❌ Error instalando dependencias del backend{Color.END}")
        return 1
    
    # Frontend dependencies
    frontend_dir = Path(__file__).parent / "frontend"
    if (frontend_dir / "package.json").exists():
        print(f"\n{Color.BLUE}Instalando dependencias del frontend...{Color.END}")
        result = subprocess.run(["npm", "install"], cwd=frontend_dir)
        
        if result.returncode != 0:
            print(f"{Color.RED}❌ Error instalando dependencias del frontend{Color.END}")
            return 1
    
    print(f"\n{Color.GREEN}✓ Todas las dependencias instaladas correctamente{Color.END}")
    return 0


def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="Launcher para Revisiones-Traducciones-Ultimate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python launcher.py                    # Inicia backend y frontend juntos (modo por defecto)
  python launcher.py --both             # Inicia backend y frontend juntos
  python launcher.py --backend          # Inicia solo el backend
  python launcher.py --frontend         # Inicia solo el frontend
  python launcher.py --install          # Instala dependencias
  python launcher.py --load-sample-data # Carga datos de ejemplo en la base de datos
  python launcher.py --no-reload        # Inicia con auto-reload desactivado
  python launcher.py --port 8080        # Inicia backend en puerto 8080
        """
    )
    
    # Create mutually exclusive group for mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--backend",
        action="store_true",
        help="Iniciar solo el backend"
    )
    
    mode_group.add_argument(
        "--frontend",
        action="store_true",
        help="Iniciar solo el frontend"
    )
    
    mode_group.add_argument(
        "--both",
        action="store_true",
        help="Iniciar backend y frontend juntos (modo completo)"
    )
    
    parser.add_argument(
        "--install",
        action="store_true",
        help="Instalar dependencias"
    )
    
    parser.add_argument(
        "--load-sample-data",
        action="store_true",
        help="Cargar datos de ejemplo en la base de datos"
    )
    
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Desactivar auto-reload del backend"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host del backend (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Puerto del backend (default: 8000)"
    )
    
    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Saltar verificaciones de inicio"
    )
    
    args = parser.parse_args()
    
    # Print header
    print_header()
    
    # Install dependencies
    if args.install:
        sys.exit(install_dependencies())
    
    # Load sample data
    if args.load_sample_data:
        if not args.skip_checks:
            check_python_version()
            if not check_requirements():
                print(f"\n{Color.YELLOW}Ejecuta: python launcher.py --install{Color.END}")
                sys.exit(1)
            if not check_and_init_database():
                print(f"\n{Color.RED}❌ No se pudo inicializar la base de datos{Color.END}")
                sys.exit(1)
        print(f"\n{Color.BLUE}📦 Cargando datos de ejemplo...{Color.END}")
        load_sample_data()
        sys.exit(0)
    
    # Run checks
    if not args.skip_checks:
        check_python_version()
        if not check_requirements():
            print(f"\n{Color.YELLOW}Ejecuta: python launcher.py --install{Color.END}")
            sys.exit(1)
    
    # Determine what to start
    if args.frontend:
        # Frontend only
        sys.exit(start_frontend())
    elif args.backend:
        # Backend only
        if not args.skip_checks:
            if not check_and_init_database():
                print(f"\n{Color.RED}❌ No se pudo inicializar la base de datos{Color.END}")
                sys.exit(1)
        sys.exit(start_backend(
            reload=not args.no_reload,
            host=args.host,
            port=args.port
        ))
    else:
        # Both (default mode)
        if not args.skip_checks:
            if not check_and_init_database():
                print(f"\n{Color.RED}❌ No se pudo inicializar la base de datos{Color.END}")
                sys.exit(1)
        sys.exit(start_both())

if __name__ == "__main__":
    # Windows multiprocessing requires this guard to prevent infinite process spawning
    # when the script imports itself during Process creation
    multiprocessing.freeze_support()
    main()
