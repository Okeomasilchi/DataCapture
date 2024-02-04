#!/usr/bin/python3


"""
Models for the routes of the reviews_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import survey_views
from models import storage
from models.survey import Survey
from models.user import User
from models.question import Question
from utils.validators import parse_dict, pop_dict
from utils.error import log_error


@survey_views.route("survey/<survey_id>", methods=["GET"], strict_slashes=False)
def get_survey_by_id(survey_id):
    survey = storage.get(Survey, survey_id)

    if not survey:
        abort(404)

    try:
        data = survey.to_dict()
        data["questions"] = [question.to_dict() for question in survey.questions]
        return js(data)
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


@survey_views.route("/survey/<survey_id>", methods=["DELETE"], strict_slashes=False)
def delete_survey_by_id(survey_id):
    survey = storage.get(Survey, survey_id)

    if not survey:
        abort(404)
    try:
        survey.delete()
        storage.save()
        return js({}), 204
    except Exception as e:
        log_error("survey/<user_id>['DELETE']", e.args, type(e).__name__, e)
        abort(500)


@survey_views.route("/survey", methods=["POST"], strict_slashes=False)
def create_survey_by_id():
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
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
        survey_id = survey.to_dict()
        survey_id = survey_id["id"]
        print(survey_id)
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


# {
#     "created_at": "2024-01-31 14:05:49",
#     "id": "1bb7123c-eea0-41dd-b914-acc0f8e5035a",
#     "title": "teching and teching techniques",
#     "expiry_date": "2024-03-12",
#     "randomize": true,
#     "updated_at": "2024-01-31 14:05:49",
#     "user_id": "08c2c669-15b5-4e0a-951b-92d17c27a370",
#     "description": "omoku",
#     "visibility": false,
#     "question_type": "user prefrence",
#     "questions": [
#         {
#             "question": "what is your name",
#             "options": [
#                 "okeoma",
#                 "silachi",
#                 "here"
#             ],
#             "random": true
#         },
#         {
#             "question": "who is obu?",
#             "options": [
#                 "a girl",
#                 "a boy",
#                 "a lady",
#                 "none"
#             ],
#             "random": true
#         }
#     ]
# }
