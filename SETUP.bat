@echo off
title Instalador - Transcriptor de Audio

echo ============================================
echo   Instalador del Transcriptor de Audio
echo ============================================
echo.

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado.
    echo.
    echo Descargalo de: https://www.python.org/downloads/
    echo IMPORTANTE: Marca la casilla "Add Python to PATH" al instalar.
    echo.
    echo Despues de instalar Python, volve a ejecutar este archivo.
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado:
python --version
echo.

:: Instalar dependencias (incluye ffmpeg embebido, no hace falta instalarlo aparte)
echo [...] Instalando dependencias...
echo.
pip install openai noisereduce pydub imageio-ffmpeg numpy audioop-lts
echo.

if %errorlevel% neq 0 (
    echo [ERROR] Hubo un error instalando las dependencias.
    echo.
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas
echo.

:: Crear carpetas
if not exist "input" mkdir input
if not exist "output" mkdir output

echo [OK] Carpetas creadas: input\ y output\
echo.

:: Pedir API key
echo ============================================
echo   Configuracion de la API Key de OpenAI
echo ============================================
echo.
echo Necesitas una API key de OpenAI.
echo Si no tenes una, creala en: https://platform.openai.com/api-keys
echo.

set /p API_KEY="Pega tu API key aca: "

if "%API_KEY%"=="" (
    echo [ERROR] No ingresaste una API key. Podes configurarla despues.
    echo.
    pause
    exit /b 1
)

:: Guardar API key en archivo .env local
echo OPENAI_API_KEY=%API_KEY%> .env

echo.
echo [OK] API key guardada en archivo .env
echo.
echo ============================================
echo   Todo listo!
echo ============================================
echo.
echo   1. Pone tus archivos MP3 en la carpeta "input\"
echo   2. Hace doble click en "TRANSCRIBIR.bat"
echo   3. Los textos van a aparecer en "output\"
echo.
pause