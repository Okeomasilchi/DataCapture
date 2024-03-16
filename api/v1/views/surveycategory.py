#!/usr/bin/python3

"""
Models for the routes of the surveycat_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import surveycat_views
from models import storage
from models.surveycategory import SurveyCategory


@surveycat_views.route("/states", methods=["POST"], strict_slashes=False)
def create_new_state():
    abort(404)
