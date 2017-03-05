#!/usr/bin/env python3
# Configuration module.
# ===================================

# Built-in modules.
import os
import sys
import stat
import argparse
from shutil import copyfile
from distutils.dir_util import copy_tree
from distutils.errors import DistutilsFileError

# Argument parsing.
parser = argparse.ArgumentParser(prog="tm", description="Task manager"
                                 " configuration")
parser.add_argument("path", help="Source and executable path.")
args = parser.parse_args()

source_directory = os.path.dirname(os.path.realpath(__file__))
to_directory = executable_directory = args.path


def copy_project_files():
    """Copies project tree to the specified to_directory."""
    try:
        copy_tree(source_directory, to_directory)
        print("Project files successfully copied to {}.".format(to_directory))
        return True
    except DistutilsFileError as detail:
        print("Files could not be copied to {}. ".format(to_directory) +
              str(detail))
        return False


def copy_menu():
    """Copies interactive menu to the executable directory."""
    menu_source_path = source_directory + "/menu.py"
    menu_bin_path = executable_directory + "/tm"
    try:
        if not os.path.exists(executable_directory):
            os.makedirs(executable_directory)
        # Create a new file 'tm' in the executable directory.
        copyfile(menu_source_path, menu_bin_path)
        # Make the file executable.
        st = os.stat(menu_bin_path)
        os.chmod(menu_bin_path, st.st_mode | stat.S_IEXEC)
        print("Menu successfully copied to {}.".format(executable_directory))
        return True
    except IOError as detail:
        print("Menu file could not be copied to {}. ".
              format(executable_directory) + str(detail))
        return False


def path_file():
    """Creates a nexus between the executable and this configuration file, for
    importing a whole directory."""
    path = executable_directory + "/lib.py"
    try:
        with open(path, "w") as f:
            f.write("__path__ = ['{}']".format(to_directory))
        return True
    except (OSError, IOError) as detail:
        print(detail)
        return False


if copy_project_files() and copy_menu() and path_file():
    print("Files successfully copied.")
else:
    print("The necessary project files were not successfully copied in their"
          " respective directories due to permission errors. Run the script"
          " again with administrator privileges.")
