#!/usr/bin/python3
"""model for function of error handling"""
from datetime import datetime
import os

# Access environment variable
error_log_file = os.environ.get('ERROR_LOG_FILE')


def log_error(location="None", args="None", type="None", error="None"):
    # if not location:
    #     raise ValueError("location is required")
    # elif not args:
    #     raise ValueError("args is required")
    # elif not type:
    #     raise ValueError("type is required")
    # elif not error:
    #     raise ValueError("error message is required")

    with open(error_log_file, "a+", encoding="UTF-8") as file:
        file.write(f"{location} --- {args} --- {type} --- {error} --- {datetime.utcnow()}\n")
