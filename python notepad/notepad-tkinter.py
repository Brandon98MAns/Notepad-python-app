import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

class NotaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Notepad")  # Set the title of the application

        # Configure Open Sans font for the Text widget
        self.text_font = ("Helvetica", 10)  # Adjust according to your preferences

        # Add padding around the text box
        self.text = tk.Text(master, wrap="word", font=self.text_font, padx=10, pady=10)
        self.text.pack(expand=True, fill="both")  # Pack the Text widget

        self.modified = False  # Variable to track modifications

        # Menu bar
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        # File menu
        menu_file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="New", command=self.new_note)
        menu_file.add_command(label="Open", command=self.open_note)
        menu_file.add_command(label="Save", command=self.save_note)
        menu_file.add_command(label="Save As", command=self.save_as_note)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.exit_app)

        # Associate the exit function with the window close button
        master.protocol("WM_DELETE_WINDOW", self.exit_app)

        # Associate the save function with the keyboard shortcut (Ctrl + S)
        master.bind("<Control-s>", self.save_shortcut)

        # Update the window title based on modifications
        master.title("Notepad" + (" *" if self.modified else ""))

        # Associate a function to track changes in the text
        self.text.bind("<Key>", self.text_modified)

    def new_note(self):
        self.text.delete("1.0", tk.END)  # Delete existing text
        self.modified = False
        self.update_title()

    def open_note(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            self.modified = False
            self.update_title()

    def save_note(self):
        if hasattr(self, "current_file"):
            with open(self.current_file, "w", encoding="utf-8") as file:
                content = self.text.get("1.0", tk.END)
                file.write(content)
            self.modified = False
            self.update_title()
        else:
            self.save_as_note()

    def save_as_note(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                content = self.text.get("1.0", tk.END)
                file.write(content)
            self.current_file = file_path
            self.modified = False
            self.update_title()

    def exit_app(self):
        if self.modified:
            confirmation = messagebox.askyesnocancel("Exit", "Do you want to save changes before exiting?")
            if confirmation is not None:
                if confirmation:
                    self.save_note()
                self.master.destroy()
        else:
            self.master.destroy()

    def save_shortcut(self, event):
        # Keyboard shortcut for saving (Ctrl + S)
        self.save_note()

    def text_modified(self, event):
        self.modified = True
        self.update_title()

    def update_title(self):
        # Update the window title based on modifications
        self.master.title("Notepad" + (" *" if self.modified else ""))

if __name__ == "__main__":
    root = tk.Tk()

    app = NotaApp(root)
    root.mainloop()






