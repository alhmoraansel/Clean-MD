import tkinter as tk
from tkinter import Menu

def markdown_editor_init(self, *args, **kwargs):
    super(MarkdownEditor, self).__init__(*args, **kwargs)

    # Creating the menu bar
    self.menu_bar = Menu(self)
    self.config(menu=self.menu_bar)

    # Adding the "Actions" menu
    self.actions_menu = Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="Actions", menu=self.actions_menu)

    # Adding commands to the "Actions" menu
    self.actions_menu.add_command(label="Clean File", command=self.clean_file)
    self.actions_menu.add_command(label="Save As", command=self.save_as)
    self.actions_menu.add_command(label="Remove Links", command=self.remove_links)
    self.actions_menu.add_command(label="Find and Replace", command=self.find_replace)
    self.actions_menu.add_command(label="Process Links", command=self.process_links)

    print("Menu bar created successfully")
