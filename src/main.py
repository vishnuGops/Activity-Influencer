from tkinter import Tk
from config import setup_folders
from app_ui import AppUI

import os
import sys

# Check if running in a headless environment (like GitHub Actions)
if os.environ.get('GITHUB_ACTIONS'):
    # Skip the GUI for CI/CD environment
    print("Running in headless mode. Skipping GUI...")
    sys.exit(0)  # Exit or provide alternative execution logic
else:
    # Run the Tkinter app
    setup_folders()  # Set up folders on startup
    root = Tk()
    app = AppUI(root)
    root.mainloop()
