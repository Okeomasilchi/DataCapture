#!/usr/bin/python3

"""
Model that handles import and export of views
"""


from flask import Blueprint
from flask_cors import CORS

app_views = Blueprint("app_views", __name__)
surveycat_views = Blueprint("surveycat_views", __name__)
question_views = Blueprint("question_views", __name__)
customcategory_views = Blueprint("customcategory_views", __name__)
user_views = Blueprint("user_views", __name__)
response_views = Blueprint("response_views", __name__)
survey_views = Blueprint("survey_views", __name__)

CORS(app_views)
CORS(surveycat_views)
CORS(customcategory_views)
CORS(question_views)
CORS(user_views)
CORS(response_views)
CORS(survey_views)

from api.v1.views.customcategory import *
from api.v1.views.question import *
from api.v1.views.index import *
from api.v1.views.response import *
from api.v1.views.survey import *
from api.v1.views.surveycategory import *
from api.v1.views.users import *
