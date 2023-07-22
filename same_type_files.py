from tkinter import filedialog, ttk, messagebox
from file_compression import compress_files
import customtkinter as ctk
import tkinter as tk
import os

class FileSelectorGUI(tk.Toplevel):
    FILE_EXTENSIONS = {
        "Audio": [".aif", ".cda", ".mid", ".midi", ".mp3",
                  ".mpa", ".ogg", ".wav", ".wma", ".wpl"],
        "Executable": [".apk", ".bat", ".bin", ".cgi", ".pl",
                       ".com", ".exe", ".gadget", ".jar", ".wsf"],
        "Image": [".ai", ".bmp", ".gif", ".ico", ".jpeg", ".jpg",
                  ".png", ".ps", ".psd", ".svg", ".tif", ".tiff"],
        "Presentation": [".key", ".odp", ".pps", ".ppt", ".pptx"],
        "Spreadsheet": [".ods", ".xlr", ".xls", ".xlsx"],
        "Video": [".3g2", ".3gp", ".avi", ".flv", ".h264", ".m4v",
                  ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", ".rm",
                  ".swf", ".vob", ".wmv"],
        "Document": [".doc", ".docx", ".pdf", ".rtf", ".tex",
                     ".txt", ".wks", ".wps", ".wpd"],
        "Source Code": [".c", ".class", ".cpp", ".cs", ".h", ".py",
                        ".java", ".sh", ".swift", ".vb", ".v",
                        ".css", ".js", ".php", ".htm", ".html"]
    }

    def __init__(self):
        super().__init__()
        self.title("File Selector")
        self.geometry("800x600")
        self.configure(bg="lightblue")

        self.directory_frame = tk.Frame(self)
        self.directory_frame.pack(pady=10)

        self.directory_label = tk.Label(self.directory_frame, text="Select Directory:", font= ("Montserrat", 13), bg= "lightblue")
        self.directory_label.pack(side=tk.LEFT)

        self.directory_var = tk.StringVar()
        self.directory_entry = tk.Entry(self.directory_frame, textvariable=self.directory_var, width=30)
        self.directory_entry.pack(side=tk.LEFT)

        self.browse_button = ctk.CTkButton(self.directory_frame, text="Browse", command=self.select_directory)
        self.browse_button.pack(side=tk.LEFT, padx = 6)

        self.file_type_label = tk.Label(self, text="Select file type:", font= ("Montserrat", 13), bg= "lightblue")
        self.file_type_label.pack(pady=5)

        self.file_type_var = tk.StringVar()
        self.file_type_combobox = ttk.Combobox(self, textvariable=self.file_type_var, values=list(self.FILE_EXTENSIONS.keys()), state="readonly")
        self.file_type_combobox.pack()

        self.enter_button = ctk.CTkButton(self, text="Enter", command=self.display_files)
        self.enter_button.pack(pady=10)

        self.file_list = tk.Listbox(self, width=50, height=15, selectmode=tk.EXTENDED)
        self.file_list.pack(pady=10)

        self.total_space_label = tk.Label(self, text="Total Space: ", font= ("Montserrat", 13), bg= "lightblue")
        self.total_space_label.pack(pady=10)

        # Add select all button
        self.select_all_button = ctk.CTkButton(self, text="Select All", command=self.select_all)
        self.select_all_button.pack(pady=8)

        # Add delete selected button
        self.delete_selected_button = ctk.CTkButton(self, text="Delete Selected", command=self.delete_selected)
        self.delete_selected_button.pack(pady=8)

        # Add compress selected button
        self.compress_selected_button = ctk.CTkButton(self, text="Compress Selected", command=self.compress_selected)
        self.compress_selected_button.pack(pady=8)

    def select_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.directory_var.set(directory_path)

    def display_files(self):
        directory_path = self.directory_var.get()
        file_type = self.file_type_var.get()

        if file_type not in self.FILE_EXTENSIONS:
            self.file_list.delete(0, tk.END)
            self.file_list.insert(tk.END, "Invalid file type.")
            self.total_space_label.config(text="Total Space: ")
            return

        extensions = self.FILE_EXTENSIONS[file_type]
        if not os.path.exists(directory_path):
            self.file_list.delete(0, tk.END)
            self.file_list.insert(tk.END, "Directory not found.")
            self.total_space_label.config(text="Total Space: ")
            return

        self.file_list.delete(0, tk.END)
        total_space = 0
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            if os.path.isfile(filepath) and os.path.splitext(filename)[1].lower() in extensions:
                self.file_list.insert(tk.END, filename)
                total_space += os.path.getsize(filepath)

        self.total_space_label.config(text=f"Total Space: {self.format_bytes(total_space)}")

    def format_bytes(self, bytes_val):
        for unit in ['', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0

    def select_all(self):
        self.file_list.select_set(0, tk.END)

    def delete_selected(self):
        selected_indices = self.file_list.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "No files selected for deletion.")
            return

        confirm_delete = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected_indices)} files?")
        if confirm_delete:
            directory_path = self.directory_var.get()
            for index in reversed(selected_indices):
                filename = self.file_list.get(index)
                filepath = os.path.join(directory_path, filename)
                try:
                    os.remove(filepath)
                    self.file_list.delete(index)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete {filename}: {e}")

    def compress_selected(self):
        selected_indices = self.file_list.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "No files selected for compression.")
            return

        files_to_compress = []
        directory_path = self.directory_var.get()
        extensions = self.FILE_EXTENSIONS[self.file_type_var.get()]

        for index in selected_indices:
            filename = self.file_list.get(index)
            filepath = os.path.join(directory_path, filename)
            if os.path.isfile(filepath) and os.path.splitext(filename)[1].lower() in extensions:
                files_to_compress.append(filepath)

        if not files_to_compress:
            messagebox.showwarning("Invalid Selection", "No valid files selected for compression.")
            return

        output_zip = filedialog.asksaveasfilename(defaultextension='.zip', filetypes=[("ZIP files", "*.zip")])
        if output_zip:
            compress_files(output_zip, files_to_compress)
            messagebox.showinfo("Success", "Files compressed successfully.")
        else:
            messagebox.showwarning("Warning", "Compression canceled.")
   
