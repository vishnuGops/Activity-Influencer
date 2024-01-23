import logging
from github import Github
import os
from datetime import datetime, timedelta
import random
import time


# Configure logging
logging.basicConfig(filename='../activity_log.txt', level=logging.INFO,
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


# set time for running the commits check
hour = 00
min = 15


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
        if today.hour == hour and today.minute == min:
            print_and_log(f'It is ' + str(hour) + ":" +
                          str(min) + ' , checking commits at : {today} ')
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
                f'Waiting for {sleep_seconds} seconds until ' + str(hour) + ":" +
                str(min) + ' next day...')
            time.sleep(sleep_seconds)
        else:
            print_and_log("It's not " + str(hour) + ':' +
                          str(min) + " , not checking for commits")
            # Calculate the sleep duration until it's 11:50 pm
            sleep_seconds = abs((hour - today.hour) * 3600 +
                                (min - today.minute) * 60)
            print_and_log(
                f'Waiting for {sleep_seconds} seconds until today ' + str(hour) + ':' +
                str(min) + '...')
            time.sleep(sleep_seconds)


# Run the function
update_and_delete_file()
