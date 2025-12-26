#!/bin/bash
set -e

# 1. Check Python3 and pip
if ! command -v python3 &> /dev/null; then
    echo "Python3 needed! Please install Python3 Environment."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 needed! Please install pip3 first."
    sudo apt update
    sudo apt install -y python3-pip
fi

# 2. Create virtual env
python3 -m venv venv
source venv/bin/activate

# 3. install requirements
pip install --upgrade pip
pip install -r requirements.txt
