from __future__ import annotations
import os
import math
from tkinter import messagebox
import pygame
from typing import List, Tuple, Optional
import os
import math
import pygame
import sys
import tkinter as tk
from tkinter import filedialog
from typing import List, Tuple, Optional


    
DIMENSIONS = (1024, 576)
FILE_EXTENSIONS = {"Audio": [".aif", ".cda", ".mid", ".midi", "mp3",
                             ".mpa", ".ogg", ".wav", ".wma", ".wpl"],
                   "Executable": [".apk", ".bat", ".bin", ".cgi", ".pl",
                                  ".com", ".exe", ".gadget", ".jar", ".wsf"],
                   "Image": [".ai", ".bmp", "gif", "ico", ".jpeg", "jpg",
                             ".png", ".ps", ".psd", ".svg", ".tif", "tiff"],
                   "Presentation": [".key", ".odp", ".pps", ".ppt", ".pptx"],
                   "Spreadsheet": [".ods", ".xlr", ".xls", ".xlsx"],
                   "Video": [".3g2", ".3gp", ".avi", ".flv", ".h264", ".m4v",
                             ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", ".rm",
                             ".swf", ".vob", ".wmv"],
                   "Document": [".doc", ".docx", ".pdf", ".rtf", ".tex",
                                ".txt", ".wks", ".wps", ".wpd"],
                   "Source Code": [".c", ".class", ".cpp", ".cs", ".h", ".py",
                                   ".java", ".sh", ".swift", ".vb", ".v",
                                   ".css", ".js", ".php", ".htm", ".html"]}

FILE_COLORS = {"Executable": (51, 107, 135),
               "Source Code": (144, 175, 197),
               "Video": (255, 66, 14),
               "Image": (204, 56, 32),
               "Audio": (249, 136, 102),
               "Document": (89, 130, 52),
               "Presentation": (128, 189, 158),
               "Spreadsheet": (137, 218, 89),
               "Other File": (125, 68, 39)}
