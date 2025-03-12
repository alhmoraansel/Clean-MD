import tkinter as tk
from tkinter import font, filedialog, Text, Scrollbar
import os

class MarkdownEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Asterisk Normalizer")
        self.file_path = None
        self.original_content = ""
        self.modified_content = ""

        # Color scheme
        self.bg_color = "#f0f0f0"
        self.text_bg_color = "#ffffff"
        self.button_bg_color = "#3498db"
        self.button_hover_bg_color = "#2980b9"
        self.text_color = "#333333"
        self.title_color = "#2c3e50"

        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.text_font = font.Font(family="Courier", size=12)
        self.button_font = font.Font(family="Helvetica", size=11, weight="bold")

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
        self.original_text = Text(self.frame, wrap="word", font=self.text_font, undo=True, bg=self.text_bg_color, fg=self.text_color, bd=2, relief="groove")
        self.original_text.grid(row=1, column=0, padx=5, sticky="nsew")
        self.original_scroll = Scrollbar(self.frame, command=self.on_scroll, bg=self.bg_color)
        self.original_scroll.grid(row=1, column=1, sticky="ns")
        self.original_text.configure(yscrollcommand=self.original_scroll.set)

        # Modified content
        self.modified_label = tk.Label(self.frame, text="Preview Changes", font=self.title_font, bg=self.bg_color, fg=self.title_color)
        self.modified_label.grid(row=0, column=2, padx=5, sticky="w")
        self.modified_text = Text(self.frame, wrap="word", font=self.text_font, bg=self.text_bg_color, fg=self.text_color, undo=True, bd=2, relief="groove")
        self.modified_text.grid(row=1, column=2, padx=5, sticky="nsew")
        self.modified_scroll = Scrollbar(self.frame, command=self.on_scroll, bg=self.bg_color)
        self.modified_scroll.grid(row=1, column=3, sticky="ns")
        self.modified_text.configure(yscrollcommand=self.modified_scroll.set)

        # Button panel
        self.button_frame = tk.Frame(root, bg=self.bg_color)
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Configure button frame grid
        for i in range(8):
            self.button_frame.grid_columnconfigure(i, weight=1)

        # Button style
        button_style = {
            "font": self.button_font,
            "bg": self.button_bg_color,
            "fg": "white",
            "relief": "raised",
            "bd": 2,
            "highlightthickness": 0,
            "activebackground": "#2980b9",
            "activeforeground": "white",
            "padx": 15,
            "pady": 8,
            "borderwidth": 0,
            "highlightbackground": "#CCCCCC",
            "highlightcolor": "#CCCCCC",
            "relief": "flat",
            "borderwidth": 2,
            "relief": "groove",
            "cursor": "hand2"
        }

        # Buttons
        self.select_button = self.create_button(self.button_frame, "Select File", self.select_file, button_style)
        self.preview_button = self.create_button(self.button_frame, "Preview Changes", self.preview_changes, button_style)
        self.save_button = self.create_button(self.button_frame, "Save File", self.save_file, button_style)
        self.save_as_button = self.create_button(self.button_frame, "Save As", self.save_as, button_style)
        self.find_replace_button = self.create_button(self.button_frame, "Find and Replace", self.find_replace, button_style)
        self.process_links_button = self.create_button(self.button_frame, "Process Links", self.process_links, button_style)
        self.remove_links_button = self.create_button(self.button_frame, "Remove Links", self.remove_links, button_style)
        self.clean_file_button = self.create_button(self.button_frame, "Clean File", self.clean_file, button_style)

        self.select_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.preview_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.save_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.save_as_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.find_replace_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        self.process_links_button.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        self.remove_links_button.grid(row=0, column=6, padx=5, pady=5, sticky="ew")
        self.clean_file_button.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

    def create_button(self, parent, text, command, style):
        button = tk.Button(parent, text=text, command=command, **style)
        button.bind("<Enter>", lambda event: event.widget.config(bg=self.button_hover_bg_color))
        button.bind("<Leave>", lambda event: event.widget.config(bg=self.button_bg_color))
        return button

    def on_scroll(self, *args):
        self.original_text.yview_moveto(args[1])
        self.modified_text.yview_moveto(args[1])
        self.original_scroll.set(*args)
        self.modified_scroll.set(*args)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
        if self.file_path:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.original_content = file.read()
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(tk.END, self.original_content)

    def preview_changes(self):
        # Implement your markdown processing logic here
        self.modified_content = self.original_content  # Placeholder
        self.modified_






























        def on_scroll(self, *args):
    """Synchronizes the vertical scrolling of both text areas."""
    self.original_text.yview_moveto(args[0])
    self.modified_text.yview_moveto(args[0])
    self.original_scroll.set(*args)
    self.modified_scroll.set(*args)

