from tkinter import Tk
from config import setup_folders
from app_ui import AppUI

# Run the Tkinter app
setup_folders()  # Set up folders on startup
root = Tk()
app = AppUI(root)
root.mainloop()
