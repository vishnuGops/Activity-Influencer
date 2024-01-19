import logging
from github import Github
import os
from datetime import datetime, timedelta
import random
import time


# Configure logging
logging.basicConfig(filename='C:/Users/Vishnu-Server/Desktop/Coding/Activity-Influencer/activity_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def print_and_log(str):
    logging.info(str)
    print(str)


print_and_log(
    f'****************************Github Activity Influencer Started****************************')


# Your GitHub personal access token - Generate one in your GitHub account settings
ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

# Your repository details
repo_owner = 'vishnugops'
repo_name = 'Activity-Influencer'


g = Github(ACCESS_TOKEN)
repo = g.get_user(repo_owner).get_repo(repo_name)

# File details
file_name = 'activity.txt'

# Function to update and delete file


def update_and_delete_file():
    while True:
        today = datetime.now()
        print_and_log(f'Checking date and time on {today}')
        # Check if it's 11:50 pm
        if today.hour == 23 and today.minute == 50:
            print_and_log(f'It is 11:50, checking commits at : {today} ')
            # Check the number of commits for the day
            commits_today = list(repo.get_commits(since=today.replace(hour=0, minute=0, second=0, microsecond=0),
                                                  until=today.replace(hour=23, minute=59, second=59, microsecond=999999)))

            if len(commits_today) == 0:
                # If no commits for the day, generate random commits between 2 and 16
                num_commits = random.randint(2, 16)
                print_and_log(f'Random number of commits : {num_commits}')

                for i in range(num_commits):
                    # Randomly pick a time within the last 10 days
                    commit_date = today - timedelta(days=random.randint(0, 10))

                    # Update the file content with commit information
                    new_content = f'Commit {i + 1} on {commit_date}'
                    commit_message = f'Commit {i + 1} - {commit_date}'
                    contents = repo.get_contents(file_name, ref='main')
                    repo.update_file(contents.path, commit_message,
                                     new_content, contents.sha, branch='main')

                    print_and_log(f'Committed change {i + 1} on {commit_date}')
            else:
                print_and_log(
                    f'Commits already made for today - {today} : {len(commits_today)}')

            # Calculate the sleep duration until the next day
            sleep_seconds = (23 * 3600) + (55 * 60)
            print_and_log(
                f'Waiting for {sleep_seconds} seconds until 11:50 pm next day...')
            time.sleep(sleep_seconds)
        else:
            print_and_log("It's not 11:50, not checking for commits")
            # Calculate the sleep duration until it's 11:50 pm
            sleep_seconds = abs((23 - today.hour) * 3600 +
                                (50 - today.minute) * 60)
            print_and_log(
                f'Waiting for {sleep_seconds} seconds until today 11:50 pm...')
            time.sleep(sleep_seconds)


# Run the function
update_and_delete_file()