#Within the init function:
#...
self.original_text.configure(yscrollcommand=self.on_scroll)
self.modified_text.configure(yscrollcommand=self.on_scroll)
#...


























import tkinter as tk
from tkinter import font, filedialog, Text, Scrollbar
import os

class MarkdownEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Asterisk Normalizer")
        self.file_path = None
        self.original_content = ""
        self.modified_content = ""

        # Color scheme
        self.bg_color = "#f0f0f0"
        self.text_bg_color = "#ffffff"
        self.button_bg_color = "#3498db"
        self.button_hover_bg_color = "#2980b9"
        self.text_color = "#333333"
        self.title_color = "#2c3e50"

        # Custom font (Congenial) - Ensure you have this font installed!
        try:
            self.base_font = font.Font(family="Congenial", size=12) #set base size.
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
        self.original_text = Text(self.frame, wrap="word", font=self.text_font, undo=True, bg=self.text_bg_color, fg=self.text_color, bd=2, relief="groove")
        self.original_text.grid(row=1, column=0, padx=5, sticky="nsew")
        self.original_scroll = Scrollbar(self.frame, command=self.on_scroll, bg=self.bg_color)
        self.original_scroll.grid(row=1, column=1, sticky="ns")
        self.original_text.configure(yscrollcommand=self.on_scroll)

        # Modified content
        self.modified_label = tk.Label(self.frame, text="Preview Changes", font=self.title_font, bg=self.bg_color, fg=self.title_color)
        self.modified_label.grid(row=0, column=2, padx=5, sticky="w")
        self.modified_text = Text(self.frame, wrap="word", font=self.text_font, bg=self.text_bg_color, fg=self.text_color, undo=True, bd=2, relief="groove")
        self.modified_text.grid(row=1, column=2, padx=5, sticky="nsew")
        self.modified_scroll = Scrollbar(self.frame, command=self.on_scroll, bg=self.bg_color)
        self.modified_scroll.grid(row=1, column=3, sticky="ns")
        self.modified_text.configure(yscrollcommand=self.on_scroll)

        # Button panel
        self.button_frame = tk.Frame(root, bg=self.bg_color)
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Configure button frame grid
        for i in range(8):
            self.button_frame.grid_columnconfigure(i, weight=1)

        # Button style
        button_style = {
            "font": self.button_font,
            "bg": self.button_bg_color,
            "fg": "white",
            "relief": "raised",
            "bd": 2,
            "highlightthickness": 0,
            "activebackground": "#2980b9",
            "activeforeground": "white",
            "padx": 15,
            "pady": 8,
            "borderwidth": 0,
            "highlightbackground": "#CCCCCC",
            "highlightcolor": "#CCCCCC",
            "relief": "flat",
            "borderwidth": 2,
            "relief": "groove",
            "cursor": "hand2"
        }

        # Buttons
        self.select_button = self.create_button(self.button_frame, "Select File", self.select_file, button_style)
        self.preview_button = self.create_button(self.button_frame, "Preview Changes", self.preview_changes, button_style)
        self.save_button = self.create_button(self.button_frame, "Save File", self.save_file, button_style)
        self.save_as_button = self.create_button(self.button_frame, "Save As", self.save_as, button_style)
        self.find_replace_button = self.create_button(self.button_frame, "Find and Replace", self.find_replace, button_style)
        self.process_links_button = self.create_button(self.button_frame, "Process Links", self.process_links, button_style)
        self.remove_links_button = self.create_button(self.button_frame, "Remove Links", self.remove_links, button_style)
        self.clean_file_button = self.create_button(self.button_frame, "Clean File", self.clean_file, button_style)

        self.select_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.preview_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.save_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.save_as_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.find_replace_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        self.process_links_button.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        self.remove_links_button.grid(row=0, column=6, padx=5, pady=5, sticky="ew")
        self.clean_file_button.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

    # ... (rest of your class methods - create_button, on_scroll, select_file, etc.) ...



















    import tkinter as tk
from tkinter import font, filedialog, Text, Scrollbar
import os

