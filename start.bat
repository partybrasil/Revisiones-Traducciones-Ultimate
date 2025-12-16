@echo off
REM Windows Batch Launcher for Revisiones-Traducciones-Ultimate
REM Simple double-click script to start the backend

echo.
echo ===============================================================
echo   Revisiones-Traducciones-Ultimate v1.0.0
echo   Sistema de Gestion de Fichas de Producto Multiidioma
echo ===============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor, instala Python 3.11+ desde https://www.python.org
    pause
    exit /b 1
)

REM Launch the application
echo Iniciando servidor backend...
echo.
python launcher.py

pause
