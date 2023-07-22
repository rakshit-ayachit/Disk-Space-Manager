from files_visualizer import FileSystemTree, visualize, filedialog
from custom_msg import CustomMessageBox,show_custom_message_box
from visualisation_piechart import DiskSpaceVisualizerGUI
from temp_file_manager import TempFileManager
from tkinter import filedialog, messagebox
from large_file import LargeFile
from file_compression import compress_files 
from same_type_files import FileSelectorGUI
from disk_space import DiskSpaceVisualizer
from duplicate import DuplicateFilesGUI
from delete import FileDeletionGUI
from tkinter import filedialog
import customtkinter as ctk
from typing import List
from tkinter import *
import tkinter as tk
import pygame
import os
import math
import sys

def open_directory():
    directory = filedialog.askdirectory()
    if directory:
        file_tree = FileSystemTree(directory)
        visualize(file_tree)

def check_free():
    disk_space_gui = DiskSpaceVisualizer()
    disk_space_gui.mainloop()

def check_dup():
    duplicate_files_gui = DuplicateFilesGUI()
    duplicate_files_gui.mainloop()

def file_del():
    del_disk=FileDeletionGUI()
    del_disk.mainloop()

def same_file():
    file_selector_gui = FileSelectorGUI()
    file_selector_gui.mainloop()

def disk_space():
    disk_space_visualisation = DiskSpaceVisualizer()
    disk_space_visualisation.display()
    

def open_file_visualizer_app():
    result = show_custom_message_box(
        title="Message Box",
        message="Please choose the visualisation:",
        button1_text="SSD Representaion",
        button2_text="Pie Chart"
    )

    if result is not None:
        if result:
            open_directory()
        else:
            root = tk.Toplevel()
            app = DiskSpaceVisualizerGUI(root)
    
        

def compress():
    directory = filedialog.askdirectory()
    if directory:
        files = [os.path.join(directory, f) for f in os.listdir(directory)]
        output_zip = filedialog.asksaveasfilename(defaultextension='.zip', filetypes=[("ZIP files", "*.zip")])
        compress_files(output_zip, files)

def remove_temp_files():
    temp_manager = TempFileManager()
    total_cleared_space, num_files_deleted = temp_manager.remove_temp_files()
    temp_manager.show_success_message(total_cleared_space, num_files_deleted)

def display_disk_utilization():
    root = tk.Toplevel()
    app = DiskSpaceVisualizerGUI(root)

def show_large():
    root = tk.Tk()
    app = LargeFile(root)
    root.mainloop()



if __name__ == "__main__":
    root = tk.Tk()
    root.title("File System Manager")

    root.geometry(f"{500}x{500}")
    root.configure(bg="lightblue")

    header_label = tk.Label(root, text="Disk Space Manager", font=("Montserrat", 25, "bold"), bg="lightblue")
    header_label.pack(pady=10)

    content_label = tk.Label(root, text="A GUI application of all functions to manage your disk space.", 
                             bg="lightblue", font=("Montserrat", 13,))
    content_label.pack(pady=10)

    free_button = ctk.CTkButton(root,text="Display Disk Space", command=disk_space, font= ("Montserrat", 13))
    free_button.pack(padx=10,pady=10)

    visualize_button = ctk.CTkButton(root, text="Visualize Files", command=open_file_visualizer_app, font= ("Montserrat", 13))
    visualize_button.pack(padx=10,pady=10)

    duplicate_button=ctk.CTkButton(root,text="Find Duplicate Files",command=check_dup, font= ("Montserrat", 13))
    duplicate_button.pack(padx=10,pady=10)

    file_visualizer_button = ctk.CTkButton(root, text="Find Large Files", command=show_large, font= ("Montserrat", 13))
    file_visualizer_button.pack(padx=10,pady=10)

    delete_button=ctk.CTkButton(root,text="Delete Files",command=file_del, font= ("Montserrat", 13))
    delete_button.pack(padx=10,pady=10)

    sametype_button=ctk.CTkButton(root,text="Find File Type",command=same_file, font= ("Montserrat", 13))
    sametype_button.pack(pady=10)

    compress_button = ctk.CTkButton(root, text="Compress Files", command=compress, font=("Montserrat", 13))
    compress_button.pack(pady=10)

    temp_button = ctk.CTkButton(root, text="Remove Temp Files", command=remove_temp_files, font=("Montserrat", 13))
    temp_button.pack(pady=10)


    root.mainloop()
