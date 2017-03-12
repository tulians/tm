#!/usr/bin/env python3
# Actions to perform module.
# ===================================

import os
import sys
import time
import argparse
import lib.manage as m
from subprocess import run

current_directory = os.getcwd()
os.chdir(current_directory)
pt = m.PendingTasks(current_directory + "/.logs")

# Argument parsing.
parser = argparse.ArgumentParser(prog="tm", description="Task manager CLI")
parser.add_argument("action", help="action to perform",
                    choices=["init", "create", "start", "update", "delete",
                             "completed", "dump", "report", "partial"])
parser.add_argument("identifier", nargs="?", help="Task unique identifier")
parser.add_argument("partial_push_commit", nargs="?", help="Partial push"
                    " commit message")
args = parser.parse_args()

# Select action depending on argument.
if args.action == "init":
    if pt.log:
        pt.log.add_entry("Log file creation",
                         "The logging file was successfully created.",
                         time.strftime("%Y-%m-%d %H:%M:%S"))
    if pt._check_if_exists():
        pt.log.add_entry("Create basic tables",
                         "The three tables ('NotStarted', 'WorkingOn',"
                         " 'Completed') were successfully created.",
                         time.strftime("%Y-%m-%d %H:%M:%S"))
    print("Task manager initialized in project.")
elif args.action == "create":
    print("New task creation.\n")
    identifier = input("Identifier: ")
    description = input("Description: ")
    depends_from = input("Depends from: ")
    priority = int(input("Priority: "))
    pt.create_task(identifier, description, depends_from, priority)
    print("Task successfully created.")
elif args.action == "start":
    identifier = args.identifier
    pt.start_task(identifier)
    print("Task successfully labeled as started.")
elif args.action == "update":
    identifier = args.identifier
    print("Update task {}\n".format(identifier))
    updates = {}
    description = input("New description: ")
    depends_from = input("New dependencies: ")
    priority = input("New priority: ")
    if description:
        updates["description"] = description
    if depends_from:
        updates["depends_from"] = depends_from
    if priority:
        updates["priority"] = int(priority)
    if updates:
        pt.update_task(identifier, **updates)
elif args.action == "delete":
    identifier = args.identifier
    pt.delete_task(identifier)
    git_checkout_string = "git checkout master"
    run(git_checkout_string.strip().split(" "))
    git_delete_branch_local = "git branch -d {}".format(identifier)
    run(git_delete_branch_local.strip().split(" "))
    print("Task successfully deleted.")
elif args.action == "completed":
    identifier = args.identifier
    pt.completed_task(identifier, pt.partials_exist)
    print("Task successfully labeled as completed.")
elif args.action == "dump":
    pt.dump_db()
    print("Database dump successfully generated.")
elif args.action == "report":
    identifier = args.identifier
    pt.generate_report(identifier)
elif args.action == "partial":
    identifier = args.identifier
    if args.partial_push_commit:
        pt.partial(identifier, args.partial_push_commit)
        print("Commit successfully generated.")
else:
    print("No valid option selected.")