class FileSystemTree:
    rect: Tuple[int, int, int, int] = (0, 0, 0, 0)
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[FileSystemTree]
    _parent_tree: Optional[FileSystemTree] = None
    _expanded: bool = False

    def __init__(self, directory: str) -> None:
        self._name = os.path.basename(directory)
        self._init_subtrees(directory)
        self._init_colour(self._name)
        self._init_data_size(directory)

    def _init_subtrees(self, directory: str) -> None:
        self._subtrees = []
        if os.path.isdir(directory):
            for filename in os.listdir(directory):
                subitem = FileSystemTree(os.path.join(directory, filename))
                self._subtrees.append(subitem)

        for subtree in self._subtrees:
            subtree._parent_tree = self

    def _init_colour(self, name: str) -> None:
        if len(self._subtrees) > 0:
            self._colour = (100, 100, 100)
        else:
            file_type = "Other File"
            for category in FILE_EXTENSIONS:
                for extension in FILE_EXTENSIONS[category]:
                    if name.lower().endswith(extension):
                        file_type = category
            self._colour = FILE_COLORS[file_type]

    def _init_data_size(self, directory: str) -> None:
        if len(self._subtrees) == 0:
            if os.path.isdir(directory):
                self.data_size = 1
            else:
                self.data_size = os.path.getsize(directory)
        elif self._name is not None:
            total_size = 0
            for tree in self._subtrees:
                total_size += tree.data_size
            self.data_size = total_size

    def construct_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        self.rect = rect
        x, y, width, height = rect
        total_area = width * height

        if len(self._subtrees) == 0 or height == 0 or width == 0:
            self.rect = rect
        elif height >= width:
            self._construct_horizontal_recs(rect, total_area)
        elif height < width:
            self._construct_vertical_recs(rect, total_area)

    def _construct_horizontal_recs(self, rect: Tuple[int, int, int, int],
                                   total_area: int) -> None:
        counter = 1
        x, y, width, height = rect
        for subtree in self._subtrees:
            if self.data_size != 0:
                target_ratio = subtree.data_size / self.data_size
            else:
                target_ratio = 0
            target_area = target_ratio * total_area

            if counter == len(self._subtrees):
                subtree.rect = (x, y, width, height)
                subtree.construct_rectangles((x, y, width, height))
            else:
                y_change = math.floor(target_area / width)
                height -= y_change
                subtree.construct_rectangles((x, y, width, y_change))
                y += y_change
                counter += 1

    def _construct_vertical_recs(self, rect: Tuple[int, int, int, int],
                                 total_area: int):
        counter = 1
        x, y, width, height = rect
        for subtree in self._subtrees:
            if self.data_size != 0:
                target_ratio = subtree.data_size / self.data_size
            else:
                target_ratio = 0
            target_area = target_ratio * total_area

            if counter == len(self._subtrees):
                subtree.rect = (x, y, width, height)
                subtree.construct_rectangles((x, y, width, height))
            else:
                x_change = math.floor(target_area / height)
                width -= x_change
                subtree.construct_rectangles((x, y, x_change, height))
                x += x_change
                counter += 1

    def get_visible_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                                   Tuple[int, int, int]]]:
        if self._expanded is False:
            return [(self.rect, self._colour)]
        else:
            ret = []
            for subtree in self._subtrees:
                ret.extend(subtree.get_visible_rectangles())
            return ret

    def expand(self, expand_all: bool) -> None:
        if len(self._subtrees) != 0:
            self._expanded = True
        if expand_all:
            for subtree in self._subtrees:
                subtree.expand(True)
            return None

    def collapse(self, collapse_all: bool) -> None:
        traverse_tree = self
        if collapse_all:
            while traverse_tree._parent_tree is not None:
                traverse_tree = traverse_tree._parent_tree
        else:
            traverse_tree = traverse_tree._parent_tree
        traverse_tree._collapse_helper()

    def _collapse_helper(self) -> None:
        self._expanded = False
        for subtree in self._subtrees:
            subtree._collapse_helper()

    def get_tree_at_position(self, pos: Tuple[int, int]) -> \
            Optional[FileSystemTree]:
        visible_recs = []
        for rect_and_color in self.get_visible_rectangles():
            visible_recs.append(rect_and_color[0]) 

        possible_rects = []
        for rect in visible_recs:
            if rect[0] <= pos[0] <= rect[0] + rect[2] \
                    and rect[1] <= pos[1] <= rect[1] + rect[3]:
                possible_rects.append(rect)

        return self._find_tree_by_rect(
            self._conflict_resolver(possible_rects, pos))

    def _find_tree_by_rect(self, rect: Tuple) -> Optional[FileSystemTree]:
        if self.rect is rect:
            return self
        else:
            for subtree in self._subtrees:
                if subtree._find_tree_by_rect(rect) is not None:
                    return subtree._find_tree_by_rect(rect)
        return None

    @staticmethod
    def _conflict_resolver(possible_rects: List, pos: Tuple) \
            -> Optional[Tuple[int, int, int, int]]:
        x_conflict = 0
        y_conflict = 0

        for rec in possible_rects:
            if rec[0] == pos[0]:
                x_conflict += 0.5
            if rec[0] + rec[2] == pos[0]:
                x_conflict += 0.5
            if rec[1] == pos[1]:
                y_conflict += 0.5
            if rec[1] + rec[3] == pos[1]:
                y_conflict += 0.5

        for rect in possible_rects:
            if x_conflict >= 1 and rect[0] == pos[0]:
                possible_rects.remove(rect)
            elif y_conflict >= 1 and rect[1] == pos[1]:
                possible_rects.remove(rect)

        if len(possible_rects) == 0:
            return None
        else:
            return possible_rects[0]

    def get_directory(self) -> str:
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_directory() + os.sep + self._name


def visualize(tree: FileSystemTree) -> None:
    pygame.init()
    screen = pygame.display.set_mode(DIMENSIONS)
    pygame.display.set_caption("Simple Python File System Visualizer")
    _render(screen, tree, None)
    tree.construct_rectangles((0, 0, DIMENSIONS[0], DIMENSIONS[1] - 25))
    tree.expand(True)
    _input_loop(screen, tree)


def _render(surface: pygame.Surface, tree: Optional[FileSystemTree],
            selected_item: Optional[FileSystemTree]) -> None:
    _clear_screen(surface)
    _add_legend(surface)
    sub_surface = surface.subsurface(
        (0, 0, DIMENSIONS[0] - 180, DIMENSIONS[1] - 25))
    _draw_rectangles(sub_surface, tree, selected_item)
    _render_text(surface, _get_display_text(selected_item))
    pygame.display.flip()


