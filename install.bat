@echo off
REM AI Agent GUI - Installation Script
REM This script sets up the complete environment for the AI Agent GUI

echo ========================================
echo AI Agent GUI - Installation
echo ========================================
echo.

REM Check for Python
echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo ✓ Python found
python --version

REM Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python 3.8 or higher is required
    echo Please upgrade your Python installation
    pause
    exit /b 1
)

echo ✓ Python version is compatible
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv\" (
    echo Virtual environment already exists
    choice /C YN /M "Do you want to recreate it"
    if errorlevel 2 goto skip_venv
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created

:skip_venv
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install requirements
echo.
echo Installing dependencies...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo WARNING: Some packages may have failed to install
    echo The application may still work, but some features might be limited
    echo.
) else (
    echo ✓ All dependencies installed successfully
)

REM Create necessary directories
echo.
echo Creating directories...
if not exist "output\" mkdir output
if not exist "temp\" mkdir temp
if not exist "logs\" mkdir logs
echo ✓ Directories created

REM Check for FFmpeg
echo.
echo Checking for FFmpeg (optional but recommended)...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: FFmpeg not found
    echo FFmpeg is recommended for video processing
    echo Download from: https://ffmpeg.org/download.html
    echo.
    echo The application will work but may have limited video processing capabilities
    echo.
) else (
    echo ✓ FFmpeg found
)

REM Installation complete
echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Get your API keys:
echo    - OpenAI (Sora): https://platform.openai.com/
echo    - Google Gemini: https://ai.google.dev/
echo    - YouTube API: See API_SETUP_GUIDE.md
echo.
echo 2. Launch the application:
echo    - Double-click: start_ai_agent.bat
echo    - Or run: python main.py
echo.
echo 3. Configure your settings in the Settings tab
echo.
echo 4. Set up your schedule in the Schedule tab
echo.
echo 5. Test with "Run Workflow Now"
echo.
echo For detailed instructions, see:
echo - README.md
echo - QUICK_START.md
echo - API_SETUP_GUIDE.md
echo.
echo ========================================
echo.

REM Ask if user wants to launch now
choice /C YN /M "Do you want to launch the application now"
if errorlevel 2 goto end

echo.
echo Launching AI Agent GUI...
python main.py

:end
echo.
pause

