# tm - Task management.
# Github abstraction module.
# Author: Julian Ailan
# ===================================

# Built-in modules.
from subprocess import call
# Project specific modules.
from utils import sanitize_string


def add_files(files):
    """Performs 'git add [-files]' operation."""
    if not files:
        raise ValueError("No files received for adding.")
    files_to_add = " ".join(files)
    if sanitize_string(files_to_add):
        git_cmd_string = "git add {}".format(files_to_add)
        _execute(git_cmd_string)
    else:
        print("The given parameters contain not safe characters or commands.")


def status(flags=""):
    """Performs 'git status [-flags]' operation."""
    flags_to_use = " ".join(flags)
    flags_are_safe = sanitize_string(flags_to_use)
    if flags_are_safe or (flags_are_safe == ""):
        git_cmd_string = "git status {}".format(flags_are_safe)
        _execute(git_cmd_string)
    else:
        print("The given parameters contain not safe characters or commands.")


def commit(message):
    """Performs 'git commit -m [-message]' operation."""
    if message == sanitize_string(message):
        git_cmd_string = "git commit -m '{}'".format(message)
        _execute(git_cmd_string)
    else:
        print("The given commit message contains not safe characters or"
              " commands.")


def push(server, branch):
    """Performs 'git push [-server] [-branch]' operation."""
    squashed = server + branch
    if sanitize_string(squashed):
        git_cmd_string = "git push {} {}".format(server, branch)
        _execute(git_cmd_string)
    else:
        print("The given server and/or branch contain not safe characters or"
              " commands.")


def _execute(git_cmd_string):
    git_cmd_string = git_cmd_string.strip()
    call(git_cmd_string, shell=True)
