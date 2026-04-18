@echo off
title GreenVibe 
echo ====================================================
echo.

cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo [INFO] PyQt6 not found. Installing...
    python -m pip install PyQt6
    if errorlevel 1 (
        echo [ERROR] Failed to install PyQt6.
        pause
        exit /b 1
    )
)

echo [OK] Launching GreenVibe...
python main.py
if errorlevel 1 (
    echo.
    echo [ERROR] App crashed. Check output above.
)
pause