class MarkdownEditor:
    def __init__(self, root):
        # ... (rest of your init code) ...

        # Button style (Google-like)
        button_style = {
            "font": self.button_font,
            "bg": "#f8f9fa",  # Light background, similar to Google
            "fg": "#3c4043",  # Darker text color
            "relief": "flat",  # Flat appearance
            "bd": 0,  # No border
            "highlightthickness": 0,
            "padx": 20,  # Increased padding
            "pady": 10,
            "cursor": "hand2",
            "borderwidth": 0,
            "highlightbackground": "#e8eaed",
            "highlightcolor": "#e8eaed",
        }

        # ... (rest of your init code) ...

def create_button(self, parent, text, command, style):
        button = tk.Button(parent, text=text, command=command, **style)

        def on_enter(event):
            event.widget.config(bg="#e8eaed")  # Lighter hover
            event.widget.config(relief="raised") #give slight raised effect on hover.

        def on_leave(event):
            event.widget.config(bg=style["bg"])
            event.widget.config(relief="flat")#return to flat look.

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        # Add rounded corners (using canvas overlay)
        button.config(compound="center")  # Center text
        button.update()  # Ensure button size is calculated
        width = button.winfo_width()
        height = button.winfo_height()

        canvas = tk.Canvas(button, width=width, height=height, bg=style["bg"], highlightthickness=0)
        canvas.place(x=0, y=0)

        radius = min(width, height) // 2  # Adjust radius for more/less rounded corners
        canvas.create_rectangle(0, 0, width, height, fill=style["bg"], outline="")
        button.config(bg=style["bg"])
        button.config(activebackground=style["bg"])

        button.lift(canvas) #make sure the button text is above the canvas.

        return button

    # ... (rest of your class methods) ...









import tkinter as tk
from tkinter import ttk

def create_button(self, parent, text, command, style):
    button = tk.Button(parent, text=text, command=command, **style)
    def on_enter(event):
        event.widget.config(bg=self.button_hover_bg_color)
    def on_leave(event):
        target_color = "white"
        original_color = button["bg"]
        def gradual_change(step):
            if step <= 100:
                r1, g1, b1 = button.winfo_rgb(original_color)
                r2, g2, b2 = button.winfo_rgb(target_color)
                r = int(r1 + (r2 - r1) * step / 100)
                g = int(g1 + (g2 - g1) * step / 100)
                b = int(b1 + (b2 - b1) * step / 100)
                new_color = "#{:02x}{:02x}{:02x}".format(r >> 8, g >> 8, b >> 8)
                button.config(bg=new_color)
                button.after(10, lambda: gradual_change(step + 5)) 
        gradual_change(0)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    return button
















# MY BYUTTON

        def create_button(self, parent, text, command, style):
        button = tk.Button(parent, text=text, command=command, **style)
        def on_enter(event):
            event.widget.config(bg=self.button_hover_bg_color)
        def on_leave(event):
            event.widget.config(bg="white")  # Change background to white on leave
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
















----------------------CENTER------------------------------------
        import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, font, Menubutton, Menu
import re

class MarkdownEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Asterisk Normalizer")
        self.file_path = None
        self.original_content = ""
        self.modified_content = ""

        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate window dimensions and position
        window_width = screen_width // 2
        window_height = screen_height // 2
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set window geometry
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Color scheme
        self.bg_color = "#f0f0f0"
        self.text_bg_color = "#ffffff"
        self.button_bg_color = "#3498db"
        self.button_hover_bg_color = "#2980b9"
        self.text_color = "#333333"
        self.title_color = "#2c3e50"

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
        self.original_text = Text(self.frame, wrap="word", font=self.text_font, undo=True, bg=self.text_bg_color, fg=self.text_color, bd=2, relief="groove")
        self.original_text.grid(row=1, column=0, padx=5, sticky="nsew")
        self.original_scroll = Scrollbar(self.frame, command=self.on_scroll, bg=self.bg_color)
        self.original_scroll.grid(row=1, column=1, sticky="ns")
        self.original_text.configure(yscrollcommand=self.on_scroll)

        # Modified content
        self.modified_label = tk.Label(self.frame, text="Preview Changes", font=self.title_font, bg=self.bg_color, fg=self.title_color)
        self.modified_label.grid(row=0, column=2, padx=5, sticky="w")
        self.modified_text = Text(self.frame, wrap="word", font=self.text_font, bg=self.text_bg_color, fg=self.text_color, undo=True, bd=2, relief="groove")
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
            "relief": "flat",
            "bd": 0,
            "highlightthickness": 0,
            "padx": 20,
            "pady": 10,
            "cursor": "hand2",
            "borderwidth": 0,
            "highlightbackground": "#e8eaed",
            "highlightcolor": "#e8eaed",
        }

        # Dropdown menu for grouped actions
        self.actions_menu = Menubutton(self.button_frame, text="Actions", **button_style)
        self.actions_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        menu = Menu(self.actions_menu, tearoff=0)
        menu.add_command(label="Preview Changes", command=self.preview_changes)
        menu.add_command(label="Save File", command=self.save_file)
        menu.add_command(label="Save As", command=self.save_as)
        menu.add_command(label="Remove Links", command=self.remove_links)
        menu.add_command(label="Find and Replace", command=self.find_replace)
        menu.add_command(label="Process Links", command=self.process_links)

        self.actions_menu.config(menu=menu)

        # Buttons
        self.select_button = self.create_button(self.button_frame, "Select File", self.select_file, button_style)
        self.clean_file_button = self.create_button(self.button_frame, "Clean File", self.clean_file, button_style)
        self.clean_file_x2_button = self.create_button(self.button_frame, "Clean File x2", self.clean_file_x2, button_style)

        self.select_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.clean_file_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.clean_file_x2_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    def create_button(self, parent, text, command, style):
        button = tk.Button(parent, text=text, command=command, **style)

        def on_enter(event):
            button.config(bg=self.button_hover_bg_color)

        def on_leave(event):
            button.config(bg=style["bg"])

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    # ... (rest of the class remains the same)