def _draw_rectangles(surface: pygame.Surface, tree: Optional[FileSystemTree],
                     selected_item: Optional[FileSystemTree]) -> None:
    for rect in tree.get_visible_rectangles():
        pygame.draw.rect(surface, rect[1], rect[0])
        pygame.draw.rect(surface, (0, 0, 0), rect[0], 1)
    if selected_item is not None:
        pygame.draw.rect(surface, (255, 255, 255), selected_item.rect, 2)


def _add_legend(title_text: pygame.Surface) -> None:
    sub_surface = title_text.subsurface((DIMENSIONS[0] - 178, 0,
                                         178, DIMENSIONS[1] - 25))
    pygame.draw.rect(sub_surface, pygame.color.THECOLORS["aliceblue"],
                     (0, 0, 178, DIMENSIONS[1] - 25))
    sub_surface.blit(pygame.font.SysFont("Segoe UI", 30, True).render
                     ("Legend", 1, pygame.color.THECOLORS["black"]), (35, 15))
    _add_legend_items(sub_surface)
    _add_author(sub_surface)


def _add_legend_items(surface: pygame.Surface) -> None:
    surface.blit(pygame.font.SysFont("Segoe UI", 15).
                 render("Folder", 1, pygame.color.THECOLORS["black"]), (60, 70))
    pygame.draw.rect(surface, (100, 100, 100), (30, 74, 15, 15))
    pygame.draw.rect(surface, (0, 0, 0), (30, 74, 15, 15), 1)

    y_position = 95
    for item in FILE_COLORS:
            surface.blit(pygame.font.SysFont("Segoe UI", 15).
                         render(item, 1, pygame.color.THECOLORS["black"]),
                         (60, y_position))
            pygame.draw.rect(surface, FILE_COLORS[item],
                             (30, y_position + 4, 15, 15))
            pygame.draw.rect(surface, (0, 0, 0),
                             (30, y_position + 4, 15, 15), 1)
            y_position += 25


def _add_author(surface: pygame.Surface) -> None:
    surface.blit(pygame.font.SysFont("Segoe UI", 15).render
                 ("Petuh Pakhuh", 1, pygame.color.THECOLORS["black"]),
                 (27, DIMENSIONS[1] - 55))


def _clear_screen(surface: pygame.Surface) -> None:
    pygame.draw.rect(surface, pygame.color.THECOLORS["black"],
                     (0, 0, DIMENSIONS[0], DIMENSIONS[1]))


def _render_text(screen: pygame.Surface, text: str) -> None:
    screen.blit(pygame.font.SysFont("Segoe UI", 17)
                .render(text, 1, pygame.color.THECOLORS['white']),
                (5, DIMENSIONS[1] - 25))


def _input_loop(screen: pygame.Surface, tree: FileSystemTree) -> None:
    while True:
        event = pygame.event.poll()
        selected = tree.get_tree_at_position(pygame.mouse.get_pos())

        if event.type == pygame.QUIT:
            return None
        elif event.type == pygame.MOUSEBUTTONUP:
            _handle_click(event.button, selected)
        elif event.type == pygame.KEYUP and selected is not None:
            if event.key == pygame.K_e:
                selected.expand(True)
            elif event.key == pygame.K_c:
                selected.collapse(True)

        _render(screen, tree, selected)


def _handle_click(mouse_act: int, selected: Optional[FileSystemTree]) -> None:
    if selected is None:
        pass
    elif mouse_act == 1:  # Left click
        selected.expand(False)
    elif mouse_act == 3:  # Right click
        selected.collapse(False)


def _get_display_text(selected: Optional[FileSystemTree]) -> str:
    if selected is None:
        return "No file or folder selected."
    else:
        return selected.get_directory() + \
               " (Size: {})".format(_get_size_text(selected))


def _get_size_text(selected: Optional[FileSystemTree]) -> str:
    size_bits = selected.data_size
    unit = " Bytes"
    if size_bits > 1073741824:
        size_bits = round(size_bits / 1073741824, 2)
        unit = " GB"
    elif size_bits > 1048576:
        size_bits = round(size_bits / 1048576, 2)
        unit = " MB"
    elif size_bits > 1024:
        size_bits = round(size_bits / 1024, 2)
        unit = " KB"
    elif size_bits == 1:
        unit = " Byte"
    return str(size_bits) + unit

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

if __name__ == "__main__":
    root = tk.Toplevel()
    root.title("File System Manager")

    # Set the main window size
    root.geometry(f"{500}x{500}")
    root.configure(bg="lightblue")

    # ... (previous code remains unchanged) ...

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()