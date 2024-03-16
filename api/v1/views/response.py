#!/usr/bin/python3


"""
Models for the routes of the response_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import response_views
from models import storage
from models.response import Response
from models.survey import Survey
from utils.validators import parse_dict, check_keys
from utils.error import log_error


@response_views.route("response/<survey_id>", methods=["POST"], strict_slashes=False)
def log_response(survey_id):
    """
    Logs a response for a given survey ID.

    Args:
        survey_id (str): The ID of the survey.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    if not request.is_json:
        abort(400, "Not a JSON")

    if not storage.get(Survey, survey_id):
        abort(404)

    data = request.get_json()

    parse_dict(data, fields=["bio", "answers", "survey_id"], status_code=400)

    if check_keys(data, mode="response"):
        if type(data["answers"]) is not list:
            return {"error": "Answers not list"}, 400

        if survey_id != data["survey_id"]:
            return {"error": "Unidentical survey id's"}, 400

        data["bio"] = js(data["bio"])
        data["answers"] = js(data["answers"])
        res = Response(**data)
        res.save()

        try:
            return js({"id": res.to_dict()[0]["id"]}), 201
        except Exception as e:
            # print(e)
            log_error('response/<survey_id>["POST"]', e.args, type(e).__name__, e)
            abort(500)


@response_views.route("response/<survey_id>", methods=["GET"], strict_slashes=False)
def get_response_by_survey_id(survey_id):
    """
    Retrieves the responses for a given survey ID.

    Args:
        survey_id (str): The ID of the survey.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    survey = storage.get(Survey, survey_id)

    if not survey:
        abort(404)

    responses = survey.responses

    return js([response.to_dict() for response in responses]), 200
