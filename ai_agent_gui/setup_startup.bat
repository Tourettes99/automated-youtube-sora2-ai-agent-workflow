@echo off
REM Setup Windows Startup Task
REM This script creates a scheduled task to run the AI Agent GUI at system startup

echo ========================================
echo AI Agent GUI - Startup Setup
echo ========================================
echo.
echo This will create a Windows Task Scheduler entry to automatically
echo run the AI Agent GUI when Windows starts.
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires Administrator privileges.
    echo Please right-click and select "Run as Administrator"
    pause
    exit /b 1
)

REM Get the full path to the startup script
set "SCRIPT_DIR=%~dp0"
set "STARTUP_SCRIPT=%SCRIPT_DIR%start_ai_agent.bat"

echo Script location: %STARTUP_SCRIPT%
echo.

REM Delete existing task if it exists
schtasks /query /tn "AIAgentGUI" >nul 2>&1
if %errorlevel% equ 0 (
    echo Removing existing task...
    schtasks /delete /tn "AIAgentGUI" /f >nul 2>&1
)

REM Create new scheduled task
echo Creating startup task...
schtasks /create ^
    /tn "AIAgentGUI" ^
    /tr "\"%STARTUP_SCRIPT%\"" ^
    /sc onlogon ^
    /rl highest ^
    /f

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo The AI Agent GUI will now start automatically when you log in.
    echo.
    echo To disable: Open Task Scheduler and disable/delete "AIAgentGUI" task
    echo Or run: schtasks /delete /tn "AIAgentGUI" /f
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR
    echo ========================================
    echo.
    echo Failed to create startup task.
    echo Please check the error messages above.
    echo.
)

pause

