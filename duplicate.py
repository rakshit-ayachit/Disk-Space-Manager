from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import tkinter as tk
import hashlib
import os

def get_file_hash(file_path, block_size=65536):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(block_size)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def find_duplicate_files(directory):
    file_hashes = {}
    duplicate_files = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_hash = get_file_hash(file_path)
            if file_hash in file_hashes:
                duplicate_files.append((os.path.basename(file_hashes[file_hash]), os.path.basename(file_path)))
            else:
                file_hashes[file_hash] = file_path

    return duplicate_files

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            return False
    except Exception as e:
        return False

class DuplicateFilesGUI(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Duplicate Files Finder")
        self.geometry("800x600")
        self.configure(bg="lightblue")

        self.label = tk.Label(self, text="Select a directory to find duplicate files:", bg="lightblue", font = "Montserrat")
        self.label.pack(pady=10)

        self.directory_var = tk.StringVar()
        self.directory_entry = tk.Entry(self, textvariable=self.directory_var, width=40)
        self.directory_entry.pack(pady=5)

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.select_directory)
        self.browse_button.pack(pady=5)

        self.find_button = ctk.CTkButton(self, text="Find Duplicate Files", command=self.find_duplicates)
        self.find_button.pack(pady=10)

        self.result_frame = tk.Frame(self)
        self.result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(self.result_frame, wrap="word", width=60, height=15)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.result_frame, command=self.result_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=self.scrollbar.set)

        self.select_all_var = tk.IntVar()
        self.select_all_checkbutton = ctk.CTkCheckBox(self, text="Select All", command=self.toggle_select_all, 
                                                      variable=self.select_all_var, font= ("Montserrat", 13), text_color= "black")
        self.select_all_checkbutton.pack(pady=5)

        self.delete_button = ctk.CTkButton(self, text="Delete Selected", command=self.delete_selected_duplicates)
        self.delete_button.pack(pady=5)

        self.duplicate_pairs = []
        self.checkboxes = []
        self.scrollable_frame = None

    def toggle_select_all(self):
        select_all_state = self.select_all_var.get()
        for var, _, _ in self.checkboxes:
            var.set(select_all_state)

    def select_directory(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.directory_var.set(selected_directory)

    def find_duplicates(self):
        directory = self.directory_var.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory.")
            return

        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory path.")
            return

        self.result_text.delete(1.0, tk.END)
        self.duplicate_pairs = find_duplicate_files(directory)

        if not self.duplicate_pairs:
            self.result_text.insert(tk.END, "No duplicate files found.")
        else:
            self.create_scrollable_frame()
            self.checkboxes = []
            for i, (file1, file2) in enumerate(self.duplicate_pairs, start=1):
                var = tk.IntVar()
                checkbox = ctk.CTkCheckBox(self.scrollable_frame, text=f"{file1} -- {file2}", variable=var, onvalue=1, offvalue=0,
                                           font= ("Montserrat", 13), text_color= "black", bg_color="white")
                checkbox.pack(anchor=tk.W)
                self.checkboxes.append((var, file1, file2))

    def create_scrollable_frame(self):
        if self.scrollable_frame:
            self.scrollable_frame.destroy()

        self.scrollable_frame = tk.Frame(self.result_text)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)
        self.result_text.window_create(tk.END, window=self.scrollable_frame)

    def delete_selected_duplicates(self):
        selected_indices = [i for i, (var, _, _) in enumerate(self.checkboxes) if var.get() == 1]

        if selected_indices:
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected duplicates?")
            if confirm:
                directory = self.directory_var.get()
                duplicates_to_delete = [self.duplicate_pairs[index][0] for index in selected_indices]
                
                with ThreadPoolExecutor() as executor:
                    results = list(executor.map(delete_file, [os.path.join(directory, file_to_delete) for file_to_delete in duplicates_to_delete]))

                for i, (file_to_delete, result) in enumerate(zip(duplicates_to_delete, results)):
                    if result:
                        self.result_text.insert(tk.END, f"Deleted: {file_to_delete}\n")
                        del self.duplicate_pairs[selected_indices[i]]
                    else:
                        self.result_text.insert(tk.END, f"Error: Unable to delete {file_to_delete}\n")

                for checkbox in self.scrollable_frame.winfo_children():
                    checkbox.destroy()
