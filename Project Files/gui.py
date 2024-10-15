import tkinter as tk
from tkinter import ttk

class Window(ttk.Frame):
    def __init__(self, master=None):
        import reader
        self.master = master
        super().__init__(master)
        self.master.style = ttk.Style()
        self.master.style.theme_use("clam")
        
        # word display
        self.word_label = ttk.Label(master, font=('Helvetica', 38))
        self.word_label.grid(row=0, column=0, columnspan=3, rowspan=2, padx=15, sticky='ew')

        self.input_text = ttk.Entry(master)
        self.input_text.grid(row=2, column=0, columnspan=3, rowspan=2, pady=10, padx=10, ipady=20)
        initial_text = r'''
                        |\_/|                  
                        | @ @     
                        |   <>              _  
                        |  _/\------____ ((| |))
                        |=[L]=          `--' |   
                    ____|_       ___|   |___.' 
                /_/_____/____/_______|\n'''
        

        self.tts_var = tk.IntVar()
        self.tts_checkbox = ttk.Checkbutton(master, text="Text to Speech", variable=self.tts_var)
        self.tts_checkbox.grid(row=3, column=3, columnspan=1, padx=10, pady=5, sticky='ew')

        self.submit_button = ttk.Button(master, text="Submit", command=reader.submit_text)
        self.submit_button.grid(row=4, column=0, columnspan=1, padx=10, pady=5, sticky='ew')

        # Select Vault Button
        self.select_vault_button = ttk.Button(master, text="Select Vault", command=reader.select_vault_path)
        self.select_vault_button.grid(row=7, column=2, columnspan=1, padx=5, pady=2, sticky='ew')

        self.clear_button = ttk.Button(master, text="Clear", command=reader.clear_content)
        self.clear_button.grid(row=4, column=1, columnspan=1, pady=5, padx=10, sticky='ew')

        self.note_selector = ttk.Combobox(master)
        self.note_selector.grid(row=5, column=0, columnspan=2, rowspan=2, padx=5, pady=1,sticky='ew')
        self.note_selector.bind('<KeyRelease>', reader.on_keyrelease)
        self.note_selector.bind('<<ComboboxSelected>>', reader.on_note_select)

        self.note_mapping = {}

        if reader.vault_path:
            self.note_mapping = reader.list_obsidian_notes(reader.vault_path)

        self.playButton = ttk.Button(master, text="Start/Pause", command=reader.toggle_start_pause)
        self.playButton.grid(row=4, column=2, columnspan=1, pady=5, padx=10, sticky='ew')

        self.speed_scale = tk.Scale(master, from_=25, to=450, orient='horizontal', label='Speed (ms)')
        self.speed_scale.set(300)
        self.speed_scale.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='ew')