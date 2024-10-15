import tkinter as tk
import gui

def main():
    mgui = gui.Window
    root = tk.Tk()
    mgui(root)
    root.wm_title("Obsidian Reader v1.0.0b")
    root.mainloop()

if __name__ == "__main__":
    main()