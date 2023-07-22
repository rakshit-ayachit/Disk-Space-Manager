import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import *
import customtkinter as ctk

FILE_EXTENSIONS = {
    "Audio": [".aif", ".cda", ".mid", ".midi", ".mp3", ".mpa", ".ogg", ".wav", ".wma", ".wpl"],
    "Executable": [".apk", ".bat", ".bin", ".cgi", ".pl", ".com", ".exe", ".gadget", ".jar", ".wsf"],
    "Image": [".ai", ".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".ps", ".psd", ".svg", ".tif", ".tiff"],
    "Presentation": [".key", ".odp", ".pps", ".ppt", ".pptx"],
    "Spreadsheet": [".ods", ".xlr", ".xls", ".xlsx"],
    "Video": [".3g2", ".3gp", ".avi", ".flv", ".h264", ".m4v", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", ".rm", ".swf", ".vob", ".wmv"],
    "Document": [".doc", ".docx", ".pdf", ".rtf", ".tex", ".txt", ".wks", ".wps", ".wpd"],
    "Source Code": [".c", ".class", ".cpp", ".cs", ".h", ".py", ".java", ".sh", ".swift", ".vb", ".v", ".css", ".js", ".php", ".htm", ".html"]
}

FILE_COLORS= {

    "Executable": (51/255, 107/255, 135/255),
    "Source Code": (144/255, 175/255, 197/255),
    "Video": (51/255, 107/255, 135/255),
    "Image": (204/255, 56/255, 32/255),
    "Audio": (249/255, 136/255, 102/255),
    "Document": (89/255, 130/255, 52/255),
    "Presentation": (128/255, 189/255, 158/255),
    "Spreadsheet": (137/255, 218/255, 89/255),
    "Other File": (125/255, 68/255, 39/255)

}

class DiskSpaceVisualizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Space Visualizer")
        self.root.geometry("1500x1500")

        self.main_frame = tk.Frame(self.root, background= "lightblue")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.directory_path = tk.StringVar()
        self.file_sizes = {}
        self.fig, self.ax = plt.subplots(figsize = (20,10))  # Create a Figure and Axes objects

        self.create_widgets()

    def get_directory_path(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.directory_path.set(directory_path)
            self.calculate_file_sizes(directory_path)

    def calculate_file_sizes(self, directory_path):
        self.file_sizes = {file_type: 0 for file_type in FILE_EXTENSIONS}
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_extension = os.path.splitext(file)[1].lower()
                for file_type, extensions in FILE_EXTENSIONS.items():
                    if file_extension in extensions:
                        self.file_sizes[file_type] += os.path.getsize(os.path.join(root, file))
                        break

        self.update_pie_chart()

    def update_pie_chart(self):
        labels = []
        sizes = []
        colors = []
        total_size = 0
        for file_type, size in self.file_sizes.items():
            if size > 0:
                labels.append(file_type)
                sizes.append(size)
                colors.append(FILE_COLORS.get(file_type, FILE_COLORS["Other File"]))
                total_size += size

        self.ax.clear()  # Clear previous plot
        wedges, texts, autotexts = self.ax.pie(sizes, colors=colors, autopct='', startangle=90)
        self.ax.axis('equal')
        title_font = {'family': 'Montserrat', 'size': 16}

        self.ax.set_title("File Type Distribution")


        legend_labels = [f"{label} - {size/(1024**2):.2f} MB" for label, size in zip(labels, sizes)]
        self.ax.legend(legend_labels, loc="lower right", bbox_to_anchor=(1, 0.5), prop={'size': 8})

        self.canvas.draw()


    def create_widgets(self):
        # Input directory selection
        directory_frame = ttk.Frame(self.root)
        directory_frame.pack(pady=10)

        ttk.Label(directory_frame, text="Select Directory:", font = ("Montserrat", 13)).pack(side=tk.LEFT)
        ttk.Entry(directory_frame, textvariable=self.directory_path, width=50, state="readonly").pack(side=tk.LEFT)
        ctk.CTkButton(directory_frame, text="Browse", command=self.get_directory_path).pack(side=tk.LEFT)

        # Pie chart frame
        self.pie_frame = ttk.Frame(self.root)
        self.pie_frame.pack(pady=20)

        # Canvas to display the pie chart
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.pie_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = DiskSpaceVisualizerGUI(root)
#     root.mainloop()