import tkinter as tk
from tkinter import Text, Scrollbar, font, Menubutton, Menu, ttk
import re
from initializer import markdown_editor_init, toggle_dark_mode
from find_replace import FindReplaceWindow
from gui import create_button, on_scroll, select_file, save_file, save_as, update_original_content
from cleaner import clean_file, clean_file_x2, clean_content, process_links, remove_links, process_content_links

class MarkdownEditor:
    __init__ = markdown_editor_init

    def create_button(self, parent, text, command, style):
        return create_button(parent, text, command, style, self.button_hover_bg_color)

    def on_scroll(self, *args):
        on_scroll(self.original_text, self.modified_text, self.original_scroll, self.modified_scroll, *args)

    def select_file(self):
        self.file_path, self.original_content = select_file(self.original_text, self.modified_text, self.status_bar)

    def save_file(self):
        save_file(self.file_path, self.modified_content, self.modified_text, self.status_bar)

    def save_as(self):
        save_as(self.modified_content, self.modified_text, self.status_bar)

    def update_original_content(self):
        self.original_content = update_original_content(self.file_path, self.original_text, self.modified_text)

    def preview_changes(self):
        if not self.original_content:
            self.modified_text.delete(1.0, tk.END)
            self.modified_text.insert(tk.END, "Please select a file first.")
            return
        self.modified_content = clean_content(self.original_content)
        self.highlight_changes()
        self.status_bar.config(text="Previewed changes")

    def clean_file(self):
        clean_file(self)

    def clean_file_x2(self):
        clean_file_x2(self)

    def process_links(self):
        process_links(self)

    def remove_links(self):
        remove_links(self)

    def find_replace(self):
        FindReplaceWindow(self.root, self.modified_text, self.text_font, self.button_font, self.original_content, self.modified_content)

    def highlight_changes(self):
        self.modified_text.delete(1.0, tk.END)
        original_lines = self.original_content.splitlines()
        modified_lines = self.modified_content.splitlines()
        for original_line, modified_line in zip(original_lines, modified_lines):
            if original_line != modified_line:
                self.modified_text.insert(tk.END, modified_line + "\n", "highlight")
            else:
                self.modified_text.insert(tk.END, modified_line + "\n")
        self.modified_text.tag_configure("highlight", background="yellow", foreground="black")

    def toggle_dark_mode(self):
        toggle_dark_mode(self)

# Create the application
root = tk.Tk()
app = MarkdownEditor(root)
root.mainloop()
