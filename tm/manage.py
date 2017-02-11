# tm - Task management library.
# Task management module.
# Author: Julian Ailan
# ===================================

"""Provides a class for managing pending tasks tables."""

# Built-in modules.
import os
import time
import sqlite3
# Project specific modules.
import utils as u
from logger import Logger
from cache import TaskCache
from task import Task, labels


class PendingTasks(object):
    """Manages the creation, modification and status of pending tasks."""

    def __init__(self, current_directory):
        """Tasks manager constructor"""
        self.create_table("NotStarted", "WorkingOn", "Completed")
        self.log = Logger(current_directory)
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

    def add_task_into(self, table, task, moving_task=False):
        """Adds a given task to a given table."""
        success = False
        db_connection = sqlite3.connect("tasks.db")
        cursor = db_connection.cursor()
        if (task not in self) or moving_task:
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
        else:
            print("There were problems when adding the created task"
                  " to the 'NotStarted' table.")

    def start_task(self, identifier):
        """Sets a task as started, after checking dependencies.
        Args:
            identifier: string that uniquely identifies the task.
        Returns:
            - If the task was correctly added to the 'WorkingOn' table
            the recently started task is returned.
            - Instead, if the task depends from previous uncompleted tasks
            an informational message is returned.
        """
        task = self._get_task(identifier, "NotStarted")
        if task:
            started_task_info = dict(zip(labels, task[0]))
            depends_from = u.list_from_string(
                started_task_info["depends_from"])
            if not depends_from:
                started_task_info["started"] = time.strftime("%Y-%m-%d "
                                                             "%H:%M:%S")
                started_task = Task(started_task_info, "WorkingOn")
                status = self.add_task_into("WorkingOn", started_task, True)
                self.delete_task(identifier)
                print("Successfully labeled task as started.")
                if status:
                    if started_task in self.recent_tasks:
                        self.recent_tasks.update(started_task, "WorkingOn")
                        print("Task updated in cache.")
                    else:
                        self.recent_tasks.push(started_task)
                        print("Task added to cache.")
                    return started_task
                else:
                    print("There were problems when adding the started task"
                          " to the 'WorkingOn' table.")
            else:
                incomplete_tasks = self._meets_dependencies(depends_from)
                msg = ("The current task ('{}') depends from ".format(
                    started_task_info["identifier"]))
                if len(incomplete_tasks) == 1:
                    msg += ("task '{}', which has to be completed before"
                            " starting this task.".format(incomplete_tasks[0]))
                else:
                    msg += ("tasks {}. Please complete them "
                            "first.".format(incomplete_tasks))
                    msg = u.replace_last_comma(msg)
                chars_to_remove = ["[", "]"]
                for char in chars_to_remove:
                    msg = msg.replace(char, "")
                return msg
        else:
            print("There is no task with that identifier waiting to be"
                  " started.")

    def update_task(self, identifier, **update_values):
        """Updates task information, no matter the table the task is in.
        Args:
            identifier: string that uniquely identifies the task.
            update_values: key-value arguments of task information to update.
        Returns:
            No data is returned.
        """
        table = self._get_table(identifier)
        if table:
            task = self._get_task(identifier, table)
            modified_task_info = dict(zip(labels, task[0]))
            for key, value in update_values.items():
                    modified_task_info[key] = value
            modified_task_info["modified"] = time.strftime("%Y-%m-%d %H:%M:%S")
            modified_task = Task(modified_task_info, table)
            db_connection = sqlite3.connect("tasks.db")
            cursor = db_connection.cursor()
            cursor.execute(
                "UPDATE " + table +
                """
                SET completed=?, started=?, created_at=?, modified=?,
                depends_from=?, priority=?, description=?, identifier=?
                WHERE identifier=?
                """,
                (modified_task.info["completed"],
                 modified_task.info["started"],
                 modified_task.info["created_at"],
                 modified_task.info["modified"],
                 str(modified_task.info["depends_from"]),
                 modified_task.info["priority"],
                 modified_task.info["description"],
                 modified_task.info["identifier"],
                 modified_task.info["identifier"])
            )
            db_connection.commit()
            db_connection.close()
            if modified_task in self.recent_tasks:
                self.recent_tasks.update(modified_task)
                print("Information updated.")
            else:
                self.recent_tasks.push(modified_task)
                print("Task added to cache.")
        else:
            print("The given identifier is not present in any table.")

    def delete_task(self, identifier):
        """Deletes a task in any table.
        Args:
            identifier: string that uniquely identifies the task.
        Returns:
            If the task with the given identifier exists in the cache
            it is returned after its deletition.
        """
        table = self._get_table(identifier)
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
                self.log.add("delete", detail, time.strftime(
                    "%Y-%m-%d %H:%M:%S"))
        else:
            print("Cant delete the desired task. Please, check the"
                  " parameters.")

    def completed_task(self, identifier):
        """Labels a task as completed.
        Args:
            identifier: string that uniquely identifies the task.
        Returns:
            The recently labeled task is returned.
        """
        task = self._get_task(identifier, "WorkingOn")
        if task:
            completed_task_info = dict(zip(labels, task[0]))
            completed_task_info["completed"] = time.strftime(
                "%Y-%m-%d %H:%M:%S")
            completed_task = Task(completed_task_info, "Completed")
            status = self.add_task_into("Completed", completed_task, True)
            self.delete_task(identifier)
            if status:
                if completed_task in self.recent_tasks:
                    self.recent_tasks.update(completed_task, "Completed")
                    print("Information updated.")
                else:
                    self.recent_tasks.push(completed_task)
                    print("Task added to cache.")
                return completed_task
            else:
                print("There were problems when adding the completed task"
                      " to the 'Completed' table.")
        else:
            print("There is no task with that identifier waiting to be"
                  " completed.")

    def dump_db(self, name="dump.sql"):
        """Dumps the content of tasks.db into a file."""
        db_connection = sqlite3.connect('tasks.db')
        with open(name, 'w') as f:
            for line in db_connection.iterdump():
                f.write('%s\n' % line)
        db_connection.close()

    def generate_report(self, identifier):
        """Generates a report with the state of a given task.
        Args:
            identifier: string that uniquely identifies the task.
        Returns:
            No data is returned.
        """
        table = self._get_table(identifier)
        if identifier and table:
            task = self._get_task(identifier, table)
            if task:
                task_info = dict(zip(labels, task[0]))
                depends_from = u.list_from_string(task_info["depends_from"])
                incomplete_tasks = self._meets_dependencies(depends_from)
                msg = ("Task '{}' depends from ".format(
                    task_info["identifier"]))
                if len(incomplete_tasks) == 0:
                    msg += ("no other task(s).")
                elif len(incomplete_tasks) == 1:
                    msg += ("task '{}', which has to be completed before"
                            " starting this task.".format(incomplete_tasks[0]))
                else:
                    msg += ("tasks {}. Please complete them"
                            " first.".format(incomplete_tasks))
                    msg = u.replace_last_comma(msg)
                chars_to_remove = ["[", "]"]
                for char in chars_to_remove:
                    msg = msg.replace(char, "")
                print(
                    "Task #{0}:\n"
                    "- Description: {1}\n"
                    "- Priority: {2}\n"
                    "- Dependencies {3}\n"
                    "- Created at: {4}\n"
                    "- Started at: {5}\n"
                    "- Completed at: {6}\n"
                    "- Modified at: {7}\n".format(
                        task_info["identifier"],
                        task_info["description"],
                        task_info["priority"],
                        msg,
                        task_info["created_at"],
                        task_info["started"],
                        task_info["completed"],
                        task_info["modified"]
                    )
                )

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
            print("Table name contains non-alphanumeric characters or"
                  " is non-existent.")
            self.log.add("_get_task", detail, time.strftime(
                "%Y-%m-%d %H:%M:%S"))

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
                  " cache.")
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

    def _get_table(self, identifier):
        """Returns the table that holds a certain task."""
        db_connection = sqlite3.connect("tasks.db")
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        for table in cursor.fetchall():
            # Get the table name from tuple.
            table_name = table[0]
            matches = self._get_task(identifier, table_name)
            if len(matches) > 0:
                return table[0]
        return None

    def _meets_dependencies(self, dependencies):
        """Returns all incomplete tasks."""
        incomplete_tasks = []
        db_connection = sqlite3.connect("tasks.db")
        cursor = db_connection.cursor()
        for dependency in dependencies:
            cursor.execute(
                "SELECT * FROM Completed WHERE identifier=?",
                (dependency,))
            if not cursor.fetchall():
                incomplete_tasks.append(str(dependency))
        return incomplete_tasks

    def _check_if_exists(self):
        """Tests if the three tables exist."""
        db_connection = sqlite3.connect("tasks.db")
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = cursor.fetchall()
        existing_tables = [table[0] for table in existing_tables]
        return all([table in existing_tables for table in [
            "NotStarted", "WorkingOn", "Completed"]])