# Create the application
root = tk.Tk()
app = MarkdownEditor(root)
root.mainloop()














-------------------------------MAXIMIZED-----------------------------------------

import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, font, Menubutton, Menu
import re

    class MarkdownEditor:
        def __init__(self, root):
            self.root = root
            self.root.title("Markdown Asterisk Normalizer")
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
            self.original_text = Text(self.frame, wrap="word", font=self.text_font, undo=True, bg=self.text_bg_color, fg=self.text_color, bd=2, relief="groove")
            self.original_text.grid(row=1, column=0, padx=5, sticky="nsew")
            self.original_scroll = Scrollbar(self.frame, command=self.on_scroll, bg=self.bg_color)
            self.original_scroll.grid(row=1, column=1, sticky="ns")
            self.original_text.configure(yscrollcommand=self.on_scroll)

            # Modified content
            self.modified_label = tk.Label(self.frame, text="Preview Changes", font=self.title_font, bg=self.bg_color, fg=self.title_color)
            self.modified_label.grid(row=0, column=2, padx=5, sticky="w")
            self.modified_text = Text(self.frame, wrap="word", font=self.text_font, bg=self.text_bg_color, fg=self.text_color, undo=True, bd=2, relief="groove")
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
                "relief": "flat",
                "bd": 0,
                "highlightthickness": 0,
                "padx": 20,
                "pady": 10,
                "cursor": "hand2",
                "borderwidth": 0,
                "highlightbackground": "#e8eaed",
                "highlightcolor": "#e8eaed",
            }

            # Dropdown menu for grouped actions
            self.actions_menu = Menubutton(self.button_frame, text="Actions", **button_style)
            self.actions_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

            menu = Menu(self.actions_menu, tearoff=0)
            menu.add_command(label="Preview Changes", command=self.preview_changes)
            menu.add_command(label="Save File", command=self.save_file)
            menu.add_command(label="Save As", command=self.save_as)
            menu.add_command(label="Remove Links", command=self.remove_links)
            menu.add_command(label="Find and Replace", command=self.find_replace)
            menu.add_command(label="Process Links", command=self.process_links)

            self.actions_menu.config(menu=menu)

            # Buttons
            self.select_button = self.create_button(self.button_frame, "Select File", self.select_file, button_style)
            self.clean_file_button = self.create_button(self.button_frame, "Clean File", self.clean_file, button_style)
            self.clean_file_x2_button = self.create_button(self.button_frame, "Clean File x2", self.clean_file_x2, button_style)

            self.select_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            self.clean_file_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
            self.clean_file_x2_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        def create_button(self, parent, text, command, style):
            button = tk.Button(parent, text=text, command=command, **style)

            def on_enter(event):
                button.config(bg=self.button_hover_bg_color)

            def on_leave(event):
                button.config(bg=style["bg"])

            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

            return button

    # ... (rest of the class remains the same)

# Create the application
root = tk.Tk()
app = MarkdownEditor(root)
root.mainloop().





















import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, font, Menubutton, Menu
import re

