#!/usr/bin/env python

# tm - Task management.
# Actions to perform module.
# Author: Julian Ailan
# ===================================

import os
import sys
import time
import argparse
import lib.manage as m

current_directory = os.getcwd()
os.chdir(current_directory)
pt = m.PendingTasks(current_directory + "/.logs")

# Argument parsing.
parser = argparse.ArgumentParser(prog="tm", description="Task manager CLI")
parser.add_argument("action", help="action to perform",
                    choices=["init", "create", "start", "update", "delete",
                             "completed", "dump", "report"])
parser.add_argument("identifier", nargs="?", help="Task unique identifier")
args = parser.parse_args()

# TODO: update action pending.
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
    if sys.version_info[0] == 2:
        identifier = raw_input("Identifier: ")
        description = raw_input("Description: ")
        depends_from = raw_input("Depends from: ")
        priority = int(raw_input("Priority: "))
    else:
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
# TODO: Review what happens with the branch in this case.
elif args.action == "delete":
    identifier = args.identifier
    pt.delete_task(identifier)
elif args.action == "completed":
    identifier = args.identifier
    pt.completed_task(identifier)
    print("Task successfully labeled as completed.")
elif args.action == "dump":
    print("Generates a dump file with the task database..")
    pt.dump_db()
    print("Database dump successfully generated.")
elif args.action == "report":
    identifier = args.identifier
    pt.generate_report(identifier)
else:
    print("No valid option selected.")
