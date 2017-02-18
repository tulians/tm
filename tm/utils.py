# tm - Task management.
# Utilities module.
# Author: Julian Ailan
# ===================================

"""Provides a series of methods to simplify operations."""

import re
from string import ascii_letters, punctuation

# Generate a set of characters used for string sanitization.
punctuation_minus = set(punctuation) - set(('.', '_', '-'))
substrings = set(("rm", "&&", "-f", "null", "/dev/null", "2>&1", "-rf"))
illegal = [re.escape(item) for item in (punctuation_minus | substrings)]
illegal_as_str = "|".join(illegal)


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


# TODO: This solution is O(n.m) where n = len(illegal) and m = len(parts).
# Look for a more efficient approach.
def sanitize_string(s):
    operation = (re.split(illegal_as_str, s))[0]
    operation = operation.strip()
    try:
        operation.decode("utf-8")
        return operation
    except UnicodeDecodeError as detail:
        print("UnicodeDecodeError: " + str(detail))
        return False
