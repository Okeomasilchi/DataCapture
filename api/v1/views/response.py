#!/usr/bin/python3


"""
Models for the routes of the response_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import response_views
from models import storage
from models.response import Response


@response_views.route("cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_place_by_city(city_id):
    return js([])
