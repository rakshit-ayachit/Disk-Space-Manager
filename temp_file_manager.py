import tkinter.messagebox as messagebox
import send2trash
import tempfile
import psutil
import os

class TempFileManager:
    def remove_temp_files(self):
        temp_directory = tempfile.gettempdir()
        temp_file_extensions = ['.tmp', '.temp', '.bak', '.~']
        total_cleared_space = 0
        num_files_deleted = 0

        for root, _, files in os.walk(temp_directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                _, ext = os.path.splitext(filename)
                if ext.lower() in temp_file_extensions:
                    try:
                        if not self.is_file_in_use(file_path):
                            file_size = os.path.getsize(file_path)
                            send2trash.send2trash(file_path)
                            total_cleared_space += file_size
                            num_files_deleted += 1
                    except (PermissionError, OSError) as e:
                        print(f"Error deleting file {filename}: {e}")

        return total_cleared_space, num_files_deleted

    def is_file_in_use(self, file_path):
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if file_path in proc.open_files():
                        return True
                except psutil.NoSuchProcess:
                    pass
        except Exception as e:
            print(f"Error checking if the file is in use: {e}")
        return False

    def show_success_message(self, total_cleared_space, num_files_deleted):
        messagebox.showinfo("Success",
                            f"All temporary files have been removed.\n"
                            f"Total space freed: {self.format_bytes(total_cleared_space)}\n"
                            f"Number of files deleted: {num_files_deleted}")

    @staticmethod
    def format_bytes(size: int) -> str:
        power = 2 ** 10
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return f"{size:.2f} {power_labels[n]}B"
