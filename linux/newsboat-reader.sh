#!/bin/bash

# Log file location
LOG_FILE="$HOME/newsboat-reader.log"

# Start logging
echo "[$(date)] Script started" > "$LOG_FILE"
echo "[$(date)] Script path: $0" >> "$LOG_FILE"
echo "[$(date)] Current directory: $(pwd)" >> "$LOG_FILE"
echo "[$(date)] Arguments: $@" >> "$LOG_FILE"

# Function to log messages
log() {
    echo "[$(date)] $1" >> "$LOG_FILE"
}

# Check if obsidian-reader is installed
if ! command -v obsidian-reader &> /dev/null; then
    log "Error: obsidian-reader not found"
    exit 1
fi

# Create a temporary file for the content
TEMP_FILE=$(mktemp)
log "Created temp file: $TEMP_FILE"

# Read from stdin and save to temp file
cat > "$TEMP_FILE"
log "Content size: $(wc -c < "$TEMP_FILE") bytes"

# Check if we got any content
if [ ! -s "$TEMP_FILE" ]; then
    log "Error: No content received"
    rm "$TEMP_FILE"
    exit 1
fi

# Send to obsidian-reader
log "Sending to obsidian-reader..."
obsidian-reader --text "$(cat "$TEMP_FILE")" --debug

# Clean up
rm "$TEMP_FILE"
log "Script finished"
