import logging
import random
import time
from datetime import datetime, timedelta
import pytz
import gc
from github import Github


class GithubActivityInfluencer:
    def __init__(self, api_key, repo_owner, repo_name, file_name, target_hour, target_minute, app_ui):
        self.api_key = api_key
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.file_name = file_name
        self.target_hour = target_hour
        self.target_minute = target_minute
        self.github = Github(api_key)
        self.app_ui = app_ui  # Add this line to hold reference to the UI

        try:
            self.repo = self.github.get_user(repo_owner).get_repo(repo_name)
            self.log_message(
                f"Login Successful -------> {repo_owner} | {repo_name} ")
        except Exception as e:
            error_message = f"Error accessing repository '{
                repo_owner}/{repo_name}': {e}"
            self.log_message(error_message)
            raise

    def log_message(self, msg):
        logging.info(msg)
        print(msg)
        if self.app_ui:  # Use app_ui to display in UI if it exists
            self.app_ui.log_message(msg)

    def check_and_generate_commits(self):
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
        while True:
            today = datetime.now()
            self.log_message(f'** Checking commits on {today} **')

            if today.hour == self.target_hour and today.minute == self.target_minute:
                self.log_message(
                    f'--> Checking commits at target time: {today}')
                self.check_and_generate_commits()

            wait_time = self._time_until_target(today)

            # Format wait time in hours, minutes, and seconds if greater than 60 seconds
            if wait_time >= 3600:
                hours = int(wait_time // 3600)
                minutes = int((wait_time % 3600) // 60)
                seconds = int(wait_time % 60)
                self.log_message(
                    f'--> Waiting {hours} hours, {minutes} minutes, and {seconds} seconds...')
            elif wait_time >= 60:
                minutes = int(wait_time // 60)
                seconds = int(wait_time % 60)
                self.log_message(
                    f'--> Waiting {minutes} minutes and {seconds} seconds...')
            else:
                self.log_message(
                    f'--> Waiting {round(wait_time, 2)} seconds...')

            time.sleep(wait_time)
            gc.collect()

    def _time_until_target(self, current_time):
        target_time = datetime.combine(current_time, datetime.min.time()) + timedelta(
            hours=self.target_hour, minutes=self.target_minute
        )
        if target_time < current_time:
            target_time += timedelta(days=1)
        return (target_time - current_time).total_seconds()
