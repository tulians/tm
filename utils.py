# tasks - Task management.
# Utilities module.
# Author: Julian Ailan
# ===================================

"""Provides a series of methods to simplify operations."""


def list_from_string(string):
    resulting_list = []
    dont_include = ["[", "]", ","]
    for char in string:
        if char not in dont_include:
            resulting_list.append(int(char))
    return resulting_list


def replace_last_comma(string):
    list_of_characters = string.rsplit(",", 1)
    return " and".join(list_of_characters)
