#!/usr/bin/python3


"""
Models for the routes of the reviews_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import survey_views
from models import storage
from models.survey import Survey


@survey_views.route("places/<review_id>/reviews", methods=["GET"], strict_slashes=False)
def get_review_by_place(review_id):
    return js([])
