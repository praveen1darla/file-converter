@echo off
REM Quick Start Script for File Converter (Windows)

echo 🚀 File Converter - Setup & Launch Script
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7+
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION% found

REM Create virtual environment (optional but recommended)
echo.
echo 📦 Setting up environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies from requirements.txt...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

if errorlevel 0 (
    echo ✅ Dependencies installed successfully
) else (
    echo ⚠️  Some dependencies may have failed. Trying alternative method...
    pip install flask python-docx PyPDF2 Pillow python-pptx reportlab
)

echo.
echo 🎉 Setup complete!
echo.
echo 📝 To start the converter:
echo    python main.py
echo.
echo 🌐 Then open in your browser:
echo    http://localhost:5000
echo.
echo ✨ Enjoy converting!
echo.
pause
