@echo off
setlocal enabledelayedexpansion
title NetVide Launcher
cd /d "%~dp0"

echo ========================================================
echo                 NetVide // Bootstrapper
echo ========================================================
echo.

:: 1. Check if Python is installed and available in PATH
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python was not detected on this system.
    echo [*] Downloading official Python 3.12 installer...
    
    set "PY_URL=https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe"
    set "PY_INSTALLER=%TEMP%\python_installer.exe"

    powershell -NoProfile -Command "Invoke-WebRequest -Uri '!PY_URL!' -OutFile '!PY_INSTALLER!'"
    if not exist "!PY_INSTALLER!" (
        echo [ERROR] Failed to download Python installer. Check your internet connection.
        pause
        exit /b 1
    )

    echo [*] Installing Python silently (adding to PATH)...
    "!PY_INSTALLER!" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1
    
    echo [*] Cleaning up installer...
    del "!PY_INSTALLER!" >nul 2>nul

    :: Refresh PATH in the current command session
    for /f "tokens=*" %%a in ('powershell -NoProfile -Command "[System.Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path', 'User')"') do set "PATH=%%a"

    where python >nul 2>nul
    if %errorlevel% neq 0 (
        echo [!] Python installed. Please restart this script once if PATH needs updating.
        pause
        exit /b 0
    )
    echo [+] Python installed successfully!
)

:: 2. Check if PySide6 (Chromium Engine) is installed
python -c "import PySide6" >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] Installing Chromium Engine dependencies (PySide6)...
    python -m pip install --upgrade pip >nul 2>nul
    python -m pip install PySide6
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install PySide6.
        pause
        exit /b 1
    )
    echo [+] Chromium engine ready!
)

:: 3. Launch NetVide
echo [*] Launching NetVide...
python app.py
if %errorlevel% neq 0 (
    echo.
    echo [!] NetVide exited with an error.
    pause
)
