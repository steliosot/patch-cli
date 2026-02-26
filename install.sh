#!/bin/bash
set -e

echo "=========================================="
echo "  Patch CLI Installer"
echo "=========================================="
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not found. Please install Python 3.8 or later"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info.major)')
echo "Found Python 3.$PYTHON_VERSION"

if [ "$PYTHON_VERSION" -lt 8 ]; then
    echo "[ERROR] Python 3.8 or later required (found 3.$PYTHON_VERSION)"
    exit 1
fi
echo "✓ Python version OK"

# Install dependencies
echo ""
echo "[2/5] Installing dependencies..."
if command -v python3 &> /dev/null; then
    # First try with standard installation
    python3 -m pip install --upgrade pip setuptools 2>/dev/null || true
    python3 -m pip install openai tqdm --break-system-packages 2>/dev/null || true
    
    if [ $? -eq 0 ]; then
        echo "✓ Dependencies installed"
    else
        echo "[!] Standard install failed, trying with flags..."
        echo "    Re-running with --break-system-packages flag..."
        python3 -m pip install --break-system-packages openai tqdm || true
        if [ $? -ne 0 ]; then
            echo "[WARNING] Could not install. Manual install required:"
            echo "    Try: python3 -m pip install --break-system-packages openai tqdm"
            echo ""
            echo "Alternatively, create virtual environment:"
            echo "  python3 -m venv venv && source venv/bin/activate"
            echo "  venv/bin/pip install openai tqdm"
            exit 1
        else
            echo "✓ Dependencies installed (with --break-system-packages)"
        fi
    fi
else
    echo "[ERROR] python3 not found"
    exit 1
fi

# Make script executable
echo ""
echo "[3/5] Setting up patch CLI..."
chmod +x patch.py docker_test_suite.py lsp_checker.py

# Create virtual environment
echo ""
echo "[4/5] Creating virtual environment (optional)..."
if ! command -v virtualenv &> /dev/null; then
    echo "  [WARNING] virtualenv not found. Run: pip install virtualenv"
else
    echo "  Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
fi

# Installation summary
echo ""
echo "[5/5] Installation summary:"
echo "  ├─ Python: python3 (v$PYTHON_VERSION required)"
echo "  ├─ Dependencies: openai, tqdm"
echo "  ├─ Docker: docker (optional, for real builds)"
echo "  └─ Command: ./patch.py <command>"
echo ""

echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
echo "Usage:"
echo "  ./patch.py \"sudo systemctl start docker\""
echo "  ./patch.py \"docker ps\""
echo "  python3 patch.py --help"
echo ""
echo "For Docker testing:"
echo "  python3 docker_test_suite.py"
echo ""
echo "Documentation: README.md"
echo "=========================================="