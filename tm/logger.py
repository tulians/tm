# tm - Task management library.
# Logger module.
# Author: Julian Ailan
# ===================================

# Built-in modules.
import os
import time


class Logger(object):
    def __init__(self, creation_path, project_name):
        """Logger's constructor. The log file is placed by default in
        /opt/tm/logs/ directory.
        """
        if creation_path[-1] != "/":
            creation_path += "/"

        try:
            if not os.path.exists(creation_path):
                # Creates the directory, along with all the non-existent needed
                # path subdirectories.
                os.makedirs(creation_path)
        except OSError as detail:
            print("The logger file could not be created due to permission"
                  " issues. Run the command again using 'sudo'. Exception"
                  " detail: " + str(detail))

        log_name = "log.txt"
        if project_name:
            log_name = str(project_name) + "_" + log_name

        self.log_path = creation_path + log_name
        with open(self.log_path, "w+") as self.log:
            self.log.write("Task Manager Log. Created at {}\n".format(
                time.strftime("%Y-%m-%d %H:%M:%S")
            ))

    def add_entry(self, operation, detail, timestamp):
        with open(self.log_path, "a") as self.log:
            self.log.write(
                "{0} | Operation: {1} | Detail: {2}\n".format(
                    timestamp, operation, detail
                )
            )
