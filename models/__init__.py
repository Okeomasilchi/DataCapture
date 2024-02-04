#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
from dotenv import load_dotenv

load_dotenv("./.env")

storage_t = getenv("DC_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()
storage.reload()
