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


def check_database():
    """Check if database is accessible."""
    print(f"\n{Color.BOLD}Verificando base de datos...{Color.END}")
    try:
        from backend.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"{Color.GREEN}✓ Base de datos conectada{Color.END}")
        return True
    except Exception as e:
        print(f"{Color.YELLOW}⚠ Base de datos no accesible: {e}{Color.END}")
        print(f"{Color.YELLOW}Asegúrate de que PostgreSQL está ejecutándose y configurado en backend/.env{Color.END}")
        return False


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
    """Start both backend and frontend servers."""
    print(f"\n{Color.BOLD}🚀 Iniciando Backend + Frontend...{Color.END}")
    print(f"{Color.YELLOW}Esta función requiere ejecutar en terminales separadas{Color.END}")
    print(f"\nTerminal 1: python launcher.py --backend")
    print(f"Terminal 2: python launcher.py --frontend")
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
  python launcher.py                    # Inicia el backend (modo por defecto)
  python launcher.py --backend          # Inicia el backend
  python launcher.py --frontend         # Inicia el frontend
  python launcher.py --install          # Instala dependencias
  python launcher.py --no-reload        # Inicia backend sin auto-reload
  python launcher.py --port 8080        # Inicia backend en puerto 8080
        """
    )
    
    parser.add_argument(
        "--backend",
        action="store_true",
        help="Iniciar solo el backend"
    )
    
    parser.add_argument(
        "--frontend",
        action="store_true",
        help="Iniciar solo el frontend"
    )
    
    parser.add_argument(
        "--install",
        action="store_true",
        help="Instalar dependencias"
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
    
    # Run checks
    if not args.skip_checks:
        check_python_version()
        if not check_requirements():
            print(f"\n{Color.YELLOW}Ejecuta: python launcher.py --install{Color.END}")
            sys.exit(1)
    
    # Determine what to start
    if args.frontend:
        sys.exit(start_frontend())
    elif args.backend or (not args.frontend):
        # Backend is default
        if not args.skip_checks:
            check_database()
        sys.exit(start_backend(
            reload=not args.no_reload,
            host=args.host,
            port=args.port
        ))
    else:
        sys.exit(start_both())


if __name__ == "__main__":
    main()
