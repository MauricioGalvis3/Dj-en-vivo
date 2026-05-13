@echo off
echo ============================================
echo   DJ STACK MASTER - Setup del entorno
echo ============================================
echo.

:: Verificar que Python 3.12 esté disponible
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.12 no encontrado.
    echo Descargalo desde: https://www.python.org/downloads/release/python-3120/
    pause
    exit /b 1
)

echo [OK] Python 3.12 encontrado.
echo.

:: Crear el entorno virtual con Python 3.12
echo [1/3] Creando entorno virtual...
py -3.12 -m venv venv
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual.
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado en la carpeta "venv"
echo.

:: Activar e instalar dependencias
echo [2/3] Instalando librerias...
call venv\Scripts\activate.bat
pip install --upgrade pip --quiet
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de librerias.
    pause
    exit /b 1
)
echo [OK] Librerias instaladas correctamente.
echo.

:: Crear carpetas necesarias si no existen
echo [3/3] Verificando estructura de carpetas...
if not exist "assets\music"  mkdir assets\music
if not exist "assets\temp"   mkdir assets\temp
echo [OK] Carpetas listas.
echo.

echo ============================================
echo   Todo listo. Para ejecutar la app usa:
echo   run.bat
echo ============================================
pause
