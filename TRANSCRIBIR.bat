@echo off
title Transcriptor de Audio

:: Cargar API key desde .env
if exist .env (
    for /f "tokens=1,* delims==" %%a in (.env) do (
        if "%%a"=="OPENAI_API_KEY" set OPENAI_API_KEY=%%b
    )
)

if "%OPENAI_API_KEY%"=="" (
    echo [ERROR] No se encontro la API key.
    echo         Ejecuta SETUP.bat primero.
    echo.
    pause
    exit /b 1
)

:: Verificar que hay archivos en input
dir /b input\*.mp3 input\*.wav input\*.m4a input\*.ogg input\*.mp4 input\*.webm >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] No hay archivos de audio en la carpeta "input\"
    echo         Pone tus MP3 ahi y volve a ejecutar.
    echo.
    pause
    exit /b 1
)

:: Ejecutar transcriptor
python transcribe.py

echo.
pause