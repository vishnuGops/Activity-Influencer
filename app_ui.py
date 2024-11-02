import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import logging
import threading
import os
from config import LOG_FILE, LOGIN_FILE, VERSION, DEFAULT_HOUR, DEFAULT_MINUTE
from github_activity import GithubActivityInfluencer


class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Activity Influencer")
        self.activity_thread = None
        self._setup_logging()
        self._create_widgets()
        self.log_message(f"Started Github Activity Influencer {VERSION}")
        self._load_login_state()

    def _setup_logging(self):
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def log_message(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def _create_widgets(self):
        tk.Label(self.root, text="API Key:").grid(row=0, column=0)
        self.api_key_entry = tk.Entry(self.root, width=40)
        self.api_key_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Repo Owner:").grid(row=1, column=0)
        self.repo_owner_entry = tk.Entry(self.root, width=30)
        self.repo_owner_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Repo Name:").grid(row=2, column=0)
        self.repo_name_entry = tk.Entry(self.root, width=30)
        self.repo_name_entry.grid(row=2, column=1)

        tk.Label(self.root, text="File Name:").grid(row=3, column=0)
        self.file_name_entry = tk.Entry(self.root, width=30)
        self.file_name_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Target Hour:").grid(row=4, column=0)
        self.hour_entry = ttk.Combobox(
            self.root, values=list(range(24)), width=5)
        self.hour_entry.set(DEFAULT_HOUR)
        self.hour_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Target Minute:").grid(row=5, column=0)
        self.minute_entry = ttk.Combobox(
            self.root, values=list(range(60)), width=5)
        self.minute_entry.set(DEFAULT_MINUTE)
        self.minute_entry.grid(row=5, column=1)

        self.start_button = tk.Button(
            self.root, text="Start", command=self.start_activity)
        self.start_button.grid(row=6, columnspan=2)

        self.log_text = scrolledtext.ScrolledText(
            self.root, width=60, height=20)
        self.log_text.grid(row=7, columnspan=2)

    def _load_login_state(self):
        if os.path.exists(LOGIN_FILE):
            self.log_message(f"Login file exists -------> Logging in user.")
            with open(LOGIN_FILE, 'r') as file:
                lines = file.readlines()
                if lines:
                    self.api_key_entry.insert(0, lines[0].strip())
                    self.repo_owner_entry.insert(0, lines[1].strip())
                    self.repo_name_entry.insert(0, lines[2].strip())
                    self.file_name_entry.insert(0, lines[3].strip())

    def _save_login_state(self):
        with open(LOGIN_FILE, 'w') as file:
            file.write(f"{self.api_key_entry.get()}\n")
            file.write(f"{self.repo_owner_entry.get()}\n")
            file.write(f"{self.repo_name_entry.get()}\n")
            file.write(f"{self.file_name_entry.get()}\n")
            self.log_message(
                f"Saving login info -------> {self.repo_owner_entry} | {self.repo_name_entry} ")

    def start_activity(self):
        api_key = self.api_key_entry.get()
        if not api_key:
            messagebox.showerror("Error", "Invalid API key.")
            return

        repo_owner = self.repo_owner_entry.get()
        repo_name = self.repo_name_entry.get()
        file_name = self.file_name_entry.get()
        target_hour = int(self.hour_entry.get())
        target_minute = int(self.minute_entry.get())

        # Pass `self` (AppUI instance) to `GithubActivityInfluencer`
        influencer = GithubActivityInfluencer(
            api_key, repo_owner, repo_name, file_name, target_hour, target_minute, self)
        self._save_login_state()
        self.activity_thread = threading.Thread(
            target=influencer.start_activity)
        self.activity_thread.daemon = True
        self.activity_thread.start()
