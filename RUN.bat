@echo off
setlocal EnableDelayedExpansion
title Audio Transcriber

:: ============================================
:: 1. Check Python
:: ============================================
python --version >nul 2>&1
if %errorlevel% equ 0 goto python_ok

echo ============================================
echo   Python is not installed
echo ============================================
echo.
echo   To use this app you need to install Python first.
echo.
echo   Steps:
echo     1. A download page will open in your browser.
echo     2. Click the big yellow "Download Python" button.
echo     3. Run the installer.
echo     4. IMPORTANT: Check the box that says "Add python.exe to PATH"
echo     5. Click "Install Now" and wait for it to finish.
echo     6. Close this window and run RUN.bat again.
echo.
echo   Opening download page...
start https://www.python.org/downloads/
echo.
pause
exit /b 1

:python_ok

:: ============================================
:: 2. Check dependencies
:: ============================================
python -c "import openai" >nul 2>&1
if %errorlevel% equ 0 goto deps_ok

echo [...] Installing dependencies (only the first time)...
echo.
pip install openai
if %errorlevel% neq 0 (
    echo [ERROR] There was an error installing dependencies.
    echo.
    pause
    exit /b 1
)
echo.
echo [OK] Dependencies installed.
echo.

:deps_ok

:: ============================================
:: 3. Check API key
:: ============================================
if not exist "input" mkdir input
if not exist "output" mkdir output

set OPENAI_API_KEY=
if exist .env (
    for /f "tokens=1,* delims==" %%a in (.env) do (
        if "%%a"=="OPENAI_API_KEY" set OPENAI_API_KEY=%%b
    )
)

if defined OPENAI_API_KEY goto key_ok

echo ============================================
echo   API Key Configuration (only once)
echo ============================================
echo.
echo You need an OpenAI API key.
echo If you don't have one, create it at: https://platform.openai.com/api-keys
echo.
set /p API_KEY="Paste your API key here: "

if not defined API_KEY (
    echo [ERROR] You didn't enter an API key.
    echo.
    pause
    exit /b 1
)

echo OPENAI_API_KEY=!API_KEY!> .env
set OPENAI_API_KEY=!API_KEY!
echo.
echo [OK] API key saved.
echo.

:key_ok

:: ============================================
:: 4. Main menu
:: ============================================
:menu
echo.
echo ============================================
echo   Audio Transcriber
echo ============================================
echo.
echo   [1] Transcribe files
echo   [2] Exit
echo.
set /p OPTION="Choose an option (1/2): "

if "!OPTION!"=="2" goto exit_app
if "!OPTION!"=="1" goto transcribe
goto menu

:: ============================================
:: 5. Check files and transcribe
:: ============================================
:transcribe

:check_files
dir /b input\*.mp3 input\*.wav input\*.m4a input\*.ogg input\*.mp4 input\*.webm >nul 2>&1
if %errorlevel% equ 0 goto files_ok

echo.
echo [!] No audio files in the "input\" folder
echo     Place your files there and press any key to continue...
echo.
pause >nul
goto check_files

:files_ok
echo.
python transcribe.py
echo.
goto menu

:: ============================================
:: 6. Exit
:: ============================================
:exit_app
echo.
echo Closing app...
timeout /t 2 >nul