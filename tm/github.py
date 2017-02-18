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
    files_are_safe = sanitize_string(files_to_add)
    if files_are_safe:
        git_cmd_string = "git add {}".format(files_to_add)
        call(git_cmd_string, shell=True)
    else:
        print("The given parameters contain not safe characters or commands.")


def get_status(flags=""):
    """Performs 'git status [-flags]' operation."""
    flags_to_use = " ".join(flags)
    flags_are_safe = sanitize_string(flags_to_use)
    if flags_are_safe or (flags_are_safe == ""):
        git_cmd_string = "git status {}".format(flags_are_safe)
        git_cmd_string = git_cmd_string.strip()
        call(git_cmd_string, shell=True)
    else:
        print("The given parameters contain not safe characters or commands.")
