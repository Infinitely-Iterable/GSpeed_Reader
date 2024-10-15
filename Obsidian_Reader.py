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

config_file = "config.json"
font_size = 36  # Default font size

MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 52
SPEED_STEP = 25  # ms
MIN_SPEED = 25  # ms
MAX_SPEED = 450  # ms


# .md to plain text
def markdown_to_text(note_path):
    # Read the Markdown file
    with open(note_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    # .md to HTML
    html_content = markdown.markdown(markdown_content)

    # BeautifulSoup to extract text
    soup = BeautifulSoup(html_content, "html.parser")
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
    with open(config_file, "w") as f:
        json.dump({"vault_path": vault_path, "font_size": font_size}, f)


# load vault path from JSON
def load_config():
    try:
        with open(config_file) as f:
            config = json.load(f)
            return config.get("vault_path", ""), config.get("font_size", 36)
    except FileNotFoundError:
        return "", 36


# List all .md files in the Obsidian vault and create a mapping
def list_obsidian_notes(vault_path):
    files = glob.glob(os.path.join(vault_path, "**/*.md"), recursive=True)
    note_mapping = {os.path.basename(file): file for file in files}
    return note_mapping


# Update the dropdown menu
def update_notes_dropdown(vault_path):
    note_mapping = list_obsidian_notes(vault_path)
    note_selector["values"] = list(note_mapping.keys())
    if note_mapping:
        note_selector.current(0)  # first note by default
        display_note_content(list(note_mapping.values())[0])


def on_keyrelease(event):
    value = event.widget.get()
    if value == "":
        note_selector["values"] = list(note_mapping.keys())
    else:
        # Filter
        data = []
        for item in note_selector["values"]:
            if value.lower() in item.lower():
                data.append(item)
        note_selector["values"] = data


# Read the selected note
# def read_selected_note(note_path):
# with open(note_path, 'r', encoding='utf-8') as file:
# return file.read()


# Display selected note in text area
def display_note_content(note_path):
    note_content = markdown_to_text(note_path)
    input_text.delete("1.0", tk.END)  # clear text area
    input_text.insert(tk.END, note_content)  # Insert the new content


def clear_content():
    input_text.delete("1.0", tk.END)  # clear text area


# Called when a note is selected from the dropdown
def on_note_select(event):
    selected_note_name = note_selector.get()
    selected_note_path = note_mapping[selected_note_name]
    display_note_content(selected_note_path)


def dark_mode_toggle():
    global dark_enabled, widget_fg, widget_bg, window_bg
    if dark_enabled:
        dark_enabled = False
        widget_fg = "black"
        widget_bg = "white"
        window_bg = "white"
        dark_mode_button.config(text="Dark Mode")
    else:
        dark_enabled = True
        widget_fg = "white"
        widget_bg = "gray30"
        window_bg = "gray20"
        dark_mode_button.config(text="Light Mode")
    update_colors()


# main window
root = tk.Tk()
root.title("Obsidian Speed Reader")

# word display (fixed size for largest font)
word_frame = tk.Frame(root, width=600, height=100, background="gray30")
word_frame.grid(row=0, column=0, columnspan=3, padx=15, pady=27, sticky="nsew")
word_frame.grid_propagate(False)  # Prevent the frame from resizing

word_label = tk.Label(word_frame, font=("Helvetica", font_size), wraplength=600)
word_label.place(relx=0.5, rely=0.5, anchor="center")

root.grid_rowconfigure(0, minsize=100)  # Set a minimum size for the row
root.grid_columnconfigure(0, minsize=200)  # Set a minimum size for the column
root.grid_columnconfigure(1, minsize=200)  # Set a minimum size for the column
root.grid_columnconfigure(2, minsize=200)  # Set a minimum size for the column

# Function to update font size without changing label size
def update_font_size():
    word_label.config(font=("Helvetica", font_size))
    word_label.place(relx=0.5, rely=0.5, anchor="center")  # Ensure label stays centered

# Text input area
input_text = tk.Text(root, height=10, width=50)
input_text.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

initial_text = text = (
    r"""
                |\_/|                  
                | @ @     
                |   <>              _  
                |  _/\------____ ((| |))
                |=[L]=          `--' |   
            ____|_       ___|   |___.' 
           /_/_____/____/_______|\n"""
)
input_text.insert("1.0", initial_text)


def submit_text():
    global words, current_index
    input_string = input_text.get("1.0", "end-1c")  # pull text from submit
    words = input_string.split()
    current_index = 0  # reset index
    if not is_running:
        toggle_start_pause()


submit_button = tk.Button(root, text="Submit", command=submit_text)
submit_button.grid(row=2, column=0, columnspan=1, padx=10, pady=5, sticky="ew")


def display_words(words):
    global current_index, is_running
    if current_index < len(words) and is_running:
        word_label.config(text=words[current_index])
        current_index += 1
        delay = speed_var.get()  # Use speed_var instead of speed_scale
        root.after(delay, display_words, words)


def toggle_start_pause():
    global is_running
    if is_running:
        is_running = False
    else:
        is_running = True
        display_words(words)


# Load the last used vault path and font size
vault_path, font_size = load_config()
update_font_size()  # Set initial font size

# Select Vault Button
select_vault_button = tk.Button(root, text="Select Vault", command=select_vault_path)
select_vault_button.grid(row=5, column=2, columnspan=1, padx=5, pady=2, sticky="ew")

clear_button = tk.Button(root, text="Clear", command=clear_content)
clear_button.grid(row=2, column=1, columnspan=1, pady=5, padx=10, sticky="ew")

note_selector = ttk.Combobox(root)
note_selector.grid(row=4, column=0, columnspan=3, padx=5, pady=1, sticky="ew")
note_selector.bind("<KeyRelease>", on_keyrelease)
note_selector.bind("<<ComboboxSelected>>", on_note_select)

note_mapping = {}

if vault_path:
    note_mapping = list_obsidian_notes(vault_path)
    update_notes_dropdown(vault_path)

playButton = tk.Button(root, text="Start/Pause", command=toggle_start_pause)
playButton.grid(row=2, column=2, columnspan=1, pady=5, padx=10, sticky="ew")

speed_var = tk.IntVar(value=300)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.grid(row=6, column=0, columnspan=3, pady=10)

# Font size buttons
increase_font_button = tk.Button(button_frame, text="A+", command=lambda: change_font_size(2), width=3)
increase_font_button.pack(side=tk.LEFT, padx=2)

decrease_font_button = tk.Button(button_frame, text="A-", command=lambda: change_font_size(-2), width=3)
decrease_font_button.pack(side=tk.LEFT, padx=2)

# Speed buttons
increase_speed_button = tk.Button(button_frame, text="Speed+", command=lambda: change_speed(-SPEED_STEP), width=6)
increase_speed_button.pack(side=tk.LEFT, padx=2)

decrease_speed_button = tk.Button(button_frame, text="Speed-", command=lambda: change_speed(SPEED_STEP), width=6)
decrease_speed_button.pack(side=tk.LEFT, padx=2)

speed_label = tk.Label(button_frame, textvariable=speed_var)
speed_label.pack(side=tk.LEFT, padx=2)

tk.Label(button_frame, text="ms").pack(side=tk.LEFT)

# set dark mode by default
dark_enabled = True

widget_fg = "white"
widget_bg = "gray30"
window_bg = "gray20"

word_label.config(fg=widget_fg, bg=widget_bg)
input_text.config(fg=widget_fg, bg=widget_bg)
submit_button.config(fg=widget_fg, bg=widget_bg)
playButton.config(fg=widget_fg, bg=widget_bg)
speed_var.set(300)
speed_label.config(textvariable=speed_var)
select_vault_button.config(fg=widget_fg, bg=widget_bg)
clear_button.config(fg=widget_fg, bg=widget_bg)
root.config(bg=window_bg)


# config update --dark toggle
def update_colors():
    global update_colors
    word_frame.config(bg=widget_bg)
    word_label.config(fg=widget_fg, bg=widget_bg)
    input_text.config(fg=widget_fg, bg=widget_bg)
    submit_button.config(fg=widget_fg, bg=widget_bg)
    playButton.config(fg=widget_fg, bg=widget_bg)
    dark_mode_button.config(fg=widget_fg, bg=widget_bg)
    select_vault_button.config(fg=widget_fg, bg=widget_bg)
    clear_button.config(fg=widget_fg, bg=widget_bg)
    increase_font_button.config(fg=widget_fg, bg=widget_bg)
    decrease_font_button.config(fg=widget_fg, bg=widget_bg)
    increase_speed_button.config(fg=widget_fg, bg=widget_bg)
    decrease_speed_button.config(fg=widget_fg, bg=widget_bg)
    speed_label.config(fg=widget_fg, bg=widget_bg)
    button_frame.config(bg=window_bg)
    root.config(bg=window_bg)


def change_font_size(delta):
    global font_size
    new_size = max(MIN_FONT_SIZE, min(font_size + delta, MAX_FONT_SIZE))
    if new_size != font_size:
        font_size = new_size
        update_font_size()
        save_config(vault_path)


def change_speed(delta):
    new_speed = max(MIN_SPEED, min(speed_var.get() + delta, MAX_SPEED))
    speed_var.set(new_speed)
    save_config(vault_path)


root.geometry("625x550")  # Keep the window size fixed
root.mainloop()
