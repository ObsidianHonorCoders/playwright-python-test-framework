@echo off
setlocal
set "PROJECT_ROOT=%~dp0.."

python -m venv "%PROJECT_ROOT%\.venv"
if errorlevel 1 (
    echo Failed to create the virtual environment.
    exit /b 1
)

call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
python -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo Failed to install project dependencies.
    exit /b 1
)

python -m playwright install chromium
if errorlevel 1 (
    echo Failed to install Playwright Chromium.
    exit /b 1
)

echo Virtual environment and dependencies are ready.
echo Activate it with: call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
