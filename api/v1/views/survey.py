#!/usr/bin/python3


"""
Models for the routes of the reviews_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import survey_views
import datetime
from models import storage
from models.survey import Survey
from models.user import User
from utils.validators import parse_dict
from utils.error import log_error

@survey_views.route("survey/<survey_id>", methods=["GET"], strict_slashes=False)
def get_survey_by_id(survey_id):
    survey = storage.get(Survey, survey_id)

    if not survey:
        abort(404)

    try:
        return js(survey.to_dict())
    except Exception as e:
        log_error("survey/<survey_id>['GET']", e.args, type(e).__name__, e)
        abort(500)


@survey_views.route("users/survey/<user_id>", methods=["GET"], strict_slashes=False)
def get_survey_by_user_id(user_id):
    user = storage.get(User, user_id)

    if not user:
        abort(404)
    try:
        surveys = user.user_surveys
        return js([survey.to_dict() for survey in surveys])
    except Exception as e:
        log_error("users/survey/<user_id>['GET']", e.args, type(e).__name__, e)
        abort(500)


@survey_views.route("/survey", methods=["POST"], strict_slashes=False)
def create_survey_by_id(survey_id):
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    parse_dict(data,
               ["user_id", "description", "question_type", "title"],
               status_code=400
               )

    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    try:
        instance = Survey(**data)
        instance.save()
        return js(instance.to_dict()), 201
    except Exception as e:
        log_error('/survey["POST"]', e.args, type(e).__name__, e)
        abort(500)