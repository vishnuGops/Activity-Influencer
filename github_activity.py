import logging
import random
import time
from datetime import datetime, timedelta
import pytz
import gc
from github import Github
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

# Constants
LOG_FILE = '../activity_log.txt'
VERSION = 1.9
DEFAULT_HOUR = 23
DEFAULT_MINUTE = 30


class GithubActivityInfluencer:
    def __init__(self, api_key, repo_owner, repo_name, file_name, target_hour, target_minute):
        self.api_key = api_key
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.file_name = file_name
        self.target_hour = target_hour
        self.target_minute = target_minute
        self.github = Github(api_key)
        self.repo = self.github.get_user(repo_owner).get_repo(repo_name)

    def log_message(self, msg):
        logging.info(msg)
        print(msg)
        app.log_message(msg)  # Update the UI log display

    def check_and_generate_commits(self):
        """Checks the last commit date and generates new commits if none were made today."""
        try:
            commits = self.repo.get_commits()
            if not commits:
                self.log_message('--> No commits found in the repository.')
                return

            last_commit = commits[0]
            last_commit_date = last_commit.commit.author.date.astimezone(
                pytz.timezone('America/Los_Angeles')).date()
            today = datetime.now().date()

            if last_commit_date != today:
                self._generate_commits(today)
            else:
                self.log_message(
                    '--> Last commit was made today. No new commits needed.')
        except Exception as e:
            self.log_message(f"Error checking commits: {e}")

    def _generate_commits(self, today):
        """Generates a specified number of random commits."""
        num_commits = random.randint(1, 16)
        self.log_message(f'--> No commits today. Generating {num_commits}...')

        for i in range(num_commits):
            commit_message = f'Commit {i + 1} - {today}'
            new_content = f'Commit {i + 1} on {today}'
            contents = self.repo.get_contents(self.file_name, ref='main')
            self.repo.update_file(
                contents.path, commit_message, new_content, contents.sha, branch='main')
            self.log_message(f'--> Committed change {i + 1} on {today}')

    def start_activity(self):
        """Runs the commit check and generation loop based on the specified target time."""
        while True:
            today = datetime.now()
            self.log_message(f'** Checking commits on {today} **')

            if today.hour == self.target_hour and today.minute == self.target_minute:
                self.log_message(
                    f'--> Checking commits at target time: {today}')
                self.check_and_generate_commits()

            # Calculate and wait until the next check
            wait_time = self._time_until_target(today)
            self.log_message(f'--> Waiting {wait_time} seconds...')
            time.sleep(wait_time)
            gc.collect()  # Perform garbage collection

    def _time_until_target(self, current_time):
        """Calculates the seconds remaining until the target hour and minute."""
        target_time = datetime.combine(current_time, datetime.min.time()) + timedelta(
            hours=self.target_hour, minutes=self.target_minute
        )
        if target_time < current_time:
            target_time += timedelta(days=1)
        return (target_time - current_time).total_seconds()


class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Activity Influencer")
        self.activity_thread = None
        self._setup_logging()
        self._create_widgets()

    def _setup_logging(self):
        """Sets up logging to file and formats log messages."""
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def log_message(self, msg):
        """Displays a message in the log text widget."""
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def _create_widgets(self):
        """Creates and arranges all UI elements."""
        tk.Label(self.root, text="API Key Path:").grid(row=0, column=0)
        self.api_key_path = tk.Entry(self.root)
        self.api_key_path.grid(row=0, column=1)

        tk.Label(self.root, text="Repo Owner:").grid(row=1, column=0)
        self.repo_owner_entry = tk.Entry(self.root)
        self.repo_owner_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Repo Name:").grid(row=2, column=0)
        self.repo_name_entry = tk.Entry(self.root)
        self.repo_name_entry.grid(row=2, column=1)

        tk.Label(self.root, text="File Name:").grid(row=3, column=0)
        self.file_name_entry = tk.Entry(self.root)
        self.file_name_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Target Hour:").grid(row=4, column=0)
        self.hour_entry = tk.Entry(self.root)
        self.hour_entry.insert(0, DEFAULT_HOUR)
        self.hour_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Target Minute:").grid(row=5, column=0)
        self.minute_entry = tk.Entry(self.root)
        self.minute_entry.insert(0, DEFAULT_MINUTE)
        self.minute_entry.grid(row=5, column=1)

        self.start_button = tk.Button(
            self.root, text="Start", command=self.start_activity)
        self.start_button.grid(row=6, columnspan=2)

        # Log display
        self.log_text = scrolledtext.ScrolledText(
            self.root, width=60, height=20)
        self.log_text.grid(row=7, columnspan=2)

    def start_activity(self):
        """Starts the GitHub Activity Influencer in a separate thread."""
        api_key = self._read_api_key(self.api_key_path.get())
        if not api_key:
            messagebox.showerror("Error", "Invalid API key.")
            return

        repo_owner = self.repo_owner_entry.get()
        repo_name = self.repo_name_entry.get()
        file_name = self.file_name_entry.get()
        target_hour = int(self.hour_entry.get())
        target_minute = int(self.minute_entry.get())

        influencer = GithubActivityInfluencer(
            api_key, repo_owner, repo_name, file_name, target_hour, target_minute)
        self.activity_thread = threading.Thread(
            target=influencer.start_activity)
        self.activity_thread.daemon = True
        self.activity_thread.start()

    def _read_api_key(self, file_path):
        """Reads the API key from a file."""
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    key, value = map(str.strip, line.split('=', 1))
                    if key == 'GITHUB_API_KEY':
                        return value
        except Exception as e:
            self.log_message(f"Error reading API key: {e}")
        return None


# Run the Tkinter app
root = tk.Tk()
app = AppUI(root)
root.mainloop()
