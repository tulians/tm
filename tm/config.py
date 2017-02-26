#!/usr/bin/env python
# tm - Task management.
# Configuration module.
# Author: Julian Ailan
# ===================================

# Built-in modules.
import os
import sys
import stat
from json import dumps
from shutil import copyfile
from distutils.dir_util import copy_tree
from distutils.errors import DistutilsFileError

home_dir = os.path.expanduser("~")
source_directory = os.path.dirname(os.path.realpath(__file__))
if len(sys.argv) > 1:
    to_directory = sys.argv[1]
    executable_directory = sys.argv[2]
else:
    to_directory = "/opt/tm/"
    executable_directory = home_dir + "/bin/"


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
    """Copies interactive menu to ~/bin."""
    menu_source_path = source_directory + "/menu.py"
    menu_bin_path = executable_directory + "tm"
    try:
        if not os.path.exists(executable_directory):
            os.makedirs(executable_directory)
        # Create a new file 'tm' in the ~/bin directory.
        copyfile(menu_source_path, menu_bin_path)
        # Make the file executable.
        st = os.stat(menu_bin_path)
        os.chmod(menu_bin_path, st.st_mode | stat.S_IEXEC)
        print("Menu successfully copied to ~/bin.")
        return True
    except IOError as detail:
        print("Menu file could not be copied to ~/bin. " + str(detail))
        return False


def path_file():
    """Creates a nexus between the executable and this configuration file, for
    importing a whole directory."""
    path = executable_directory + "lib.py"
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
