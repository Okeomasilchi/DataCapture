#!/usr/bin/python3

"""
Models for the routes of the question_views
"""


from flask import abort, request, g
from json import dumps as js
from api.v1.views import question_views
from models import storage
from models.question import Question
from models.survey import Survey
from utils.validators import parse_dict
from utils.error import log_error


@question_views.route("survey/question", methods=["POST"], strict_slashes=False)
def create_question():
    survey_id = getattr(g, 'survey_id', None)
    data = getattr(g, 'questions', None)
    print(survey_id, data)
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    for item in data:
        parse_dict(
            item,
            ["question", "options", "survey_id", "random"],
            status_code=400,
        )
        item["options"] = js(item["options"])

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
    # [
    #     {
    #         "question": "What is your favorite color?",
    #         "options": ["Red", "Blue", "Green"],
    #         "random": True
    #     },
    #     {
    #         "question": "How often do you exercise?",
    #         "options": ["Every day", "Once a week", "Rarely"],
    #         "random": False
    #     },
    #     {
    #         "question": "Do you prefer cats or dogs?",
    #         "options": ["Cats", "Dogs"],
    #         "random": True
    #     },
    # ]
    try:
        for que in data:
            que["survey_id"] = survey_id
            question = Question(**que)
            question.save()
            
        survey = storage.get(Survey, survey_id)
        return js(survey.to_dict()), 201
    except Exception as e:
        log_error('survey/question["POST"]', e.args, type(e).__name__, e)
        abort(500)
