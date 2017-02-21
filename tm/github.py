# tm - Task management.
# Github abstraction module.
# Author: Julian Ailan
# ===================================

# Built-in modules.
from subprocess import call, check_output
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


def commit(message="", flags="-m"):
    """Performs 'git commit -m [-message]' operation."""
    if message == "" and flags == "":
        raise ValueError("No valid message/flag values received.")
    flags_are_safe = sanitize_string(flags)
    if (message == sanitize_string(message)) and flags_are_safe:
        git_cmd_string = "git commit {0} '{1}'".format(flags_are_safe, message)
        _execute(git_cmd_string)
    else:
        print("The given commit message contains not safe characters or"
              " commands.")


def push(flags="", server="origin", branch="master"):
    """Performs 'git push [-flags] [-server] [-branch]' operation."""
    squashed = flags + server + branch
    if squashed == sanitize_string(squashed):
        git_cmd_string = "git push {0} {1} {2}".format(flags, server, branch)
        if flags == "":
            git_cmd_string = " ".join(git_cmd_string.split())
        _execute(git_cmd_string)
    else:
        print("The given server and/or branch contain not safe characters or"
              " commands.")


def branch(name):
    """Performs 'git checkout -b [-name]' operation."""
    if (not name) or (name == ""):
        raise ValueError("No valid branch name received.")
    if name == sanitize_string(name):
        git_cmd_string = "git checkout -b {}".format(name)
        _execute(git_cmd_string)
    else:
        print("The given branch name contains not safe characters or"
              " commands.")


def merge(from_branch, to_branch):
    """Performs the merging of two branches."""
    if not (from_branch and to_branch):
        raise ValueError("No valid branch names received.")
    squashed = from_branch + to_branch
    if squashed == sanitize_string(squashed):
        git_checkout_string = "git checkout {}".format(to_branch)
        git_merge_string = "git merge {}".format(from_branch)
        git_delete_branch_string = "git branch -d {}".format(from_branch)
        git_cmd_string = (git_checkout_string + "; " + git_merge_string
                          + "; " + git_delete_branch_string)
        _execute(git_cmd_string)
    else:
        print("The given branch names contain not safe characters or"
              " commands.")


# --> Utilities.
def changed_files():
    # Get all changed files.
    files = check_output("git status -s | cut -c4-", shell=True)
    # Remove trailing whitespaces.
    files = files.strip()
    return list(files.split("\n"))


def _execute(git_cmd_string):
    git_cmd_string = git_cmd_string.strip()
    call(git_cmd_string, shell=True)


def make(commit_message, files=changed_files()):
    add_files(files)
    status()
    commit(commit_message)
    push()
