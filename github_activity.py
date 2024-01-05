from github import Github
import os
from datetime import datetime

# Your GitHub personal access token - Generate one in your GitHub account settings
ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

# Your repository details
repo_owner = 'vishnugops'
repo_name = 'Activity-Influencer'

g = Github(ACCESS_TOKEN)
repo = g.get_user(repo_owner).get_repo(repo_name)

# File details
file_name = 'activity.txt'
file_content = 'Initial commit'

# Create the initial file
# repo.create_file(file_name, 'Initial commit', file_content, branch='main')

# Function to update and delete the file


def update_and_delete_file():
    today = datetime.now()

    # Randomly select the number of commits
    # num_commits = random.randint(2, 6)
    num_commits = input("Num of commits: ")

    for i in range(int(num_commits)):
        # Randomly pick a time within the last 10 days
        commit_date = today

        # Update the file content with commit information
        new_content = f'Commit {i + 1} on {commit_date}'
        commit_message = f'Commit {i + 1} - {commit_date}'
        contents = repo.get_contents(file_name, ref='main')
        repo.update_file(contents.path, commit_message,
                         new_content, contents.sha, branch='main')

        print(f'Committed change {i + 1} on {commit_date}')


# Create commits and delete file
update_and_delete_file()
