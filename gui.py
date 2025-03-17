import tkinter as tk
from tkinter import filedialog
import re
import initializer

def create_button(parent, text, command, style, button_hover_bg_color):
    
    button = tk.Button(parent, text=text, command=command, **style)

    def on_enter(event):
        event.widget.config(bg=button_hover_bg_color)

    def on_leave(event):
        global dark_mode
        if initializer.dark_mode:
            target_color = "#4a4a4a"
        else:
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

def on_scroll(original_text, modified_text, original_scroll, modified_scroll, *args):
    """Synchronizes the vertical scrolling of both text areas."""
    original_text.yview_moveto(args[0])
    modified_text.yview_moveto(args[0])
    original_scroll.set(*args)
    modified_scroll.set(*args)

def select_file(original_text, modified_text, status_bar):
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
        original_text.delete(1.0, tk.END)
        modified_text.delete(1.0, tk.END)
        original_text.insert(tk.END, original_content)
        modified_text.insert(tk.END, "Please preview the changes to see highlights.")
        status_bar.config(text=f"Loaded file: {file_path}")
        return file_path, original_content
    return None, None

def save_file(file_path, modified_content, modified_text, status_bar):
    if not modified_content:
        modified_text.delete(1.0, tk.END)
        modified_text.insert(tk.END, "No changes to save. Please preview changes first.")
        return
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)
    modified_text.delete(1.0, tk.END)
    modified_text.insert(tk.END, f"File saved successfully at: {file_path}")
    status_bar.config(text=f"Saved file: {file_path}")

def save_as(modified_content, modified_text, status_bar):
    if not modified_content:
        modified_text.delete(1.0, tk.END)
        modified_text.insert(tk.END, "No changes to save. Please preview changes first.")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
    if save_path:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        modified_text.delete(1.0, tk.END)
        modified_text.insert(tk.END, f"File saved successfully at: {save_path}")
        status_bar.config(text=f"Saved file as: {save_path}")

def update_original_content(file_path, original_text, modified_text):
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
        original_text.delete(1.0, tk.END)
        modified_text.delete(1.0, tk.END)
        original_text.insert(tk.END, original_content)
        return original_content
    return None
