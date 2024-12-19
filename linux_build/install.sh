#!/bin/bash

# Function to safely remove old files
remove_if_exists() {
    if [ -f "$1" ]; then
        echo "Removing old file: $1"
        sudo rm "$1"
    fi
}

# Build the application
pyinstaller Obsidian_Reader.spec

# Create necessary directories
sudo mkdir -p /usr/local/bin
sudo mkdir -p /usr/share/applications
sudo mkdir -p /usr/share/icons/hicolor/256x256/apps

# Remove old files if they exist
remove_if_exists "/usr/local/bin/Obsidian_Reader"
remove_if_exists "/usr/share/applications/ObsidianReader.desktop"
remove_if_exists "/usr/share/icons/hicolor/256x256/apps/obsidianreader.png"

# Copy the executable
sudo cp dist/Obsidian_Reader /usr/local/bin/

# Copy the desktop entry
sudo cp ObsidianReader.desktop /usr/share/applications/

# Copy the icon
sudo cp ../icon_assets/icon.png /usr/share/icons/hicolor/256x256/apps/obsidianreader.png

# Make the executable executable
sudo chmod +x /usr/local/bin/Obsidian_Reader

# Update desktop database
sudo update-desktop-database

echo "Installation complete! You can now launch Obsidian Reader from your applications menu."
