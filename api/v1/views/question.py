#!/usr/bin/python3

"""
Models for the routes of the question_views
"""


from flask import abort, request, abort, session, url_for, redirect
from json import dumps as js
from api.v1.views import question_views
from models import storage
from models.question import Question
from models.survey import Survey
from utils.validators import parse_dict, pop_dict, check_keys
from utils.error import log_error


@question_views.route("/question/<survey_id>", methods=["PUT"], strict_slashes=False)
def update_questions(survey_id):
    if not request.is_json:
        return {"error": "Not a JSON"}, 400

    survey = storage.get(Survey, survey_id)

    if not survey:
        abort(404)

    questions = session.pop("question", None)

    if type(questions) is not list:
        return {"error": "Must be in a list"}, 400

    for question in questions:
        if check_keys(question, mode="question"):
            if "id" not in question:
                return {"error": "Missing id"}, 400

            q = storage.get(Question, question["id"])
            if not q:
                abort(404)

            question = pop_dict(
                question, ["id", "__class__", "survey_id", "created_at", "updated_at"]
            )

            if "options" in question:
                question["options"] = js(question["options"])

            for key, value in question.items():
                setattr(q, key, value)

            storage.save()

    return redirect(url_for("survey_views.get_survey_by_id", survey_id=survey_id))


@question_views.route("/question/<survey_id>", methods=["DELETE"], strict_slashes=False)
def delete_question(survey_id):
    if not request.is_json:
        return {"error": "Not a JSON"}, 400

    if not storage.get(Survey, survey_id):
        abort(404)

    questions = request.get_json()["questions"]

    if type(questions) is not list:
        return {"error": "Must be in a list"}, 400

    for id in questions:
        print(id)
        q = storage.get(Question, id)
        if not q:
            abort(404)
        print(q.to_dict())
        if q.id != id:
            return {"error": "Invalid id"}, 400
        storage.delete(q)

    storage.save()

    return js({}), 204
