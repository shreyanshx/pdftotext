#!/bin/bash

set -eou pipefail

echo "Installing Python..."
sudo apt install -y python3 python3-venv python3-dev python3-pip

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "Python version: $PYTHON_VERSION installed successfully."

