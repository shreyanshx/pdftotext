#!/bin/bash

set -eou pipefail

echo "Installing Python 3.11..."
sudo apt install -y python3.11 python3.11-venv python3.11-dev pip

PYTHON_VERSION=$(python3.11 --version | awk '{print $2}')
echo "Python version: $PYTHON_VERSION installed successfully."

echo "Installing dependencies..."
pip install -r requirements.txt && echo "Dependencies installed successfully."


