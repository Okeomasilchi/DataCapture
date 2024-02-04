#!/usr/bin/python3

"""
Models for the routes of the question_views
"""


from flask import abort, request, abort
from json import dumps as js
from api.v1.views import question_views
from models import storage
from models.question import Question
from models.survey import Survey
from utils.validators import parse_dict, pop_dict
from utils.error import log_error


@question_views.route("/question/<survey_id>", methods=["PUT"], strict_slashes=False)
def update_questions(survey_id):
    if not request.is_json:
        return log_error(400, "Not a JSON")
    
    survey = storage.get(Survey, survey_id)
    if not survey:
        abort(404)
    questions = request.get_json()
    
    for question in questions:
        if parse_dict(question, ["id"]):
            q = storage.get(Question, question["id"])
            if not q:
                abort(404)
            q.update(question)
            storage.save()
    

