import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import customtkinter as ctk

class FileDeletionGUI(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("File Deletion GUI")
        self.geometry("500x250")
        self.configure(bg="lightblue")

        self.label = tk.Label(self, text="Select the file or directory to delete:", bg="lightblue", font = ("Montserrat", 13))
        self.label.pack(pady=10)

        self.path_var = tk.StringVar()
        self.path_entry = tk.Entry(self, textvariable=self.path_var, width=40)
        self.path_entry.pack(pady=5)

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.select_file_or_directory)
        self.browse_button.pack(pady=5)

        self.delete_button = ctk.CTkButton(self, text="Delete", command=self.delete_file_or_directory)
        self.delete_button.pack(pady=10)

    def select_file_or_directory(self):
        path = filedialog.askopenfilename()
        if path:
            self.path_var.set(path)

    def delete_file_or_directory(self):
        path = self.path_var.get()
        if not path:
            messagebox.showerror("Error", "Please select a file or directory.")
            return

        if not os.path.exists(path):
            messagebox.showerror("Error", "The selected file or directory does not exist.")
            return

        try:
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
            messagebox.showinfo("Deleted", f"'{path}' deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting '{path}': {e}")
