#!/bin/bash

# This script installs required Python libraries for OWL conversion using Python 3

# Abort on errors
set -e

# Check that Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Install it first."
    exit 1
fi

echo "🐍 Creating virtual environment with Python 3..."
python3 -m venv venv
source venv/bin/activate

echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

echo "📦 Installing core libraries..."
pip install rdflib pyshacl jinja2

echo "🧠 Installing reasoning and validation extensions..."
pip install owlrl

echo "✅ All libraries installed successfully!"
echo "👉 To activate the virtual environment later, run:"
echo "source venv/bin/activate"
