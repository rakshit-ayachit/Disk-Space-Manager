import tkinter as tk
from tkinter import ttk

class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message, button1_text, button2_text):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        self.message_label = ttk.Label(self, text=message, wraplength=250, justify="center")
        self.message_label.pack(pady=20)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)

        self.button1 = ttk.Button(self.button_frame, text=button1_text, command=self.on_button1_click)
        self.button1.pack(side="left", padx=10)

        self.button2 = ttk.Button(self.button_frame, text=button2_text, command=self.on_button2_click)
        self.button2.pack(side="right", padx=10)

        self.result = None

    def on_button1_click(self):
        self.result = True
        self.destroy()

    def on_button2_click(self):
        self.result = False
        self.destroy()

def show_custom_message_box(title, message, button1_text, button2_text):
    root = tk.Tk()
    root.withdraw()

    dialog = CustomMessageBox(root, title, message, button1_text, button2_text)
    dialog.wait_window()

    return dialog.result
