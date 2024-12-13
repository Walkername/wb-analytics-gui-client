import tkinter as tk
from tkinter import ttk, messagebox

from config.config import APP_CONFIG, MONGO_CONFIG
from views.main_view import MainWindow

def on_exit(root):
    """Handle application exit."""
    if messagebox.askokcancel("Quit", "Do you really want to exit?"):
        root.destroy()

def main():
    """Main function to start the application."""
    # Initialize the main Tkinter root window
    root = tk.Tk()
    root.title(APP_CONFIG["app_name"])
    root.geometry("800x500")  # Default window size

    # Add a clean exit handler
    root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root))

    app = MainWindow(root)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
