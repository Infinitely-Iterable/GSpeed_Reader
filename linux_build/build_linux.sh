#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_linux.txt

# Build the executable
pyinstaller --onefile --windowed Obsidian_Reader.py

# Cleanup
deactivate

echo "Build complete! The executable can be found in the dist directory."
