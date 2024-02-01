#!/usr/bin/python3

"""
Models for the routes of the question_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import question_views
from models import storage
from models.question import Question


@question_views.route(
    "/states/<state_id>/cities", methods=["GET"], strict_slashes=False
)
def get_city_by_state(state_id):
    """
    Retrieves a list of cities based on a given state ID.
    """

    return js([])
