import tkinter as tk
from tkinter import ttk, filedialog
import os
import glob
import json
import markdown
from bs4 import BeautifulSoup
from gui import Window

current_index = 0
is_running = False
words = []
config_file = 'config.json'

def create_speedconfig_folder():
    documents_folder = os.path.expanduser("~/Documents")
    speedconfig_folder = os.path.join(documents_folder, "speedconfig")
    os.makedirs(speedconfig_folder, exist_ok=True)
    return speedconfig_folder

# .md to plain text
def markdown_to_text(note_path):
    # Read the Markdown file
    with open(note_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    # .md to HTML
    html_content = markdown.markdown(markdown_content)

    # BeautifulSoup to extract text
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()

    return text

# Function to select a new Obsidian vault path
def select_vault_path():
    path = filedialog.askdirectory()
    if path:
        save_config(path)
        update_notes_dropdown(path)
    return path

# save vault path to a JSON file
def save_config(vault_path):
    speedconfig_folder = create_speedconfig_folder()
    config_file = os.path.join(speedconfig_folder, 'config.json')
    with open(config_file, 'w') as f:
        json.dump({'vault_path': vault_path}, f)

# load vault path from JSON
def load_config():
    speedconfig_folder = create_speedconfig_folder()
    config_file = os.path.join(speedconfig_folder, 'config.json')
    try:
        with open(config_file) as f:
            config = json.load(f)
            return config.get('vault_path', '')
    except FileNotFoundError:
        return ''

# Load the last used vault path
vault_path = load_config()

# List all .md files in the Obsidian vault and create a mapping
def list_obsidian_notes(vault_path):
    files = glob.glob(os.path.join(vault_path, '**/*.md'), recursive=True)
    note_mapping = {os.path.basename(file): file for file in files}
    return note_mapping

# Update the dropdown menu
note_selector = ttk.Combobox()  # Define the note_selector variable

def update_notes_dropdown(vault_path):
    note_mapping = list_obsidian_notes(vault_path)
    note_selector['values'] = list(note_mapping.keys())
    if note_mapping:
        note_selector.current(0)  # first note by default
        display_note_content(list(note_mapping.values())[0])

def on_keyrelease(event):
    value = event.widget.get()
    note_mapping = note_mapping
    if value == '':
        note_selector['values'] = list(note_mapping.keys())
    else:
        # Filter
        data = []
        for item in note_selector['values']:
            if value.lower() in item.lower():
                data.append(item)
        note_selector['values'] = data

# Read the selected note
def read_selected_note(note_path):
    with open(note_path, 'r', encoding='utf-8') as file:
        return file.read()
    
# Display selected note in text area
def display_note_content(note_path):
    win_inst = Window()
    note_content = markdown_to_text(note_path)
    win_inst.input_text.delete('1.0', tk.END)  # clear text area
    win_inst.input_text.insert(tk.END, note_content)  # Insert the new content

def clear_content():
    win_inst = Window()
    win_inst.input_text.delete('1.0', tk.END)  # clear text area

# Called when a note is selected from the dropdown
def on_note_select(event):
    win_inst = Window()
    selected_note_name = note_selector.get()
    selected_note_path = win_inst.note_mapping[selected_note_name]
    display_note_content(selected_note_path)

# def dark_mode_toggle():
#     global dark_enabled, widget_fg, widget_bg, window_bg
#     if dark_enabled:
#         dark_enabled = False
#         widget_fg = 'black'
#         widget_bg = 'white'
#         window_bg = 'white'
#         dark_mode_button.config(text="Dark Mode")
#     else:
#         dark_enabled = True
#         widget_fg = 'white'
#         widget_bg = 'gray30'
#         window_bg = 'gray20'
#         dark_mode_button.config(text="Light Mode")
#     update_colors()

def display_words(words, index=0):
    win_inst = Window()
    if index < len(words):
        word = words[index]
        win_inst.word_label.config(text=word)
        index += 1
        win_inst.after(1000, display_words, words, index)

def submit_text():
    win_inst = Window()
    global words, current_index
    input_string = win_inst.input_text.get("1.0", "end-1c")  #pull text from submit
    words = input_string.split()
    current_index = 0  #reset index
    if not is_running:
        toggle_start_pause()

def display_words(words):
    win_inst = Window()
    global current_index, is_running
    if current_index < len(words) and is_running:
        win_inst.word_label.config(text=words[current_index])
        current_index += 1
        delay = win_inst.speed_scale.get()  #pull delay from scale
        win_inst.after(delay, display_words, words)

def toggle_start_pause():
    global is_running
    if is_running:
        is_running = False
    else:
        is_running = True
        display_words(words)


