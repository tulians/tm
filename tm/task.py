# tm - Task management library.
# Tasks module.
# Author: Julian Ailan
# ===================================


labels = ("completed", "started", "created_at", "modified", "depends_from",
          "priority", "description", "identifier")


class Task(object):
    """Simple task class"""
    def __init__(self, info, table):
        self.info = info
        self.table = table
