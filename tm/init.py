#!/usr/bin/env python

# tm - Task management.
# Repository initialization module.
# Author: Julian Ailan
# ===================================

# TODO: This is just a scratch of the functionality.

# Built-in modules.
import os
import sys
# Project specific modules.
from manage import PendingTasks
from logger import Logger

current_directory = os.getcwd()
pt = PendingTasks(current_directory)
tables_creation_successful = pt._check_if_exists()

config_file_path = current_directory + ("/config.tm")
with open(config_file_path, "w") as f:
    f.write("Configuration file. Created at {}\n".format(
        time.strftime("%Y-%m-%d %H:%M:%S")))
    if tables_creation_successful:
        f.write("The three tables ('NotStarted', 'WorkingOn', '#Completed')"
                " were successfully created.\n")
    else:
        f.write("There were issues while trying to create the needed"
                " tables.\n")
    if pt.log:
        f.write("Logging file successfully created.\n")
    else:
        f.write("There were issues while trying to create the logging"
                " file.\n")
