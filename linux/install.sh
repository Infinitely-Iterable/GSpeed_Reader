#!/bin/bash

# Function to build the application
build_app() {
    echo "Creating virtual environment..."
    python3 -m venv build_env
    source build_env/bin/activate

    echo "Installing build dependencies..."
    pip install --upgrade pip wheel
    pip install markdown beautifulsoup4 pyinstaller feedparser

    echo "Building application..."
    pyinstaller --clean \
        --onefile \
        --windowed \
        --name obsidian-reader \
        --add-data "/usr/lib/python3/dist-packages/markdown:markdown" \
        --hidden-import markdown \
        --hidden-import markdown.extensions \
        --hidden-import bs4 \
        --hidden-import tkinter \
        --hidden-import feedparser \
        obsidian_reader_linux.py

    deactivate
}

# Function to install the application (requires sudo)
install_app() {
    echo "Installing application..."
    if [ -f "dist/obsidian-reader" ]; then
        sudo install -m 755 dist/obsidian-reader /usr/local/bin/

        echo "Installing desktop file..."
        sudo bash -c 'cat > /usr/share/applications/obsidian-reader.desktop << EOL
[Desktop Entry]
Name=Obsidian Speed Reader
Comment=Speed reading application for Obsidian notes and text
Exec=/usr/local/bin/obsidian-reader
Icon=text-editor
Terminal=false
Type=Application
Categories=Utility;TextTools;
Keywords=speed;read;obsidian;text;
EOL'

        # Create config directory (for all users)
        sudo mkdir -p /etc/obsidian_reader
        sudo update-desktop-database /usr/share/applications

        echo "Cleaning up..."
        rm -rf build_env build dist *.spec

        echo "Installation complete!"
        echo "You can now launch Obsidian Reader from your application menu or run 'obsidian-reader' from the terminal."
    else
        echo "Error: Build failed - executable not found"
        exit 1
    fi
}

# Main script
echo "Building Obsidian Reader..."
build_app

echo "Build complete. The application needs to be installed with sudo privileges."
echo "Please run: sudo ./install.sh --install"

# Check if we're running the install step
if [ "$1" == "--install" ]; then
    if [ "$EUID" -ne 0 ]; then 
        echo "Installation requires root privileges. Please run with sudo."
        exit 1
    fi
    install_app
fi
