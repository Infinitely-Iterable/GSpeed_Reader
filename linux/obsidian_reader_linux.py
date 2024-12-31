#!/usr/bin/env python3
import sys
import tkinter as tk
from tkinter import ttk, filedialog
import os
import glob
import json
import markdown
from bs4 import BeautifulSoup
import argparse
import logging
import feedparser

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Global variables
current_index = 0
is_running = False
dark_enabled = True
words = []
config_file = "/etc/obsidian_reader/config.json"
font_size = 36  # Default font size

# Constants
MAX_TEXT_LENGTH = 1000000  # ~1MB text limit
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 52
SPEED_STEP = 25  # ms
MIN_SPEED = 25  # ms
MAX_SPEED = 450  # ms

def ensure_config_dir():
    """Ensure the config directory exists"""
    global config_file
    config_dir = os.path.dirname(config_file)
    if not os.path.exists(config_dir):
        try:
            os.makedirs(config_dir, exist_ok=True)
        except PermissionError:
            # Fall back to user's home directory if we can't write to system directory
            config_file = os.path.expanduser("~/.config/obsidian_reader/config.json")
            os.makedirs(os.path.dirname(config_file), exist_ok=True)

def markdown_to_text(note_path):
    """Convert markdown file to plain text"""
    try:
        with open(note_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()
        html_content = markdown.markdown(markdown_content)
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text()
    except Exception as e:
        logger.error(f"Error processing markdown file: {e}")
        return ""

def fetch_rss_content(url):
    """Fetch and parse RSS feed content"""
    try:
        logger.debug(f"Attempting to fetch RSS feed from: {url}")
        feed = feedparser.parse(url)
        logger.debug(f"Feed parsed, found {len(feed.entries)} entries")
        text_content = []
        for entry in feed.entries:
            # Add title
            if hasattr(entry, 'title'):
                logger.debug(f"Adding title: {entry.title}")
                text_content.append(entry.title)
            # Add description/content
            if hasattr(entry, 'description'):
                logger.debug("Found description, parsing HTML")
                soup = BeautifulSoup(entry.description, "html.parser")
                text_content.append(soup.get_text())
            elif hasattr(entry, 'content'):
                logger.debug("Found content field, parsing HTML")
                for content in entry.content:
                    soup = BeautifulSoup(content.value, "html.parser")
                    text_content.append(soup.get_text())
        result = "\n\n".join(text_content)
        logger.debug(f"Total content length: {len(result)} characters")
        return result
    except Exception as e:
        logger.error(f"Error processing RSS feed: {e}")
        return ""

class ObsidianReader:
    def __init__(self, input_text=None):
        self.root = tk.Tk()
        self.root.title("Obsidian Speed Reader")
        self.setup_ui()
        if input_text:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", input_text)
            self.submit_text()

    def setup_ui(self):
        # Configure dark theme
        self.root.configure(bg="gray20")
        
        # word display frame
        self.word_frame = tk.Frame(self.root, width=600, height=100, background="gray30")
        self.word_frame.grid(row=0, column=0, columnspan=3, padx=15, pady=27, sticky="nsew")
        self.word_frame.grid_propagate(False)

        self.word_label = tk.Label(self.word_frame, font=("Helvetica", font_size), 
                                 wraplength=600, fg="white", bg="gray30")
        self.word_label.place(relx=0.5, rely=0.5, anchor="center")

        self.root.grid_rowconfigure(0, minsize=100)
        self.root.grid_columnconfigure(0, minsize=200)
        self.root.grid_columnconfigure(1, minsize=200)
        self.root.grid_columnconfigure(2, minsize=200)

        # Text input area
        self.input_text = tk.Text(self.root, height=10, width=50, bg="gray20", fg="white")
        self.input_text.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        self.root.grid_rowconfigure(1, weight=1)

        # Control buttons with dark theme
        button_style = {"bg": "gray30", "fg": "white", "activebackground": "gray40", 
                       "activeforeground": "white"}
        
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_text, 
                                     **button_style)
        self.submit_button.grid(row=2, column=0, columnspan=1, padx=10, pady=5, sticky="ew")

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_content, 
                                    **button_style)
        self.clear_button.grid(row=2, column=1, columnspan=1, pady=5, padx=10, sticky="ew")

        self.play_button = tk.Button(self.root, text="Start/Pause", 
                                   command=self.toggle_start_pause, **button_style)
        self.play_button.grid(row=2, column=2, columnspan=1, pady=5, padx=10, sticky="ew")

        # Speed control
        self.speed_var = tk.IntVar(value=300)
        
        # Button frame
        self.button_frame = tk.Frame(self.root, bg="gray20")
        self.button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # Speed and font buttons
        for btn_text, cmd in [
            ("Speed+", lambda: self.change_speed(-SPEED_STEP)),
            ("Speed-", lambda: self.change_speed(SPEED_STEP)),
            ("A+", lambda: self.change_font_size(2)),
            ("A-", lambda: self.change_font_size(-2))
        ]:
            width = 6 if "Speed" in btn_text else 3
            btn = tk.Button(self.button_frame, text=btn_text, command=cmd, 
                          width=width, **button_style)
            btn.pack(side=tk.LEFT, padx=2)

        # Window size
        self.root.geometry("625x550")

    def submit_text(self):
        global words, current_index
        input_string = self.input_text.get("1.0", "end-1c")
        if len(input_string) > MAX_TEXT_LENGTH:
            input_string = input_string[:MAX_TEXT_LENGTH]
            logger.warning("Text truncated to 1MB")
        words = input_string.split()
        current_index = 0
        if not is_running:
            self.toggle_start_pause()

    def clear_content(self):
        self.input_text.delete("1.0", tk.END)

    def display_words(self):
        global current_index, is_running
        if current_index < len(words) and is_running:
            self.word_label.config(text=words[current_index])
            current_index += 1
            delay = self.speed_var.get()
            self.root.after(delay, self.display_words)

    def toggle_start_pause(self):
        global is_running
        is_running = not is_running
        if is_running:
            self.display_words()

    def change_speed(self, delta):
        new_speed = self.speed_var.get() + delta
        if MIN_SPEED <= new_speed <= MAX_SPEED:
            self.speed_var.set(new_speed)

    def change_font_size(self, delta):
        global font_size
        new_size = font_size + delta
        if MIN_FONT_SIZE <= new_size <= MAX_FONT_SIZE:
            font_size = new_size
            self.word_label.config(font=("Helvetica", font_size))

    def run(self):
        self.root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Obsidian Speed Reader")
    parser.add_argument("--file", "-f", help="Path to markdown file")
    parser.add_argument("--directory", "-d", help="Path to directory containing markdown files")
    parser.add_argument("--rss", "-r", help="URL of RSS feed to read")
    parser.add_argument("--text", type=str, help="Text to read (optional)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    input_text = None
    if args.file:
        input_text = markdown_to_text(args.file)
    elif args.directory:
        all_text = []
        for md_file in glob.glob(os.path.join(args.directory, "*.md")):
            all_text.append(markdown_to_text(md_file))
        input_text = "\n\n".join(all_text)
    elif args.rss:
        input_text = fetch_rss_content(args.rss)
    elif args.text:
        input_text = args.text
    elif not sys.stdin.isatty():
        try:
            input_text = sys.stdin.read(MAX_TEXT_LENGTH)
            if len(input_text) == MAX_TEXT_LENGTH:
                logger.warning("Input text truncated to 1MB")
        except Exception as e:
            logger.error(f"Error reading from stdin: {e}")
            sys.exit(1)

    try:
        ensure_config_dir()
        app = ObsidianReader(input_text)
        app.run()
    except Exception as e:
        logger.error(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
