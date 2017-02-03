# tasks - Task management library.
# Task management module.
# Author: Julian Ailan
# ===================================

"""Provides a class for managing pending tasks tables."""

# Built-in modules.
import time
import sqlite3
# Project specific modules.
import utils as u
import logger as lg
from cache import TaskCache
from task import Task


class PendingTasks(object):
    """Manages the creation, modification and status of pending tasks."""

    def __init__(self):
        """Tasks manager constructor"""
        self.create_table("NotStarted", "WorkingOn", "Completed")
        self.log = lg.Logger()
        # Use this queue to save the most recent new, modified, on process or
        # completed tasks. These tasks should be saved in tuples along with
        # their corresponding table. The length of this queue should not be
        # greater than 10 tasks.
        self.recent_tasks = TaskCache(10)

    def create_table(self, *tables):
        """Creates tables with the same attributestructure.

        Args:
            tables: list of names for tables.

        Returns:
            No data is returned.
        """
        for table_name in tables:
            if table_name.isalnum():
                self.db_connection = sqlite3.connect("tasks.db")
                self.cursor = self.db_connection.cursor()
                self.cursor.execute(
                    "CREATE TABLE IF NOT EXISTS " + table_name +
                    """
                    (completed TEXT,
                    created_at TEXT,
                    modified TEXT,
                    depends_from TEXT,
                    priority INTEGER,
                    description TEXT,
                    identifier TEXT)
                    """
                )
                self.db_connection.commit()
                self.db_connection.close()
            else:
                print("{} is nor alphanumeric.".format(table_name))

    def create_task(self, identifier, description, depends_from, priority):
        # TODO: Check if the identifier already exists in any of the tables.
        # Avoid duplicates. ACID!
        """Creates a new pending task.

        Args:
            identifier: short string that uniquely identifies the task.
            description: string that contains a verbose explanation of the new
            task.
            depends_from: list that contains the task ids that should be first
            compeleted before.
            priority: associated integer value.

        Returns:
            No data is returned.
        """
        new_task = {
            "identifier": identifier,
            "description": description,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "depends_from": depends_from,
            "priority": priority,
        }
        self.db_connection = sqlite3.connect("tasks.db")
        self.cursor = self.db_connection.cursor()
        self.cursor.execute(
            """
            INSERT INTO NotStarted
            VALUES (NULL, ?, NULL, ?, ?, ?, ?)
            """,
            (str(new_task["created_at"]), str(new_task["depends_from"]),
             new_task["priority"], new_task["description"],
             new_task["identifier"])
        )
        self.db_connection.commit()
        self.db_connection.close()
        self.recent_tasks.push(Task(new_task, "NotStarted"))

    def get_task(self, identifier, table):
        # TODO: Extend it to add multiple conditions.
        """Get entries that meet a certain condition.

        Args:
            pending
        Returns:
            Resulting rows of the query.
        """
        self.db_connection = sqlite3.connect("tasks.db")
        self.cursor = self.db_connection.cursor()
        try:
            self.cursor.execute(
                "SELECT * FROM " + table + " WHERE identifier=?",
                (identifier,)
            )
            return self.cursor.fetchall()
        except sqlite3.OperationalError as detail:
            print("Table name contains non-alphanumeric characters.")
            self.log.add(detail, time.strftime("%Y-%m-%d %H:%M:%S"))
        self.db_connection.close()
