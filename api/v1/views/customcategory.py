#!/usr/bin/python3

"""
Models for the routes of the customcategory_views
"""

from flask import abort, request
from json import dumps as js
from api.v1.views import customcategory_views
from models import storage
from models.customcategory import CustomCategory


@customcategory_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_custom_categories():
    """
    Retrieves all amenities from storage and returns
    them as a list of dictionaries.

    Returns:
      a JavaScript array of dictionaries.
    """
    amenities = storage.all(CustomCategory).values()
    return js([])
