# tm - Task management library.
# Logger module.
# Author: Julian Ailan
# ===================================

# Built-in modules.
import time


class Logger(object):
    def __init__(self, creation_path):
        self.log_path = creation_path + "/log.txt"
        with open(self.log_path, "w") as self.log:
            self.log.write("Task Manager Log. Created at {}\n".format(
                time.strftime("%Y-%m-%d %H:%M:%S")
            ))

    def add(self, operation, detail, timestamp):
        self.log_path = creation_path + "/log.txt"
        with open(self.log_path, "w") as self.log:
            self.log.write(
                "-" * 50 +
                "During {0} at {1}:\n"
                "Detail: {2}\n".format(operation, timestamp, detail)
            )
