import tkinter as tk
from tkinter import ttk, filedialog
import os
import glob
import json
import markdown
from bs4 import BeautifulSoup

current_index = 0
is_running = False
dark_enabled = False

words = []

config_file = 'config.json'

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

# save vault path to a JSON file
def save_config(vault_path):
    with open(config_file, 'w') as f:
        json.dump({'vault_path': vault_path}, f)

# load vault path from JSON
def load_config():
    try:
        with open(config_file) as f:
            config = json.load(f)
            return config.get('vault_path', '')
    except FileNotFoundError:
        return ''

# List all .md files in the Obsidian vault and create a mapping
def list_obsidian_notes(vault_path):
    files = glob.glob(os.path.join(vault_path, '**/*.md'), recursive=True)
    note_mapping = {os.path.basename(file): file for file in files}
    return note_mapping

# Update the dropdown menu
def update_notes_dropdown(vault_path):
    note_mapping = list_obsidian_notes(vault_path)
    note_selector['values'] = list(note_mapping.keys())
    if note_mapping:
        note_selector.current(0)  # first note by default
        display_note_content(list(note_mapping.values())[0])

def on_keyrelease(event):
    value = event.widget.get()
    if value == '':
        note_selector['values'] = note_selector['values']
    else:
        # Filter
        data = []
        for item in note_selector['values']:
            if value.lower() in item.lower():
                data.append(item)
        note_selector['values'] = data

# Read the selected note
# def read_selected_note(note_path):
    # with open(note_path, 'r', encoding='utf-8') as file:
        # return file.read()
    
# Display selected note in text area
def display_note_content(note_path):
    note_content = markdown_to_text(note_path)
    input_text.delete('1.0', tk.END)  # clear text area
    input_text.insert(tk.END, note_content)  # Insert the new content

def clear_content():
    input_text.delete('1.0', tk.END)  # clear text area

# Called when a note is selected from the dropdown
def on_note_select(event):
    selected_note_name = note_selector.get()
    selected_note_path = note_mapping[selected_note_name]
    display_note_content(selected_note_path)

def dark_mode_toggle():
    global dark_enabled, widget_fg, widget_bg, window_bg
    if dark_enabled:
        dark_enabled = False
        widget_fg = 'black'
        widget_bg = 'white'
        window_bg = 'white'
    else:
        dark_enabled = True
        widget_fg = 'white'
        widget_bg = 'gray30'
        window_bg = 'gray20'
    update_colors()

def display_words(words, index=0):
    if index < len(words):
        word = words[index]
        word_label.config(text=word)
        index += 1
        root.after(1000, display_words, words, index)

#main window
root = tk.Tk()
root.title("Obsidian Speed Reader")

#word display
word_label = tk.Label(root, font=('Helvetica', 36))
word_label.grid(row=0, column=0, columnspan=3, padx=15, pady=20, sticky='ew')
is_running = False

input_text = tk.Text(root, height=10, width=50)
input_text.grid(row=1, column=0, columnspan=3, pady=10, padx=10)
initial_text = text=('''
                |\_/|                  
                | @ @     
                |   <>              _  
                |  _/\------____ ((| |))
                |=[L]=          `--' |   
            ____|_       ___|   |___.' 
            /_/_____/____/_______|\n''')
input_text.insert("1.0", initial_text)

def submit_text():
    global words, current_index
    input_string = input_text.get("1.0", "end-1c")  #pull text from submit
    words = input_string.split()
    current_index = 0  #reset index
    if not is_running:
        toggle_start_pause()

submit_button = tk.Button(root, text="Submit", command=submit_text)
submit_button.grid(row=2, column=0, columnspan=1, padx=10, pady=5, sticky='ew')

def display_words(words):
    global current_index, is_running
    if current_index < len(words) and is_running:
        word_label.config(text=words[current_index])
        current_index += 1
        delay = speed_scale.get()  #pull delay from scale
        root.after(delay, display_words, words)

def toggle_start_pause():
    global is_running
    if is_running:
        is_running = False
    else:
        is_running = True
        display_words(words)

# Load the last used vault path
vault_path = load_config()

# Select Vault Button
select_vault_button = tk.Button(root, text="Select Vault", command=select_vault_path)
select_vault_button.grid(row=5, column=2, columnspan=1, padx=5, pady=2, sticky='ew')

clear_button = tk.Button(root, text="Clear", command=clear_content)
clear_button.grid(row=2, column=1, columnspan=1, pady=5, padx=10, sticky='ew')

note_selector = ttk.Combobox(root)
note_selector.grid(row=4, column=0, columnspan=2, rowspan=2, padx=5, pady=1,sticky='ew')
note_selector.bind('<KeyRelease>', on_keyrelease)
note_selector.bind('<<ComboboxSelected>>', on_note_select)

note_mapping = {}

if vault_path:
    note_mapping = list_obsidian_notes(vault_path)

playButton = tk.Button(root, text="Start/Pause", command=toggle_start_pause)
playButton.grid(row=2, column=2, columnspan=1, pady=5, padx=10, sticky='ew')

speed_scale = tk.Scale(root, from_=25, to=450, orient='horizontal', label='Speed (ms)')
speed_scale.set(300)
speed_scale.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

dark_mode_button = tk.Button(root, text="Dark Mode", command=dark_mode_toggle)
dark_mode_button.grid(row=4, column=2, columnspan=1, padx=5, pady=3, sticky='ew')

#config update --dark toggle
def update_colors():
    global update_colors
    word_label.config(fg=widget_fg, bg=widget_bg)
    input_text.config(fg=widget_fg, bg=widget_bg)
    submit_button.config(fg=widget_fg, bg=widget_bg)
    playButton.config(fg=widget_fg, bg=widget_bg)
    speed_scale.config(fg=widget_fg, bg=widget_bg)
    dark_mode_button.config(fg=widget_fg, bg=widget_bg)
    select_vault_button.config(fg=widget_fg, bg=widget_bg)
    clear_button.config(fg=widget_fg, bg=widget_bg)
    root.config(bg=window_bg)
    

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.mainloop()
