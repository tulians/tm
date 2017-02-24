# tm - Task management.
# Github abstraction module.
# Author: Julian Ailan
# ===================================

# Built-in modules.
try:
    from subprocess import run, check_output, Popen, PIPE
except ImportError:
    from subprocess import call, check_output, Popen, PIPE


def add_files(files):
    """Performs 'git add [-files]' operation."""
    if not files:
        raise ValueError("No files received for adding.")
    files_to_add = " ".join(files)
    git_cmd_string = "git add {}".format(files_to_add)
    _execute(git_cmd_string.strip().split(" "))


def status(flags=""):
    """Performs 'git status [-flags]' operation."""
    git_cmd_string = "git status {}".format(" ".join(flags))
    _execute(git_cmd_string.strip().split(" "))


def commit(message):
    """Performs 'git commit -m [-message]' operation."""
    if message == "" or not message:
        raise ValueError("No valid message/flag values received.")
    git_cmd_list = "git commit -m".split(" ")
    git_cmd_list.append(message)
    _execute(git_cmd_list)


def push(server, branch):
    """Performs 'git push [-server] [-branch]' operation."""
    if not (server and branch):
        raise ValueError("Not valid server and/or branch values given.")
    git_cmd_string = "git push {0} {1}".format(server, branch)
    _execute(git_cmd_string.strip().split(" "))


def branch(name):
    """Performs 'git checkout -b [-name]' operation."""
    if (not name) or (name == ""):
        raise ValueError("No valid branch name received.")
    git_cmd_string = "git checkout -b {}".format(name)
    _execute(git_cmd_string.strip().split(" "))


def merge(from_branch, to_branch):
    """Performs the merging of two branches."""
    if not (from_branch and to_branch):
        raise ValueError("No valid branch names received.")
    git_checkout_string = "git checkout {}".format(to_branch)
    _execute(git_checkout_string)
    git_merge_string = "git merge {}".format(from_branch)
    _execute(git_merge_string)
    git_delete_branch_string = "git branch -d {}".format(from_branch)
    _execute(git_delete_branch_string)


# --> Utilities.
def _changed_files():
    """Returns a list with all the changed files after the last commit"""
    # Get all changed files, avoiding the use of shell=True.
    status = Popen(("git", "status", "-s"), stdout=PIPE)
    files = check_output(('cut', '-c4-'), stdin=status.stdout)
    return filter(None, files.split("\n"))


def _execute(git_cmd_list):
    """Runs the git commands."""
    # Python 2.X and 3.X compatibility.
    try:
        run(git_cmd_list)
    except NameError:
        call(git_cmd_list)


def make(commit_message, server, branch, files=_changed_files(), flags=""):
    """Pushes commits to the remote repository."""
    add_files(files)
    status(flags)
    commit(commit_message)
    push(server, branch)
