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
        menu.add_command(label="Preview Changes", command=self.preview_changes, font=self.text_font)
        menu.add_command(label="Save File", command=self.save_file, font=self.text_font)
        menu.add_command(label="Save As", command=self.save_as, font=self.text_font)
        menu.add_command(label="Remove Links", command=self.remove_links, font=self.text_font)
        menu.add_command(label="Find and Replace", command=self.find_replace, font=self.text_font)
        menu.add_command(label="Process Links", command=self.process_links, font=self.text_font)

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

    def on_scroll(self, *args):
        """Synchronizes the vertical scrolling of both text areas."""
        self.original_text.yview_moveto(args[0])
        self.modified_text.yview_moveto(args[0])
        self.original_scroll.set(*args)
        self.modified_scroll.set(*args)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
        if self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.original_content = file.read()
            self.original_text.delete(1.0, tk.END)
            self.modified_text.delete(1.0, tk.END)
            self.original_text.insert(tk.END, self.original_content)
            self.modified_text.insert(tk.END, "Please preview the changes to see highlights.")

    def preview_changes(self):
        if not self.original_content:
            self.modified_text.delete(1.0, tk.END)
            self.modified_text.insert(tk.END, "Please select a file first.")
            return

        self.modified_content = self.clean_content(self.original_content)
        self.highlight_changes()

    def save_file(self):
        if not self.modified_content:
            self.modified_text.delete(1.0, tk.END)
            self.modified_text.insert(tk.END, "No changes to save. Please preview changes first.")
            return

        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(self.modified_content)

        self.modified_text.delete(1.0, tk.END)
        self.modified_text.insert(tk.END, f"File saved successfully at: {self.file_path}")
        self.update_original_content()

    def save_as(self):
        if not self.modified_content:
            self.modified_text.delete(1.0, tk.END)
            self.modified_text.insert(tk.END, "No changes to save. Please preview changes first.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(self.modified_content)
            self.modified_text.delete(1.0, tk.END)
            self.modified_text.insert(tk.END, f"File saved successfully at: {save_path}")

    def process_links(self):
        if not self.original_content:
            self.modified_text.delete(1.0, tk.END)
            self.modified_text.insert(tk.END, "Please select a file first.")
            return
        self.modified_content = self.process_content_links(self.original_content)
        self.modified_text.delete(1.0, tk.END)
        self.modified_text.insert(tk.END, self.modified_content)

    def remove_links(self):
        if not self.original_content:
            self.modified_text.delete(1.0, tk.END)
            self.modified_text.insert(tk.END, "Please select a file first.")
            return
        self.modified_content = re.sub(r'\[\[(.*?)\]\]', r'\1', self.original_content)
        self.modified_text.delete(1.0, tk.END)
        self.modified_text.insert(tk.END, self.modified_content)

    def clean_file(self):
        if not self.original_content:
            self.modified_text.delete(1.0, tk.END)
            self.modified_text.insert(tk.END, "Please select a file first.")
            return
        self.modified_content = self.clean_content(self.original_content)
        self.modified_text.delete(1.0, tk.END)
        self.modified_text.insert(tk.END, self.modified_content)

    def clean_file_x2(self):
        if not self.original_content:
            self.modified_text.delete(1.0, tk.END)
            self.modified_text.insert(tk.END, "Please select a file first.")
            return
        # Clean the file twice
        self.modified_content = self.clean_content(self.original_content)
        self.modified_content = self.clean_content(self.modified_content)
        # Save the changes
        self.save_file()
        # Update the modified text area
        self.modified_text.delete(1.0, tk.END)
        self.modified_text.insert(tk.END, self.modified_content)

    def find_replace(self):
        fr_window = tk.Toplevel(self.root)
        fr_window.title("Find and Replace")
        fr_window.geometry("500x150")  # Increased height for better layout
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
        case_sensitive_check = tk.Checkbutton(options_frame, text="Match Case", variable=case_sensitive_var, font=self.text_font)
        case_sensitive_check.pack(side=tk.LEFT)

        whole_word_var = tk.BooleanVar()
        whole_word_check = tk.Checkbutton(options_frame, text="Word", variable=whole_word_var, font=self.text_font)
        whole_word_check.pack(side=tk.LEFT)

        regex_var = tk.BooleanVar()
        regex_check = tk.Checkbutton(options_frame, text="RE", variable=regex_var, font=self.text_font)
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

    def clean_content(self, content):
        content = re.sub(r'\*{3,}', '**', content)
        content = re.sub(r'\*\*([^\*]{0,2})\*\*', r'\1', content)
        content = re.sub(r'^(#{1,6} .*?)\*\*(.*?)\*\*', r'\1\2', content, flags=re.MULTILINE)
        content = re.sub(r'^(#{1,6})[^#\s]+(.*?)$', r'\1 \2', content, flags=re.MULTILINE)
        content = re.sub(r'\[\[\*\*(.*?)\*\*\]\]', r'[[\1]]', content)
        # Remove footnotes
        content = re.sub(r'\[\^.*?\]', ' ', content)
        lines = content.splitlines()
        processed_lines = []
        stop_processing = False
        for line in lines:
            if line.strip().lower() == "## see also" or line.strip().lower().startswith("follow us"):
                stop_processing = True
            if stop_processing:
                break
            line = re.sub(r'^(\d+)\.\s*###\s*(.*)', r'### \1. \2', line)
            line = re.sub(r'\"\>page\&nbsp;needed\<\/span\>\]\]\<\/i\>\&\#93\;\<\/sup\>\-.*?\)', ' ', line)
            line = re.sub(r'\[\[edit\]\(.*?\)\]', '---', line)
            line = re.sub(r'\[!\[.*?\]\((.*?)\)\]\(.*?\)', r'![](\1)', line)
            line = re.sub(r'\[\[.*?\]\]\(.*?\)', ' ', line)
            line = re.sub(r'(?<!\!)\[([^\]]+)\]\([^\)]+\)', r'[[\1]]', line)
            processed_lines.append(line)
        content = '\n'.join(processed_lines)
        content = re.sub(r'\[\[(.*?)\]\]', r'\1', content)
        return content

    def process_content_links(self, content):
        lines = content.splitlines()
        processed_lines = []
        stop_processing = False
        for line in lines:
            if line.strip().lower() == "## see also" or line.strip().lower().startswith("follow us"):
                stop_processing = True
            if stop_processing:
                break
            line = re.sub(r'^(\d+)\.\s*###\s*(.*)', r'### \1. \2', line)
            line = re.sub(r'\"\>page\&nbsp;needed\<\/span\>\]\]\<\/i\>\&\#93\;\<\/sup\>\-.*?\)', ' ', line)
            line = re.sub(r'\[\[edit\]\(.*?\)\]', '---', line)
            line = re.sub(r'\[!\[.*?\]\((.*?)\)\]\(.*?\)', r'![](\1)', line)
            line = re.sub(r'\[\[.*?\]\]\(.*?\)', ' ', line)
            line = re.sub(r'(?<!\!)\[([^\]]+)\]\([^\)]+\)', r'[[\1]]', line)
            processed_lines.append(line)
        return '\n'.join(processed_lines)

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

    def update_original_content(self):
        if self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.original_content = file.read()
            self.original_text.delete(1.0, tk.END)
            self.modified_text.delete(1.0, tk.END)
            self.original_text.insert(tk.END, self.original_content)

# Create the application
root = tk.Tk()
app = MarkdownEditor(root)
root.mainloop()
