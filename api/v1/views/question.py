#!/usr/bin/python3

"""
Models for the routes of the question_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import question_views
from models import storage
from models.question import Question
from utils.validators import parse_dict
from utils.error import log_error

@question_views.route(
    "survey/question", methods=["POST"], strict_slashes=False
)
def create_question():
    survey_id = request.args.get("survey_id")
    data = request.args.get("questions")
    
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400
    
    for item in data:
        parse_dict(
            item,
            ["question", "options", "survey_id", "random"],
            status_code=400,
        )
        item["options"] = js(item["options"])

    if type(data["questions"]) is not list:
        return js({"error": "questions must be a list"}), 400

    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    """
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    survey_id = Column(String(60), ForeignKey('surveys.id'), nullable=False)
    random = Column(Boolean, nullable=False)
    """
    
    # {"question": "", "options": "", "survey_id": ""}
    try:
        for que in data:
            que["survey_id"] = survey_id
            question = Question(**que)
            question.save()
    except Exception as e:
        log_error('survey/question["POST"]', e.args, type(e).__name__, e)
        abort(500)

