@echo off
REM SAXS-XPCS Analysis Suite - Windows Installation Fix
REM This script helps resolve common installation issues on Windows

echo SAXS-XPCS Analysis Suite - Windows Installation Fix
echo ==================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo Python is available
python --version

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo pip is available

REM Run the Python installation fix script
echo.
echo Running Python installation fix script...
python fix_installation.py

REM Check if the installation was successful
python -c "import saxsxpcs" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installation verification failed.
    echo You can try running the application with:
    echo   python run_saxsxpcs.py
) else (
    echo.
    echo Installation successful!
    echo You can now run the application with:
    echo   saxsxpcs
    echo   or
    echo   python -m saxsxpcs.main
)

echo.
echo Press any key to exit...
pause >nul

