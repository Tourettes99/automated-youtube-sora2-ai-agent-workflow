@echo off
REM AI Agent GUI - Startup Script
REM This script launches the AI Agent GUI application
REM Can be used for manual launch or Windows startup automation

echo ========================================
echo AI Agent GUI - Starting...
echo ========================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo.
echo Checking dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo WARNING: Some dependencies may not have installed correctly
)

REM Launch the application
echo.
echo Launching AI Agent GUI...
echo ========================================
echo.

python main.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo Application exited with error code: %errorlevel%
    echo ========================================
    pause
)

exit /b %errorlevel%

