# tm - Task management.
# Utilities module.
# Author: Julian Ailan
# ===================================

"""Provides a series of methods to simplify operations."""


def numberical_list_from_string(s):
    resulting_list = []
    dont_include = ["[", "]", ","]
    for char in s:
        if char not in dont_include:
            resulting_list.append(int(char))
    return resulting_list


def list_from_string(s):
    resulting_list = []
    list_parts = ["[", "]"]
    for part in list_parts:
        s = s.replace(part, "")
    s = s.replace(" ", "")
    s = s.split(",")
    if s == ['']:
        return []
    for substring in s:
        resulting_list.append(substring.replace("'", ""))
    return resulting_list


def replace_last_comma(s):
    list_of_characters = s.rsplit(",", 1)
    return " and".join(list_of_characters)
