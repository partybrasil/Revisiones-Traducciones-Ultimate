#!/bin/bash
# Linux/macOS Shell Launcher for Revisiones-Traducciones-Ultimate
# Simple script to start the backend

echo ""
echo "==============================================================="
echo "  Revisiones-Traducciones-Ultimate v1.0.0"
echo "  Sistema de Gestión de Fichas de Producto Multiidioma"
echo "==============================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Por favor, instala Python 3.11+ desde https://www.python.org"
    exit 1
fi

# Launch the application
echo "Iniciando servidor backend..."
echo ""
python3 launcher.py
