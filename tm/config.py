#!/usr/bin/env python

# tm - Task management.
# Configuration module.
# Author: Julian Ailan
# ===================================

# Built-in modules.
import os
import sys
from distutils.dir_util import copy_tree
from distutils.errors import DistutilsFileError

# Path to copy the project data from.
source_directory = os.path.dirname(os.path.realpath(__file__))

path_as_parameter = len(sys.argv) > 1
if not path_as_parameter:
    to_directory = "/opt/tm/"
else:
    to_directory = sys.argv[1]

try:
    copy_tree(source_directory, to_directory)
    print("Files successfully moved to {}.".format(to_directory))
except DistutilsFileError as detail:
    print(detail)
