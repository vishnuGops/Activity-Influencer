import logging
from github import Github
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random
import time


# Configure logging
logging.basicConfig(filename='activity_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to print and log the info


def print_and_log(str):
    logging.info(str)
    print(str)

# Function to calculate the time until commits are checked


def time_until_target(target_hour, target_minute, today):
    # Create target time with today's date
    target_time = datetime.combine(
        datetime.today(), datetime.min.time())
    target_time += timedelta(hours=target_hour, minutes=target_minute)

    # If target time has already passed for today, add a day to the target time
    if target_time < datetime.now():
        target_time += timedelta(days=1)

    # Calculate time difference
    time_difference = target_time - \
        datetime.combine(datetime.today(), today.time())

    # Convert time difference to seconds
    seconds_until_target = max(time_difference.total_seconds(), 0)

    return seconds_until_target


# Function to update and delete file
def update_and_delete_file():
    print_and_log(
        f'****************************Github Activity Influencer Started****************************')

    while True:
        today = datetime.now()
        print_and_log(f'Checking date and time on {today}')
        # Check if it's 11:50 pm
        if today.hour == target_hour and today.minute == target_minute:
            print_and_log(f'It is ' + str(target_hour) + ":" +
                          str(target_minute) + f' , checking commits at : {today}')
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
            seconds_until_target = time_until_target(
                target_hour, target_minute, today)
            print_and_log(
                f'Waiting for {seconds_until_target} seconds until ' + str(target_hour) + ":" +
                str(target_minute) + ' next day...')
            time.sleep(seconds_until_target)
        else:
            print_and_log("It's not " + str(target_hour) + ':' +
                          str(target_minute) + " , not checking for commits")
            # Calculate the sleep duration until it's 11:50 pm
            seconds_until_target = time_until_target(
                target_hour, target_minute, today)

            print_and_log(
                f'Waiting for {seconds_until_target} seconds until today ' + str(target_hour) + ':' +
                str(target_minute) + '...')
            time.sleep(seconds_until_target)

# Main code


# Your GitHub personal access token - Generate one in your GitHub account settings
load_dotenv('token.env')
ACCESS_TOKEN = os.getenv('GITHUB_API_KEY')

# Your repository details
repo_owner = 'vishnugops'
repo_name = 'Activity-Influencer'


# set time for running the commits check
target_hour = 23
target_minute = 30


g = Github(ACCESS_TOKEN)
repo = g.get_user(repo_owner).get_repo(repo_name)

# File details
file_name = 'activity.txt'


# Run the function
update_and_delete_file()
