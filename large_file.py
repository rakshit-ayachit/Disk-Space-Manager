import os
import hashlib
import tkinter as tk
from tkinter import IntVar, filedialog, messagebox, ttk
import zipfile
import send2trash
import customtkinter as ctk


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

class FileVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File System Visualizer")
        self.root.geometry("500x400")

        self.main_frame = tk.Frame(self.root, bg= "lightblue")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.threshold_label = tk.Label(self.main_frame, text="Enter the threshold for large files (in MB):", bg="lightblue", font = ("Montserrat", 13))
        self.threshold_label.grid(row=0, column=0, padx=5, pady=5)

        self.threshold_entry = tk.Entry(self.main_frame)
        self.threshold_entry.grid(row=0, column=1, padx=5, pady=5)

        self.label = tk.Label(self.main_frame, text="Select Directory:", bg="lightblue", font = ("Montserrat", 13))
        self.label.grid(row=1, column=0, padx=5, pady=5)

        self.browse_button = ctk.CTkButton(self.main_frame, text="Browse", command=self.ask_directory)
        self.browse_button.grid(row=1, column=1, padx=5, pady=5)

        self.file_info_label = tk.Label(self.main_frame, text="", wraplength=350, bg="lightblue", font = "Montserrat")
        self.file_info_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.status_label = tk.Label(self.main_frame, text="", bg="lightblue", font = "Montserrat")
        self.status_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.scroll_canvas = tk.Canvas(self.main_frame, width=400, height=200)
        self.scroll_canvas.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.scroll_frame = tk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_y = tk.Scrollbar(self.main_frame, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_y.grid(row=4, column=2, sticky="ns", padx=5, pady=5)

        self.scroll_canvas.configure(yscrollcommand=self.scroll_y.set)
        self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))

        self.select_all_button = ctk.CTkButton(self.main_frame, text="Select All", command=self.select_all_files)
        self.select_all_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.delete_button = ctk.CTkButton(self.main_frame, text="Delete Selected", command=self.delete_selected_and_show_status)
        self.delete_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.compress_button = ctk.CTkButton(self.main_frame, text="Compress Selected", command=self.compress_selected_files)
        self.compress_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        self.selected_files_var = []

    def ask_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.file_info_label.config(text=f"Selected directory: {directory_path}")
            self.directory_path = directory_path
            self.select_directory_and_show_large_files()


    def get_files_sorted_by_size_and_extension(self, directory: str, threshold_mb: int = 100) -> list:
        files_and_sizes = []
        threshold_bytes = threshold_mb * 1024 * 1024

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                if file_size >= threshold_bytes:
                    files_and_sizes.append((filename, file_size))

        files_and_sizes.sort(key=lambda x: (-x[1], os.path.splitext(x[0])[1]))
        return files_and_sizes

    def delete_selected_files(self, selected_files: list, directory: str, permanent_delete: bool = False) -> int:
        total_cleared_space = 0
        for filename in selected_files:
            file_path = os.path.join(directory, filename)
            try:
                file_size = os.path.getsize(file_path)
                if permanent_delete:
                    os.remove(file_path)
                else:
                    send2trash.send2trash(file_path)  # Move to Recycle Bin or Trash
                total_cleared_space += file_size
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting file {filename}: {e}")
        return total_cleared_space

    def move_to_recycle_bin(self, file_path: str):
        try:
            # On macOS, use shutil.move to move the file to the Trash
            if os.name == 'posix':
                shutil.move(file_path, os.path.join('~', '.Trash', os.path.basename(file_path)))
        except Exception as e:
            raise Exception(f"Error moving file {file_path} to the recycle bin: {e}")

    def select_directory_and_show_large_files(self):
        self.selected_files_var.clear()
        self.scroll_frame.destroy()
        self.scroll_frame = tk.Frame(self.scroll_canvas)
        self.scroll_frame.pack()

        threshold = self.get_threshold_from_entry()
        large_files = self.get_files_sorted_by_size_and_extension(self.directory_path, threshold_mb=threshold)

        if large_files:
            status = "Large files found:"
            self.status_label.config(text=status)

            # Add Checkbox for file selection
            for file, size in large_files:
                var = IntVar()
                checkbox = tk.Checkbutton(self.scroll_frame, text=file, variable=var)
                checkbox.pack(anchor="w")
                self.selected_files_var.append((file, size, var))

        else:
            self.status_label.config(text="No large files (>= 100 MB) found in the directory.")

    def select_all_files(self):
        for _, _, var in self.selected_files_var:
            var.set(1)

    def get_threshold_from_entry(self) -> int:
        try:
            threshold = int(self.threshold_entry.get())
            return threshold
        except ValueError:
            return 100  # Default threshold if input is invalid or empty

    def delete_selected_and_show_status(self):
        selected_files = [file for file, size, var in self.selected_files_var if var.get() == 1]
        if selected_files:
            permanent_delete = messagebox.askyesno("Delete Permanently", "Do you want to delete the selected files permanently?")
            if permanent_delete:
                total_cleared_space = self.delete_selected_files(selected_files, self.directory_path, permanent_delete=True)
                messagebox.showinfo("Deleted", f"Selected files have been deleted permanently.\nTotal space cleared: {self.format_bytes(total_cleared_space)}")
            else:
                total_cleared_space = self.delete_selected_files(selected_files, self.directory_path)
                messagebox.showinfo("Deleted", f"Selected files have been moved to the Recycle Bin.\nTotal space cleared: {self.format_bytes(total_cleared_space)}")
            self.select_directory_and_show_large_files()  # Refresh the file list after deletion
        else:
            messagebox.showinfo("No Files Selected", "Please select files to delete.")

    def compress_selected_files(self):
        selected_files = [file for file, size, var in self.selected_files_var if var.get() == 1]
        if selected_files:
            output_zip = filedialog.asksaveasfilename(defaultextension=".zip")
            if output_zip:
                self.compress_files(output_zip, selected_files)
                messagebox.showinfo("Compression Complete", f"Selected files have been compressed and saved to {output_zip}.")
        else:
            messagebox.showinfo("No Files Selected", "Please select files to compress.")

    def compress_files(self, output_zip: str, files: list):
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                if os.path.isfile(file):
                    zipf.write(file, os.path.basename(file))
                elif os.path.isdir(file):
                    for root, _, filenames in os.walk(file):
                        for filename in filenames:
                            filepath = os.path.join(root, filename)
                            zipf.write(filepath, os.path.relpath(filepath, file))

    @staticmethod
    def format_bytes(size: int) -> str:
        power = 2**10
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return f"{size:.2f} {power_labels[n]}B"

# if __name__ == "__main__":
#      root = tk.Tk()
#      root.configure(bg="lightblue")
#      app = FileVisualizerApp(root)
#      root.mainloop()