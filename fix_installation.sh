#!/bin/bash
# SAXS-XPCS Analysis Suite - Linux Installation Fix
# This script helps resolve common installation issues on Linux

echo "SAXS-XPCS Analysis Suite - Linux Installation Fix"
echo "=================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not installed"
        echo "Please install Python 3.7 or higher"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python is available"
$PYTHON_CMD --version

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        echo "Error: pip is not available"
        echo "Please install pip"
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

echo "pip is available"

# Run the Python installation fix script
echo ""
echo "Running Python installation fix script..."
$PYTHON_CMD fix_installation.py

# Check if the installation was successful
if $PYTHON_CMD -c "import saxsxpcs" &> /dev/null; then
    echo ""
    echo "Installation successful!"
    echo "You can now run the application with:"
    echo "  saxsxpcs"
    echo "  or"
    echo "  $PYTHON_CMD -m saxsxpcs.main"
else
    echo ""
    echo "Installation verification failed."
    echo "You can try running the application with:"
    echo "  $PYTHON_CMD run_saxsxpcs.py"
fi

echo ""
echo "Press Enter to exit..."
read

