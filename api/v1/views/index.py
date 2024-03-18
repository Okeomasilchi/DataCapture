#!/usr/bin/python3
"""
Models for the routes of the api's health & stats
"""

from flask import Flask, abort, request
from json import dumps as js
from api.v1.views import app_views
from models import storage
from models.customcategory import CustomCategory
from models.base_model import BaseModel
from models.question import Question
from models.response import Response
from models.surveycategory import SurveyCategory
from models.survey import Survey
from models.user import User
from utils.error import log_error


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def get_status():
    """
    returns a JSON object with the status "OK".
    """
    # abort(404) # undergoing maintenance
    return js({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """
    returns the number of objects stored in different classes.
    """
    return js(
        {
            "customcategory": storage.count(CustomCategory),
            "question": storage.count(Question),
            "response": storage.count(Response),
            "surveycategory": storage.count(SurveyCategory),
            "survey": storage.count(Survey),
            "users": storage.count(User),
        }
    )

