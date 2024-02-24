#!/usr/bin/python3

from flask import abort, request
import json as js
import re

def sort_list_of_dicts(list_of_dicts, key, reverse=False):
    """Sorts a list of dictionaries based on the specified key.

    Args:
        list_of_dicts: The list of dictionaries to be sorted.
        key: The key to use for sorting.
        reverse: If True, sorts in descending order. Defaults to False (ascending).

    Returns:
        The sorted list of dictionaries.
    """

    sorted_list = sorted(list_of_dicts, key=lambda item: item[key], reverse=reverse)
    return sorted_list



def parse_dict(args, fields=[], message=[], status_code=0):
    """
    parses a dictionary to ensure that it only contains
    the specified fields.
    """
    if status_code == 0:
        raise ValueError("Status code not specified")
    elif not fields:
        raise ValueError("Fields not specified")
    elif not 100 <= status_code <= 599:
        raise ValueError("Invalid status code")

    for field in fields:
        if field not in args and not message:
            abort(status_code, "Missing {}".format(field))
        if field not in args and message:
            abort(status_code, message)

    return True


def validate_password(password):
    """
    Validates if a password is strong enough.
    Returns an error code and message if the password is weak.
    """
    # if len(password) < 8:
    #     abort(400, "Password should be at least 8 characters long")
    # if not re.search(r"\d", password):
    #     abort(400, "Password should contain at least one digit")
    # if not re.search(r"[A-Z]", password):
    #     abort(400, "Password should contain at least one uppercase letter")
    # if not re.search(r"[a-z]", password):
    #     abort(400, "Password should contain at least one lowercase letter")
    # if not re.search(r"[!@#$%^&*()\-_=+{};:,<.>]", password):
    #     abort(400, "Password should contain at least one special character")

    return True


def pop_dict(data=dict, values=list):
    if not data or type(data) is not dict:
        raise ValueError("data must be a non empty dictionary")
    elif not values or type(values) is not list:
        raise ValueError("values must be a non empty list")

    for value in values:
        data.pop(value, None)

    return data


def check_keys(dictionary, mode="None"):
    """
    Check if any key from the list is present in the dictionary.

    Parameters:
    - dictionary: The dictionary to check.
    - keys_to_check: A list of keys to check.

    Returns:
    - True if any key is present, False otherwise.
    """
    if mode == "None":
        raise ValueError("Mode not specified")

    survey = ["title", "description", "expiry_date", "visibility", "randomize", "question_type"]
    question = ["question", "options", "random"]
    user = ["password"]
    response = ["bio", "answers", "survey_id"]

    if mode == "survey":
        keys_to_check = survey
    elif mode == "question":
        keys_to_check = question
    elif mode == "user":
        keys_to_check = user
    elif mode == "response":
        keys_to_check = response
    else:
        raise ValueError("Invalid mode")

    return any(key in dictionary for key in keys_to_check)
