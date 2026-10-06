@echo off
title NetVide Launcher
cd /d "%~dp0"

echo ========================================================
echo                 NetVide Launcher
echo ========================================================
echo.

:: 1. Check Python
where python >nul 2>nul
if errorlevel 1 goto install_python
goto check_pyside

:install_python
echo [!] Python was not detected on this system.
echo [*] Downloading and installing Python...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$u='https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe'; $f=Join-Path $env:TEMP 'py_inst.exe'; Invoke-WebRequest -Uri $u -OutFile $f; Start-Process -FilePath $f -ArgumentList '/quiet','PrependPath=1','Include_pip=1' -Wait; Remove-Item $f -Force;"
echo [+] Python installation complete. Please restart run.cmd.
pause
exit /b 0

:check_pyside
:: 2. Check PySide6
python -c "import PySide6" >nul 2>nul
if errorlevel 1 goto install_pyside
goto launch

:install_pyside
echo [*] Installing Chromium Engine (PySide6)...
python -m pip install PySide6
if errorlevel 1 (
    echo [ERROR] Failed to install PySide6. Check your internet connection.
    pause
    exit /b 1
)
echo [+] Chromium engine ready!

:launch
:: 3. Launch
echo [*] Launching NetVide...
python app.py
if errorlevel 1 (
    echo.
    echo [!] NetVide exited with an error.
    pause
)
