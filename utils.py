# tasks - Task management.
# Utilities module.
# Author: Julian Ailan
# ===================================

"""Provides a series of methods to simplify operations."""


def numberical_list_from_string(string):
    resulting_list = []
    dont_include = ["[", "]", ","]
    for char in string:
        if char not in dont_include:
            resulting_list.append(int(char))
    return resulting_list


def list_from_string(string):
    resulting_list = []
    list_parts = ["[", "]"]
    for part in list_parts:
        string = string.replace(part, "")
    string = string.replace(" ", "")
    string = string.split(",")
    if string == ['']:
        return []
    for substring in string:
        resulting_list.append(substring.replace("'", ""))
    return resulting_list


def replace_last_comma(string):
    list_of_characters = string.rsplit(",", 1)
    return " and".join(list_of_characters)
