#!/bin/bash
# Quick Start Script for File Converter

echo "🚀 File Converter - Setup & Launch Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.7+"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo ""

# Create virtual environment (optional but recommended)
echo "📦 Setting up environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "⚠️  Some dependencies may have failed. Trying alternative method..."
    pip install flask python-docx PyPDF2 Pillow python-pptx reportlab
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📝 To start the converter:"
echo "   python main.py"
echo ""
echo "🌐 Then open in your browser:"
echo "   http://localhost:5000"
echo ""
echo "✨ Enjoy converting!"
