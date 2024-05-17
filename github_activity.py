import logging
from datetime import datetime, timedelta
import random
import time
import pytz
import gc  # Importing garbage collector module

from github import Github

# Version of the app


def display_version():
    version = 1.9
    print_and_log(
        f'****************************Github Activity Influencer {version} Started****************************')


# Configure logging
logging.basicConfig(filename='../activity_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Function to print and log the info
def print_and_log(msg):
    logging.info(msg)
    print(msg)


# Function to calculate the time until commits are checked
def time_until_target(target_hour, target_minute, today):
    target_time = datetime.combine(datetime.today(), datetime.min.time())
    target_time += timedelta(hours=target_hour, minutes=target_minute)

    if target_time < datetime.now():
        target_time += timedelta(days=1)

    time_difference = target_time - \
        datetime.combine(datetime.today(), today.time())

    seconds_until_target = max(time_difference.total_seconds(), 0)

    return seconds_until_target


# Function to check the last commit and generate random commits if not made today
def check_last_commit_and_generate(repo, file_name):
    # Retrieve the list of commits
    commits = repo.get_commits()

    # Check if there are any commits
    if commits:
        # Get the latest commit (first in the list)
        last_commit = commits[0]
        # Assuming last_commit_date is a datetime object in UTC timezone
        last_commit_date_utc = last_commit.commit.author.date
        pst_timezone = pytz.timezone('America/Los_Angeles')  # PST timezone

        # Convert UTC datetime to PST datetime
        last_commit_date_pst = last_commit_date_utc.astimezone(pst_timezone)

        # Extract date component in PST timezone
        last_commit_date_pst_date = last_commit_date_pst.date()
        print_and_log("--> Last commit made: " +
                      str(last_commit_date_pst_date))
        # Get today's date
        today = datetime.now().date()

        # Check if the last commit was made today
        if last_commit_date_pst_date != today:
            # Generate random commits
            # min_value = 2
            # max_value = 14
            # mean_dist = 8
            # std_dev = 2
            # num_commits = number_from_normal_curve(
            #     min_value, max_value, mean_dist, std_dev)
            num_commits = random.randint(1, 16)

            print_and_log(
                f'--> No commits made today. Generating {num_commits} random commits...')

            for i in range(num_commits):
                commit_date = today
                new_content = f'Commit {i + 1} on {commit_date}'
                commit_message = f'Commit {i + 1} - {commit_date}'
                contents = repo.get_contents(file_name, ref='main')
                repo.update_file(contents.path, commit_message,
                                 new_content, contents.sha, branch='main')

                print_and_log(f'--> Committed change {i + 1} on {commit_date}')
        else:
            print_and_log(
                '--> Last commit was made today. No need to generate commits.')
    else:
        print_and_log('--> No commits found in the repository.')


# Function to read API key from file
def read_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = map(str.strip, line.split('=', 1))
                if key == 'GITHUB_API_KEY':
                    return value
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

    return None


# Function to generate a random number from a normal distribution within a specified range
@DeprecationWarning
def number_from_normal_curve(min_value, max_value, mu, sigma):
    while True:
        number = random.normalvariate(mu, sigma)
        if min_value <= number <= max_value:
            return round(number)


# Main code
def generate_activity_based_on_commits():
    display_version()
    ACCESS_TOKEN = read_api_key(
        'C:\\Users\\Vishnu-Server\\Desktop\\Coding\\Activity-Influencer\\token.env')
    repo_owner = 'vishnugops'
    repo_name = 'Activity-Influencer'
    target_hour = 23
    target_minute = 30

    g = Github(ACCESS_TOKEN)
    repo = g.get_user(repo_owner).get_repo(repo_name)
    file_name = 'activity.txt'

    while True:
        today = datetime.now()
        print_and_log(f'**CHECKING DATE AND COMMITS ON --> {today}')

        if today.hour == target_hour and today.minute == target_minute:
            # if True:
            print_and_log(
                f'--> It is {target_hour}:{target_minute}, checking commits at: {today}')
            check_last_commit_and_generate(repo, file_name)
            seconds_until_target = time_until_target(
                target_hour, target_minute, today)
            print_and_log(
                f'--> Waiting for {seconds_until_target} seconds until {target_hour}:{target_minute}...')
            time.sleep(seconds_until_target)
            gc.collect()  # Perform garbage collection
        else:
            print_and_log(
                f"--> It's not {target_hour}:{target_minute}, not checking for commits")
            seconds_until_target = time_until_target(
                target_hour, target_minute, today)
            print_and_log(
                f'--> Waiting for {seconds_until_target} seconds until {target_hour}:{target_minute}...')
            time.sleep(seconds_until_target)
            gc.collect()  # Perform garbage collection


# Run the function
generate_activity_based_on_commits()
