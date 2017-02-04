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

    def __contains__(self, task):
        return self._is_task_duplicate(task)

# --> Public methods.

# Table methods.
    def create_table(self, *tables):
        """Creates tables with the same attribute structure.

        Args:
            tables: list of names for tables.

        Returns:
            No data is returned.
        """
        for table_name in tables:
            if table_name.isalnum():
                db_connection = sqlite3.connect("tasks.db")
                cursor = db_connection.cursor()
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS " + table_name +
                    """
                    (completed TEXT,
                    started TEXT,
                    created_at TEXT,
                    modified TEXT,
                    depends_from TEXT,
                    priority INTEGER,
                    description TEXT,
                    identifier TEXT)
                    """
                )
                db_connection.commit()
                db_connection.close()
            else:
                print("{} is not alphanumeric.".format(table_name))

    def drop_table(self, *tables):
        """Deletes specified tables."""
        for table_name in tables:
            if table_name.isalnum():
                db_connection = sqlite3.connect("tasks.db")
                cursor = db_connection.cursor()
                cursor.execute(
                    "DROP TABLE " + table_name
                )
                db_connection.commit()
                db_connection.close()
            else:
                print("{} is not alphanumeric.".format(table_name))

    def add_task_into(self, table, task):
        """Adds a given task to a given table."""
        success = False
        db_connection = sqlite3.connect("tasks.db")
        cursor = db_connection.cursor()
        if task not in self:
            cursor.execute(
                "INSERT INTO " + table +
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (str(task.info["completed"]), str(task.info["started"]),
                 str(task.info["created_at"]), str(task.info["modified"]),
                 str(task.info["depends_from"]), task.info["priority"],
                 task.info["description"], task.info["identifier"])
            )
            success = True
        db_connection.commit()
        db_connection.close()
        return success
# Task methods.

    def create_task(self, identifier, description, depends_from, priority):
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
        task = Task({
            "completed": None,
            "started": None,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "modified": None,
            "depends_from": depends_from,
            "priority": priority,
            "description": description,
            "identifier": identifier
        }, "NotStarted")

        status = self.add_task_into(
            "NotStarted", task
        )

        if status:
            self.recent_tasks.push(task)

    def start_task(self, identifier):
        pass

    def update_task():
        pass

    def delete_task(self, identifier, table):
        if identifier and table:
            try:
                db_connection = sqlite3.connect("tasks.db")
                cursor = db_connection.cursor()
                cursor.execute(
                    "DELETE FROM " + table + " WHERE identifier=?",
                    (identifier,)
                )
                db_connection.commit()
                db_connection.close()
                return self.recent_tasks.pop((identifier, table))
            except sqlite3.OperationalError as detail:
                print("Table name contains non-alphanumeric characters.")
                self.log.add(detail, time.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("Cant delete the desired task. Please, check the"
                  " parameters.")

    def completed_task():
        pass

    def dump_db(self, name="dump.sql"):
        """Dumps the content of tasks.db into a file."""
        db_connection = sqlite3.connect('tasks.db')
        with open(name, 'w') as f:
            for line in db_connection.iterdump():
                f.write('%s\n' % line)
        db_connection.close()

# --> Private methods.

    # TODO: Extend it to add multiple conditions.
    def _get_task(self, identifier, table):
        """Get entries that meet a certain condition.

        Args:
            pending
        Returns:
            Resulting rows of the query.
        """
        try:
            db_connection = sqlite3.connect("tasks.db")
            cursor = db_connection.cursor()
            cursor.execute(
                "SELECT * FROM " + table + " WHERE identifier=?",
                (identifier,)
            )
            entries = cursor.fetchall()
            db_connection.close()
            return entries
        except sqlite3.OperationalError as detail:
            print("Table name contains non-alphanumeric characters.")
            self.log.add(detail, time.strftime("%Y-%m-%d %H:%M:%S"))

    def _is_task_duplicate(self, task):
        """Checks if a given task is already in any of the tables.

        Args:
            task: data to look for.

        Returns:
            Boolean value depending on whether the given data is present in
            the database.
        """
        if task in self.recent_tasks:
            print("A task with that identifier already exists in the"
                  " database.")
            return True
        db_connection = sqlite3.connect("tasks.db")
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        for table in cursor.fetchall():
            # Get the table name from tuple.
            table_name = table[0]
            matches = self._get_task(task.info["identifier"], table_name)
            if len(matches) > 0:
                db_connection.close()
                return True
        db_connection.close()
        return False
