import os

# Constants
APP_FOLDER = "C:\\Program Files (x86)\\GitAI"
LOG_FOLDER = os.path.join(APP_FOLDER, "log")
TOKEN_FOLDER = os.path.join(APP_FOLDER, "token")
LOG_FILE = os.path.join(LOG_FOLDER, 'activity_log.txt')
LOGIN_FILE = os.path.join(TOKEN_FOLDER, 'login.txt')
VERSION = 2.0
DEFAULT_HOUR = 23
DEFAULT_MINUTE = 30


def setup_folders():
    os.makedirs(LOG_FOLDER, exist_ok=True)
    os.makedirs(TOKEN_FOLDER, exist_ok=True)
