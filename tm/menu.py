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
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

# TODO: update dump and report actions pending.
# Select action depending on argument.
if args.action == "init":
    if pt.log:
        pt.log.add_entry("Log file creation",
                         "The logging file was successfully created.\n",
                         time.strftime("%Y-%m-%d %H:%M:%S"))
    if pt._check_if_exists():
        pt.log.add_entry("Create basic tables",
                         "The three tables ('NotStarted', 'WorkingOn',"
                         " 'Completed') were successfully created.\n",
                         time.strftime("%Y-%m-%d %H:%M:%S"))
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
elif args.action == "start":
    print("Label a task as started.\n")
    if sys.version_info[0] == 2:
        identifier = raw_input("Identifier: ")
    else:
        identifier = input("Identifier: ")
    pt.start_task(identifier)
elif args.action == "delete":
    print("Delete a task from the pending tasks list.")
    if sys.version_info[0] == 2:
        identifier = raw_input("Identifier: ")
    else:
        identifier = input("Identifier: ")
    pt.delete_task(identifier)
elif args.action == "completed":
    print("Label a task as completed.\n")
    if sys.version_info[0] == 2:
        identifier = raw_input("Identifier: ")
    else:
        identifier = input("Identifier: ")
    pt.completed_task(identifier)
else:
    print("No valid option selected.")
