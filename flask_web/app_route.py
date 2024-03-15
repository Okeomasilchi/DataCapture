from flask import render_template, url_for, flash, redirect, request
from flask_web import app, root
from flask_web.form import UpdateAccountFrom
from flask_login import current_user, login_required
import requests as rq
from flask_login import login_required
from utils.algorithm import parse_survey_data


def to_dict(user):
    user_dict = {}

    user_dict["id"] = user.id
    user_dict["first_name"] = user.first_name
    user_dict["last_name"] = user.last_name
    user_dict["email"] = user.email
    user_dict["picture"] = user.picture
    return user_dict


def update():
    form = UpdateAccountFrom()
    if current_user.is_authenticated:
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.picture.data = url_for("static", filename="dpics/okeoma.jpg")
    return form


@app.route("/", methods=["GET"], strict_slashes=False)
def home():

    return render_template(
        "home.html",
        title="Empowering Insights through Interactive Surveys",
        update_account=update(),
    )


@app.route("/app/survey/respond/<survey_id>", methods=["GET"], strict_slashes=False)
def response(survey_id):
    if not survey_id:
        flash("Survey ID not found", "danger")
        return redirect(url_for(request.referrer or "home"))
    r = rq.get(f"{root}survey/{survey_id}")
    if r.status_code != 200:
        flash("Survey not found", "danger")
        return redirect(url_for("home"))
    data = r.json()
    ur = rq.get(f"{root}users/{data['user_id']}")
    if ur.status_code != 200:
        flash("User Survey not found", "danger")
        return redirect(url_for("home"))
    return render_template(
        "response.html",
        data=data,
        user_data=ur.json()[0],
        title="Survey Response",
    )


@app.route("/app/survey/new", methods=["GET"], strict_slashes=False)
@login_required
def create_survey():
    if current_user.is_authenticated:
        return render_template(
            "create_survey.html",
            user_data=to_dict(current_user),
            title="Create Survey",
            update_account=update(),
        )


@app.route("/app/user/surveys", methods=["GET", "POST"], strict_slashes=False)
@login_required
def user_survey():
    if current_user.is_authenticated:
        if request.method == "POST":
            pass
        r = rq.get(f"{root}users/survey/{current_user.id}")
        if r.status_code != 200:
            flash("User not found", "danger")
            return redirect(url_for("home"))
        # print(r.json())
        return render_template(
            "user_surveys.html",
            user_data=to_dict(current_user),
            title="User Survey",
            surveys=r.json(),
            update_account=update(),
        )


@app.route("/app/dashboard/<survey_id>", methods=["GET"], strict_slashes=False)
@login_required
def dashboard(survey_id):
    if current_user.is_authenticated and survey_id:
        r = rq.get(f"{root}dashboard/{survey_id}")
        if r.status_code != 200:
            flash("Survey not found", "danger")
            return redirect(url_for("user_survey" or "home"))
        survey = r.json()
        ur = rq.get(f"{root}users/{survey['user_id']}")
        if ur.status_code != 200:
            flash("User not found", "danger")
        data = ur.json()[0]
        print(data)
        return render_template(
            "Dashboard.html",
            title="Dashboard",
            user_data=data,
            update_account=update(),
            response=parse_survey_data(survey),
            data=survey,
        )
