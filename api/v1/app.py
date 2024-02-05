#!/usr/bin/python3

"""
default model for the flask app instance
"""


import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from json import dumps as js
from api.v1.views import customcategory_views
from api.v1.views import app_views
from api.v1.views import question_views
from api.v1.views import response_views
from api.v1.views import survey_views
from api.v1.views import surveycat_views
from api.v1.views import user_views
from models import storage

load_dotenv("./.env")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

@app.after_request
def apply_caching(response):
    """
    setting the "Content-Type" header to
    "application/json".
    """
    response.headers["Content-Type"] = "application/json"

    return response


cors = CORS(app, resources={r"/api/v1/*": {"origins": "http://0.0.0.0"}})

url_prefix = "/api/v1"


app.register_blueprint(customcategory_views, url_prefix=url_prefix)
app.register_blueprint(app_views, url_prefix=url_prefix)
app.register_blueprint(question_views, url_prefix=url_prefix)
app.register_blueprint(response_views, url_prefix=url_prefix)
app.register_blueprint(surveycat_views, url_prefix=url_prefix)
app.register_blueprint(user_views, url_prefix=url_prefix)
app.register_blueprint(survey_views, url_prefix=url_prefix)


@app.teardown_appcontext
def close(exc):
    """
    used to close a storage object.
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    returns a JSON response with an
    error message and a status code of 404.

    Args:
      error: The error parameter is the error
      message that will be returned in the response.

    Returns:
      a JSON response error message "Not found
      and a status code of 404.
    """
    return js({"error": "Not found"}), 404


@app.errorhandler(500)
def error_500(error):
    """
    returns a JSON response with an
    error message and a status code of 500.
    """
    return js({"error": "Internal Server Error"}), 500


@app.errorhandler(400)
def error_400(error):
    """
    returns a JSON response with an
    error message and a status code of 400.
    """
    return js({"error": f"{error}".split(":")[1]}), 400


@app.errorhandler(405)
def error_400(error):
    """
    returns a JSON response with an
    error message and a status code of 400.
    """
    return js({"error": "Method Not Allowed"}), 405


@app.errorhandler(409)
def error_400(error):
    """
    returns a JSON response with an
    error message and a status code of 409.
    """
    return js({"error": f"{error}".split(":")[1]}), 409


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    app.run(host=host, port=port, debug=True, threaded=True)
