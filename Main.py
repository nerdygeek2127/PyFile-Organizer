import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, simpledialog, Menu
from datetime import datetime
import subprocess
import json

# File for saving persistent data
DATA_FILE = "file_data.json"
NOTEPAD_PLUS_PATH = r"C:\Program Files\Notepad++\notepad++.exe"  # Path to Notepad++ executable

class PythonFileListerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python File Lister")
        self.root.geometry("700x500")
        
        self.bookmarked_folders = {}
        self.file_tags = {}
        self.last_opened_folder = None
        
        # Load saved data (bookmarks, tags, last opened folder)
        self.load_data()

        # Control frame for search, bookmark, and tag buttons
        self.control_frame = ttk.Labelframe(self.root, text="Python File Lister", padding=(10, 10))
        self.control_frame.pack(pady=10, padx=10, fill=ttk.X)

        self.search_button = ttk.Button(self.control_frame, text="Search Folder", command=self.search_folder, bootstyle=PRIMARY)
        self.search_button.pack(side=ttk.LEFT, padx=5)

        self.bookmark_button = ttk.Button(self.control_frame, text="Bookmark Folder", command=self.bookmark_folder, bootstyle=SUCCESS)
        self.bookmark_button.pack(side=ttk.LEFT, padx=5)

        self.tag_button = ttk.Button(self.control_frame, text="Tag", command=self.add_tag, bootstyle=INFO)
        self.tag_button.pack(side=ttk.LEFT, padx=5)

        # Frame for the table
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(pady=10, padx=10, fill=ttk.BOTH, expand=True)

        # Configure a custom style for Treeview to increase row padding
        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=30)  # Increase row height for more spacing between rows

        # Configure scrollbar style
        style.configure(
            "Custom.Vertical.TScrollbar",
            gripcount=0,
            background=style.colors.primary,
            darkcolor=style.colors.primary,
            troughcolor=style.colors.light,
            bordercolor=style.colors.primary,
            arrowsize=15,
            relief="flat",
            borderwidth=1
        )

        # Treeview for file list
        self.file_tree = ttk.Treeview(self.table_frame, columns=("Name", "Last Modified", "Tag"), show="headings", bootstyle=SECONDARY, style="Custom.Treeview")
        self.file_tree.heading("Name", text="Name", command=lambda: self.sort_by_column("Name"))
        self.file_tree.heading("Last Modified", text="Last Modified", command=lambda: self.sort_by_column("Last Modified"))
        self.file_tree.heading("Tag", text="Tag")
        self.file_tree.column("Name", width=200)
        self.file_tree.column("Last Modified", width=150)
        self.file_tree.column("Tag", width=100, anchor="center")
        self.file_tree.pack(fill=ttk.BOTH, expand=True)

        # Scrollbar for Treeview (Vertical Only) with custom style
        self.scrollbar = ttk.Scrollbar(self.file_tree, orient="vertical", command=self.file_tree.yview, style="Custom.Vertical.TScrollbar")
        self.file_tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=ttk.RIGHT, fill=ttk.Y)

        # Bookmark label frame
        self.bookmark_frame = ttk.Labelframe(self.root, text="Bookmarks", padding=(10, 10))
        self.bookmark_frame.pack(pady=10, padx=10, fill=ttk.X)

        self.bookmark_container = ttk.Frame(self.bookmark_frame)
        self.bookmark_container.pack(fill=ttk.X, pady=5)

        # Bind events for double-click and right-click menu
        self.file_tree.bind("<Double-1>", self.run_python_file)
        self.file_tree.bind("<Button-3>", self.show_context_menu)

        # Load last opened folder on startup
        if self.last_opened_folder:
            self.list_python_files(self.last_opened_folder)

        # Display saved bookmarks
        self.update_bookmarks()

    def search_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.last_opened_folder = folder_path
            self.list_python_files(folder_path)
            self.save_data()

    def list_python_files(self, folder_path):
        # Clear the previous file list
        self.file_tree.delete(*self.file_tree.get_children())

        # Find and display Python files
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    modification_time = os.path.getmtime(file_path)
                    formatted_time = datetime.fromtimestamp(modification_time).strftime("%Y-%m-%d %H:%M:%S")
                    file_list.append((file, formatted_time, self.file_tags.get(file, "No Tag"), file_path))

        # Sort the file list by modification time
        file_list.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S"), reverse=True)

        # Insert sorted files into the Treeview
        for file, mod_time, tag, file_path in file_list:
            tag_color = "blue" if tag != "No Tag" else "black"
            self.file_tree.insert("", "end", values=(file, mod_time, tag), tags=(file_path,))
            if tag != "No Tag":
                self.file_tree.tag_configure(file_path, foreground=tag_color)

    def add_tag(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            file_name = self.file_tree.item(selected_item, "values")[0]
            tag_name = simpledialog.askstring("Input", f"Enter a tag for {file_name}:")
            if tag_name:
                self.file_tags[file_name] = tag_name
                # Update tag in Treeview
                self.file_tree.item(selected_item, values=(file_name, self.file_tree.item(selected_item, "values")[1], tag_name))
                # Change tag color to blue if a tag is applied
                file_path = self.file_tree.item(selected_item, "tags")[0]
                self.file_tree.tag_configure(file_path, foreground="blue")
                self.save_data()

    def run_python_file(self, event=None):
        selected_item = self.file_tree.selection()
        if selected_item:
            file_path = self.file_tree.item(selected_item)["tags"][0]
            try:
                subprocess.Popen(['python', file_path], shell=True)
                messagebox.showinfo("Success", f"Running {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not run {file_path}: {str(e)}")

    def show_context_menu(self, event):
        selected_item = self.file_tree.selection()
        if selected_item:
            # Create a popup menu
            menu = Menu(self.root, tearoff=0)
            menu.add_command(label="Edit", command=self.edit_file_in_notepad)
            menu.post(event.x_root, event.y_root)

    def edit_file_in_notepad(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            file_path = self.file_tree.item(selected_item)["tags"][0]
            try:
                subprocess.Popen([NOTEPAD_PLUS_PATH, file_path])  # Open file in Notepad++
            except FileNotFoundError:
                messagebox.showerror("Error", f"Notepad++ not found at {NOTEPAD_PLUS_PATH}")

    def sort_by_column(self, column):
        # Get all the data from the treeview
        data = [(self.file_tree.set(child, column), child) for child in self.file_tree.get_children('')]

        # Sort the data by the selected column
        data.sort(reverse=True if column == "Last Modified" else False)

        # Rearrange the items in sorted positions
        for index, (val, item) in enumerate(data):
            self.file_tree.move(item, '', index)

    def bookmark_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_name = os.path.basename(folder_path)
            self.bookmarked_folders[folder_name] = folder_path
            self.update_bookmarks()
            self.save_data()

    def update_bookmarks(self):
        # Clear previous bookmarks
        for widget in self.bookmark_container.winfo_children():
            widget.destroy()

        if self.bookmarked_folders:
            bookmark_buttons = []
            for folder_name, folder_path in self.bookmarked_folders.items():
                bookmark_button = ttk.Button(self.bookmark_container, text=folder_name, cursor="hand2", bootstyle="outline-primary")
                bookmark_button.bind("<Button-1>", lambda e, path=folder_path: self.list_python_files(path))
                bookmark_button.bind("<Button-3>", lambda e, path=folder_name: self.show_bookmark_context_menu(e, folder_name))
                bookmark_buttons.append(bookmark_button)

            # Place bookmark buttons in a row
            for button in             bookmark_buttons:
                button.pack(side=ttk.LEFT, padx=5)
        else:
            no_bookmark_label = ttk.Label(self.bookmark_container, text="No bookmarks yet", anchor="w")
            no_bookmark_label.pack(fill=ttk.X)

    def show_bookmark_context_menu(self, event, folder_name):
        # Create a popup menu for bookmarks
        menu = Menu(self.root, tearoff=0)
        menu.add_command(label="Delete", command=lambda: self.delete_bookmark(folder_name))
        menu.post(event.x_root, event.y_root)

    def delete_bookmark(self, folder_name):
        if folder_name in self.bookmarked_folders:
            del self.bookmarked_folders[folder_name]
            self.update_bookmarks()
            self.save_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.bookmarked_folders = data.get("bookmarked_folders", {})
                self.file_tags = data.get("file_tags", {})
                self.last_opened_folder = data.get("last_opened_folder", None)

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            data = {
                "bookmarked_folders": self.bookmarked_folders,
                "file_tags": self.file_tags,
                "last_opened_folder": self.last_opened_folder
            }
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    app = ttk.Window(themename="superhero")  # You can choose any theme from ttkbootstrap (darkly, journal, etc.)
    app.title("Python File Lister")
    PythonFileListerApp(app)
    app.mainloop()

