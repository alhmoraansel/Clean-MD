# initializer.py

from sqlite3 import Row
import tkinter as tk
from tkinter import Text, Scrollbar, font, Menubutton, Menu, ttk

dark_mode_disabled = True

def markdown_editor_init(self, root):
    self.root = root
    self.root.title("Markdown Normalizer")
    self.file_path = None
    self.original_content = ""
    self.modified_content = ""
    # Maximize the window
    self.root.state('zoomed')
    # Color scheme
    self.bg_color = "#f0f0f0"
    self.text_bg_color = "#ffffff"
    self.button_bg_color = "#3498db"
    self.button_hover_bg_color = "#2980b9"
    self.text_color = "#333333"
    self.title_color = "#2c3e50"
    # Dark mode colors
    self.dark_bg_color = "#1e1e1e"
    self.dark_text_bg_color = "#2d2d2d"
    self.dark_button_bg_color = "#4a4a4a"
    self.dark_button_hover_bg_color = "#5c5c5c"
    self.dark_text_color = "#d4d4d4"
    self.dark_title_color = "#ffffff"
    # Custom font (Congenial) - Ensure you have this font installed!
    try:
        self.base_font = font.Font(family="Congenial", size=12)
    except tk.TclError:
        print("Congenial font not found. Using default font.")
        self.base_font = font.Font(family="Helvetica", size=12)
    self.title_font = font.Font(family=self.base_font.actual("family"), size=14, weight="bold")
    self.text_font = font.Font(family=self.base_font.actual("family"), size=12)
    self.button_font = font.Font(family=self.base_font.actual("family"), size=11, weight="bold")
    # Main frame
    self.frame = tk.Frame(root, bg=self.bg_color)
    self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    # Configure grid weights for resizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    self.frame.grid_rowconfigure(1, weight=1)
    self.frame.grid_columnconfigure(0, weight=1)
    self.frame.grid_columnconfigure(2, weight=1)
    # Original content
    self.original_label = tk.Label(self.frame, text="Original File", font=self.title_font, bg=self.bg_color, fg=self.title_color)
    self.original_label.grid(row=0, column=0, padx=5, sticky="w")
    self.original_text = Text(self.frame, wrap="word", font=self.text_font, undo=True, bg=self.text_bg_color, fg=self.text_color, bd=2, relief="flat")
    self.original_text.grid(row=1, column=0, padx=5, sticky="nsew")
    self.original_scroll = Scrollbar(self.frame, command=self.on_scroll, bg=self.bg_color)
    self.original_scroll.grid(row=1, column=1, sticky="ns")
    self.original_text.configure(yscrollcommand=self.on_scroll)
    # Modified content
    self.modified_label = tk.Label(self.frame, text="Preview Changes", font=self.title_font, bg=self.bg_color, fg=self.title_color)
    self.modified_label.grid(row=0, column=2, padx=5, sticky="w")
    self.modified_text = Text(self.frame, wrap="word", font=self.text_font, bg=self.text_bg_color, fg=self.text_color, undo=True, bd=2, relief="flat")
    self.modified_text.grid(row=1, column=2, padx=5, sticky="nsew")
    self.modified_scroll = Scrollbar(self.frame, command=self.on_scroll, bg=self.bg_color)
    self.modified_scroll.grid(row=1, column=3, sticky="ns")
    self.modified_text.configure(yscrollcommand=self.on_scroll)
    # Button panel
    self.button_frame = tk.Frame(root, bg=self.bg_color)
    self.button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
    # Configure button frame grid
    for i in range(4):
        self.button_frame.grid_columnconfigure(i, weight=1)
    # Button style
    button_style = {
        "font": self.button_font,
        "bg": "#f8f9fa",
        "fg": "#3c4043",
        "relief": "raised",
        "bd": 0,
        "highlightthickness": 0,
        "padx": 20,
        "pady": 10,
        "cursor": "hand2",
        "borderwidth": 0,
        "highlightbackground": "#e8eaed",
        "highlightcolor": "#e8eaed",
    }
    ##REGION Buttons
    self.select_button = self.create_button(self.button_frame, "Select File", self.select_file, button_style)
    self.preview_changes_button = self.create_button(self.button_frame, "Preview", self.preview_changes, button_style)
    self.clean_file_x2_button = self.create_button(self.button_frame, "Clean File x2", self.clean_file_x2, button_style)
    self.save_file_button = self.create_button(self.button_frame, "Save File", self.save_file, button_style)
    self.dark_mode_button = self.create_button(self.button_frame, "Dark Mode", self.toggle_dark_mode, button_style)
    self.select_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    self.preview_changes_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    self.save_file_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
    self.clean_file_x2_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
    self.dark_mode_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

def toggle_dark_mode(self):
    global dark_mode_disabled
    if dark_mode_disabled:
        # Switch to dark mode
        self.root.config(bg=self.dark_bg_color)
        self.frame.config(bg=self.dark_bg_color)
        self.button_frame.config(bg=self.dark_bg_color)
        self.original_label.config(bg=self.dark_bg_color, fg=self.dark_title_color)
        self.modified_label.config(bg=self.dark_bg_color, fg=self.dark_title_color)
        self.original_text.config(bg=self.dark_text_bg_color, fg=self.dark_text_color)
        self.modified_text.config(bg=self.dark_text_bg_color, fg=self.dark_text_color)
        self.original_scroll.config(bg=self.dark_bg_color)
        self.modified_scroll.config(bg=self.dark_bg_color)
        self.select_button.config(bg=self.dark_button_bg_color, fg=self.dark_text_color)
        self.preview_changes_button.config(bg=self.dark_button_bg_color, fg=self.dark_text_color)
        self.clean_file_x2_button.config(bg=self.dark_button_bg_color, fg=self.dark_text_color)
        self.save_file_button.config(bg=self.dark_button_bg_color, fg=self.dark_text_color)
    else:
        # Switch to light mode
        self.root.config(bg=self.bg_color)
        self.frame.config(bg=self.bg_color)
        self.button_frame.config(bg=self.bg_color)
        self.original_label.config(bg=self.bg_color, fg=self.title_color)
        self.modified_label.config(bg=self.bg_color, fg=self.title_color)
        self.original_text.config(bg=self.text_bg_color, fg=self.text_color)
        self.modified_text.config(bg=self.text_bg_color, fg=self.text_color)
        self.original_scroll.config(bg=self.bg_color)
        self.modified_scroll.config(bg=self.bg_color)
        self.select_button.config(bg=self.button_bg_color, fg=self.text_color)
        self.preview_changes_button.config(bg=self.button_bg_color, fg=self.text_color)
        self.clean_file_x2_button.config(bg=self.button_bg_color, fg=self.text_color)
        self.save_file_button.config(bg=self.button_bg_color, fg=self.text_color)
    dark_mode_disabled = not dark_mode_disabled
