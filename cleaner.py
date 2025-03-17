import re
import tkinter as tk
from tkinter import *

def clean_file_x2(editor):
    if not editor.original_content:
        editor.modified_text.delete(1.0, tk.END)
        editor.modified_text.insert(tk.END, "Please select a file first.")
        return
    editor.modified_content = clean_content(editor.original_content)
    editor.save_file()
    editor.modified_text.delete(1.0, tk.END)
    editor.modified_text.insert(tk.END, editor.modified_content)

def clean_content(content):
    content = _clean_once(content)
    content = _clean_once(content)
    return _clean_once(content)

def _clean_once(content):
    content = re.sub(r'\*{3,}', '**', content)
    content = re.sub(r'\*\*([^\*]{0,2})\*\*', r'\1', content)
    content = re.sub(r'^(#{1,6} .*?)\*\*(.*?)\*\*', r'\1\2', content, flags=re.MULTILINE)
    content = re.sub(r'^(#{1,6})[^#\s]+(.*?)$', r'\1 \2', content, flags=re.MULTILINE)
    content = re.sub(r'\[\[\*\*(.*?)\*\*\]\]', r'[[\1]]', content)
    content = re.sub(r'\[\^.*?\]', ' ', content)
    lines = content.splitlines()
    processed_lines = []
    stop_processing = False
    for line in lines:
        if stop_processing:
            break
        if line.strip().lower() == "## see also" or line.strip().lower().startswith("follow us"):
            stop_processing = True
            continue
        line = re.sub(r'^(\d+)\.\s*###\s*(.*)', r'### \1. \2', line)
        line = re.sub(r'\"\>page\&nbsp;needed\<\/span\>\]\]\<\/i\>\&\#93\;\<\/sup\>\-.*?\)', ' ', line)
        line = re.sub(r'\[\[edit\]\(.*?\)\]', '---', line)
        line = re.sub(r'\[!\[.*?\]\((.*?)\)\]\(.*?\)', r'![](\1)', line)
        line = re.sub(r'\[\[.*?\]\]\(.*?\)', ' ', line)
        line = re.sub(r'(?<!\!)\[([^\]]+)\]\([^\)]+\)', r'[[\1]]', line)
        processed_lines.append(line)
    content = '\n'.join(processed_lines)
    return re.sub(r'\[\[(.*?)\]\]', r'\1', content)