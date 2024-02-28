#!/usr/bin/python3


"""
Models for the routes of the reviews_views
"""


from flask import abort, request, redirect, url_for, session
from json import dumps as js
from api.v1.views import survey_views
from models import storage
from models.survey import Survey
from models.user import User
from models.question import Question
from utils.validators import parse_dict, pop_dict, check_keys, sort_list_of_dicts
from utils.error import log_error
from datetime import datetime

@survey_views.route("survey/<survey_id>", methods=["GET"], strict_slashes=False)
def get_survey_by_id(survey_id):
    """
    Get a survey by its ID.

    Args:
        survey_id (str): The ID of the survey.

    Returns:
        str: JSON representation of the survey.

    Raises:
        404: If the survey is not found.
        500: If there is an internal server error.
    """
    survey = storage.get(Survey, survey_id)

    if not survey:
        abort(404)

    data = survey.to_dict()[0]
    data["questions"] = [question.to_dict()[0] for question in survey.questions]
    try:
        return js(data)
    except Exception as e:
        log_error("survey/<survey_id>['GET']", e.args, type(e).__name__, e)
        abort(500)


@survey_views.route("users/survey/<user_id>", methods=["GET"], strict_slashes=False)
def get_survey_by_user_id(user_id):
    """
    Get surveys by user ID.

    Args:
        user_id (str): The ID of the user.

    Returns:
        str: JSON representation of the surveys.

    Raises:
        404: If the user is not found.
        500: If there is an internal server error.
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)
    try:
        surveys = user.user_surveys
        print([survey.to_dict()[0] for survey in surveys])
        return js(sort_list_of_dicts([survey.to_dict()[0] for survey in surveys], "title")), 200
    except Exception as e:
        log_error("users/survey/<user_id>['GET']", e.args, type(e).__name__, e)
        abort(500)


@survey_views.route("/survey/<survey_id>", methods=["DELETE"], strict_slashes=False)
def delete_survey_by_id(survey_id):
    """
    Delete a survey by its ID.

    Args:
        survey_id (str): The ID of the survey.

    Returns:
        str: Empty JSON response.

    Raises:
        404: If the survey is not found.
        500: If there is an internal server error.
    """
    survey = storage.get(Survey, survey_id)

    if not survey:
        abort(404)
    try:
        survey.delete()
        storage.save()
        return js({}), 204
    except Exception as e:
        log_error("/survey/<survey_id>['DELETE']", e.args, type(e).__name__, e)
        abort(500)

def convert_to_mysql_date(date_string):
    try:
        # Parse the input date string
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        # Format the date as a string that fits the MySQL DATE column format
        mysql_date = date_obj.strftime('%Y-%m-%d')
        return mysql_date
    except ValueError:
        # Handle invalid date strings
        return None

@survey_views.route("/survey", methods=["POST"], strict_slashes=False)
def create_survey_by_id():
    """
    Create a new survey.

    Returns:
        str: JSON representation of the created survey.

    Raises:
        400: If the request is not in JSON format or if required fields are missing.
        404: If the user is not found.
        500: If there is an internal server error.
    """
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    data['expiry_date'] = convert_to_mysql_date(data['expiry_date'])
    parse_dict(
        data,
        ["user_id", "description", "question_type", "title", "questions"],
        status_code=400,
    )

    if not storage.get(User, data["user_id"]):
        return js({"error": "User not found"}), 404

    if type(data["questions"]) is not list:
        return js({"error": "questions must be a list"}), 400

    questions = data["questions"]
    data = pop_dict(data, ["id", "created_at", "updated_at", "questions"])

    
    try:
        survey = Survey(**data)
        survey.save()
        instance = survey.to_dict()
        survey_id = instance[0]['id']
        # print(survey_id)
        for item in questions:
            item["survey_id"] = survey_id
            parse_dict(
                item,
                ["question", "options", "survey_id", "random"],
                status_code=400,
            )
            pop_dict(item, ["id", "created_at", "updated_at"])
            item["options"] = js(item["options"])
            item = Question(**item)
            item.save()
    except Exception as e:
        log_error('/survey["POST"]', e.args, type(e).__name__, e)
        abort(500)
    else:
        return js(survey.to_dict()), 201


@survey_views.route("/survey/<survey_id>", methods=["PUT"], strict_slashes=False)
def update_survey_by_id(survey_id):
    """
    Update a survey by its ID.

    Args:
        survey_id (str): The ID of the survey.

    Returns:
        str: JSON representation of the updated survey.

    Raises:
        400: If the request is not in JSON format or if required fields are missing.
        404: If the survey is not found.
        500: If there is an internal server error.
    """
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    survey = storage.get(Survey, survey_id)
    if not survey:
        abort(404)

    data = request.get_json()

    questions = data.pop("questions", None)
    if questions:
        session["question"] = questions

    data = pop_dict(data, ["__class__", "id", "created_at", "updated_at", "user_id"])

    if check_keys(data, mode="survey"):
        for key, value in data.items():
            setattr(survey, key, value)

        survey.save()

    if questions:
        return redirect(
            url_for("question_views.update_questions", survey_id=survey_id),
            code=307,
        )

    try:
        return redirect(url_for("survey_views.get_survey_by_id", survey_id=survey_id))
    except Exception as e:
        log_error('/survey/<survey_id>["PUT"]', e.args, type(e).__name__, e)