class MarkdownEditor:
    # ... (rest of the class remains the same)

    def find_replace(self):
        fr_window = tk.Toplevel(self.root)
        fr_window.title("Find and Replace")
        fr_window.geometry("400x300")  # Increased height for better layout

        # Frame for Find and Replace entries
        entries_frame = tk.Frame(fr_window, padx=10, pady=10)
        entries_frame.pack(fill=tk.X, expand=True)

        tk.Label(entries_frame, text="Find:", font=self.text_font).grid(row=0, column=0, sticky="w")
        tk.Label(entries_frame, text="Replace:", font=self.text_font).grid(row=1, column=0, sticky="w")

        find_entry = tk.Entry(entries_frame, width=30, font=self.text_font)
        find_entry.grid(row=0, column=1, sticky="ew")
        replace_entry = tk.Entry(entries_frame, width=30, font=self.text_font)
        replace_entry.grid(row=1, column=1, sticky="ew")

        # Checkboxes for options
        options_frame = tk.Frame(fr_window, padx=5, pady=5)
        options_frame.pack(fill=tk.X, expand=True)

        case_sensitive_var = tk.BooleanVar()
        case_sensitive_check = tk.Checkbutton(options_frame, text="Case Sensitive", variable=case_sensitive_var, font=self.text_font)
        case_sensitive_check.pack(side=tk.LEFT)

        whole_word_var = tk.BooleanVar()
        whole_word_check = tk.Checkbutton(options_frame, text="Whole Word", variable=whole_word_var, font=self.text_font)
        whole_word_check.pack(side=tk.LEFT)

        regex_var = tk.BooleanVar()
        regex_check = tk.Checkbutton(options_frame, text="Regular Expression", variable=regex_var, font=self.text_font)
        regex_check.pack(side=tk.LEFT)

        highlight_var = tk.BooleanVar()
        highlight_check = tk.Checkbutton(options_frame, text="Highlight Occurrences", variable=highlight_var, font=self.text_font)
        highlight_check.pack(side=tk.LEFT)

        # Button frame
        button_frame = tk.Frame(fr_window, padx=10, pady=10)
        button_frame.pack(fill=tk.X, expand=True)

        def find_action():
            find_text = find_entry.get()
            case_sensitive = case_sensitive_var.get()
            whole_word = whole_word_var.get()
            regex = regex_var.get()
            highlight = highlight_var.get()

            if not self.modified_content:
                self.modified_content = self.original_content

            flags = 0
            if not case_sensitive:
                flags |= re.IGNORECASE

            if regex:
                if whole_word:
                    find_text = r"\b" + find_text + r"\b"
                matches = list(re.finditer(find_text, self.modified_content, flags=flags))
            else:
                if whole_word:
                    find_text = r"\b" + re.escape(find_text) + r"\b"
                    matches = list(re.finditer(find_text, self.modified_content, flags=flags))
                else:
                    matches = [m for m in re.finditer(re.escape(find_text), self.modified_content, flags=flags)]

            if highlight:
                self.modified_text.tag_remove("highlight", "1.0", tk.END)
                for match in matches:
                    start = f"1.0+{match.start()}c"
                    end = f"1.0+{match.end()}c"
                    self.modified_text.tag_add("highlight", start, end)
                self.modified_text.tag_configure("highlight", background="yellow", foreground="black")

        def replace_action():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            case_sensitive = case_sensitive_var.get()
            whole_word = whole_word_var.get()
            regex = regex_var.get()

            if not self.modified_content:
                self.modified_content = self.original_content

            flags = 0
            if not case_sensitive:
                flags |= re.IGNORECASE

            if regex:
                if whole_word:
                    find_text = r"\b" + find_text + r"\b"
                self.modified_content = re.sub(find_text, replace_text, self.modified_content, flags=flags)

            else:
                if whole_word:
                    find_text = r"\b" + re.escape(find_text) + r"\b"
                    self.modified_content = re.sub(find_text, re.escape(replace_text), self.modified_content, flags=flags)
                else:
                    self.modified_content = self.modified_content.replace(find_text, replace_text)

            self.modified_text.delete(1.0, tk.END)
            self.modified_text.insert(tk.END, self.modified_content)

        find_button = tk.Button(button_frame, text="Find", command=find_action, font=self.button_font)
        find_button.pack(side=tk.LEFT)

        replace_button = tk.Button(button_frame, text="Replace", command=replace_action, font=self.button_font)
        replace_button.pack(side=tk.RIGHT)

        # Configure grid column weights for resizing
        entries_frame.columnconfigure(1, weight=1)

    # ... (rest of the class remains the same)

# Create the application
root = tk.Tk()
app = MarkdownEditor(root)
root.mainloop()