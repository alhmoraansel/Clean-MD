import tkinter as tk
import re

class FindReplaceWindow:
    def __init__(self, parent, text_widget, text_font, button_font, original_content, modified_content):
        self.parent = parent
        self.text_widget = text_widget
        self.text_font = text_font
        self.button_font = button_font
        self.original_content = original_content
        self.modified_content = modified_content

        self.fr_window = tk.Toplevel(self.parent)
        self.fr_window.title("Find and Replace")
        self.fr_window.geometry("500x150")

        # Frame for Find and Replace entries
        entries_frame = tk.Frame(self.fr_window, padx=10, pady=10)
        entries_frame.pack(fill=tk.X, expand=True)
        tk.Label(entries_frame, text="Find:", font=self.text_font).grid(row=0, column=0, sticky="w")
        tk.Label(entries_frame, text="Replace:", font=self.text_font).grid(row=1, column=0, sticky="w")
        self.find_entry = tk.Entry(entries_frame, width=30, font=self.text_font)
        self.find_entry.grid(row=0, column=1, sticky="ew")
        self.replace_entry = tk.Entry(entries_frame, width=30, font=self.text_font)
        self.replace_entry.grid(row=1, column=1, sticky="ew")

        # Checkboxes for options
        options_frame = tk.Frame(self.fr_window, padx=5, pady=5)
        options_frame.pack(fill=tk.X, expand=True)
        self.case_sensitive_var = tk.BooleanVar()
        case_sensitive_check = tk.Checkbutton(options_frame, text="Match Case", variable=self.case_sensitive_var, font=self.text_font)
        case_sensitive_check.pack(side=tk.LEFT)
        self.whole_word_var = tk.BooleanVar()
        whole_word_check = tk.Checkbutton(options_frame, text="Word", variable=self.whole_word_var, font=self.text_font)
        whole_word_check.pack(side=tk.LEFT)
        self.regex_var = tk.BooleanVar()
        regex_check = tk.Checkbutton(options_frame, text="RE", variable=self.regex_var, font=self.text_font)
        regex_check.pack(side=tk.LEFT)
        self.highlight_var = tk.BooleanVar()
        highlight_check = tk.Checkbutton(options_frame, text="Highlight Occurrences", variable=self.highlight_var, font=self.text_font)
        highlight_check.pack(side=tk.LEFT)

        # Button frame
        button_frame = tk.Frame(self.fr_window, padx=10, pady=10)
        button_frame.pack(fill=tk.X, expand=True)
        find_button = tk.Button(button_frame, text="Find", command=self.find_action, font=self.button_font)
        find_button.pack(side=tk.LEFT)
        replace_button = tk.Button(button_frame, text="Replace", command=self.replace_action, font=self.button_font)
        replace_button.pack(side=tk.RIGHT)

        # Configure grid column weights for resizing
        entries_frame.columnconfigure(1, weight=1)

    def find_action(self):
        find_text = self.find_entry.get()
        case_sensitive = self.case_sensitive_var.get()
        whole_word = self.whole_word_var.get()
        regex = self.regex_var.get()
        highlight = self.highlight_var.get()
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
            self.text_widget.tag_remove("highlight", "1.0", tk.END)
            for match in matches:
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_widget.tag_add("highlight", start, end)
            self.text_widget.tag_configure("highlight", background="yellow", foreground="black")

    def replace_action(self):
        find_text = self.find_entry.get()
        replace_text = self.replace_entry.get()
        case_sensitive = self.case_sensitive_var.get()
        whole_word = self.whole_word_var.get()
        regex = self.regex_var.get()
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
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, self.modified_content)
        