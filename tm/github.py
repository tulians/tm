# tm - Task management.
# Github abstraction module.
# Author: Julian Ailan
# ===================================

# Built-in modules.
from subprocess import call
# Project specific modules.
from utils import sanitize_string


def add_files(files):
    files_to_add = " ".join(files)
    files_are_safe = sanitize_string(files_to_add)
    if files_are_safe:
        git_cmd_string = "git add {}".format(files_to_add)
        call(git_cmd_string, shell=True)
    else:
        print("The given parameters contain not safe characters or commands.")
