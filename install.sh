#!/bin/bash

set -euo pipefail

echo "=========================================="
echo "Installing Python"
echo "=========================================="

sudo apt-get update

sudo apt-get install -y \
    python3 \
    python3-venv \
    python3-dev \
    python3-pip

echo "=========================================="
echo "Python installation completed"
echo "=========================================="

echo "Python version:"
python3 --version

echo "Pip version:"
pip3 --version
