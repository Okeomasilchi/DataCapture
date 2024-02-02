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
        log_error("survey/<survey_id>", e.args, type(e).__name__, e)
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
        log_error("users/survey/<user_id>", e.args, type(e).__name__, e)
        abort(500)



{
    "updated_at": "2024-01-31 14:06:04",
    "user_id": "0fd512fa-8fbb-4f15-b2c0-314f696f4b2f",
    "description": "Description for Survey 5",
    "visibility": true,
    "question_type": "Open-ended",
    "id": "07138bdd-fcc8-4f19-8802-c4aa1f1c10f0",
    "created_at": "2024-01-31 14:06:04",
    "title": "Survey 5 for User 2",
    "expiry_date": "2024-04-24",
    "randomize": false,
    "__class__": "Survey"
}


@survey_views.route("/survey", methods=["POST"], strict_slashes=False)
def create_survey_by_id(survey_id):
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    parse_dict(data, ["email", "password", "first_name", "last_name"],
               status_code=400)
    
    if storage.exist(data["email"]):
        abort(409, "User exists")

    if validate_password(data.get("password", None)):
        data["password"] = md5(data.pop("password", None).encode()).hexdigest()

    try:
        instance = User(**data)
        instance.save()
        return js(instance.to_dict()), 201
    except Exception as e:  # noqa
        abort(500)