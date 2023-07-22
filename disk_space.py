from tkinter import ttk, font
import tkinter as tk
import psutil


class DiskSpaceVisualizer:
    def __init__(self):
        self.disk_space_info = self._get_disk_space()
        self.root = tk.Tk()
        self.root.title("Disk Space Information")
        self.root.geometry("1100x400")
        self.root.configure(bg="lightblue")

        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.space_font = font.Font(family="Helvetica", size=12)

        self.title_label = tk.Label(self.root, text="Disk Space Information", font=self.title_font, background= "lightblue")
        self.title_label.pack(pady=10)

    def _get_disk_space(self):
        drives = psutil.disk_partitions(all=True)
        disk_space_info = {}

        for drive in drives:
            drive_letter = drive.device.split(":")[0].upper()
            disk_usage = psutil.disk_usage(drive.mountpoint)
            total_space = disk_usage.total
            used_space = disk_usage.used
            free_space = disk_usage.free
            disk_space_info[drive_letter] = {
                "total": total_space,
                "used": used_space,
                "free": free_space,
            }

        return disk_space_info

    def _format_bytes(self, bytes_val):
        for unit in ['', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0

    def display(self):
        for drive, space_info in self.disk_space_info.items():
            total_space = space_info["total"]
            used_space = space_info["used"]
            free_space = space_info["free"]

            frame = ttk.Frame(self.root)
            frame.pack(pady=5)

            label_drive = ttk.Label(frame, text=f"Drive {drive}:", font=self.space_font, background = "lightblue")
            label_drive.pack(side=tk.LEFT)

            total_width = total_space + used_space
            total_percentage = used_space / total_width

            progress_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300, mode='determinate', value=(total_percentage * 100))
            progress_bar.pack(side=tk.LEFT, padx=10)

            label_total = tk.Label(frame, text=f"Total: {self._format_bytes(total_space)}", font=self.space_font, background="lightblue")
            label_total.pack(side=tk.LEFT, padx=10)

            label_used = tk.Label(frame, text=f"Used: {self._format_bytes(used_space)}", font=self.space_font, background = "lightblue")
            label_used.pack(side=tk.LEFT, padx=10)

            label_free = tk.Label(frame, text=f"Free: {self._format_bytes(free_space)}", font=self.space_font, background="lightblue")
            label_free.pack(side=tk.LEFT, padx=10)

        self.root.mainloop()
