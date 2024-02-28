#!/usr/bin/python3

from flask import render_template, url_for, flash, redirect, request, abort, session
from flask_web import app, root, User, mail, save_pic
from hashlib import md5
from datetime import datetime
from flask_web.form import (
    Regfrom,
    Loginfrom,
    UpdateAccountFrom,
    ResetEmail,
    ResetPassword,
    Token,
)
from flask_login import login_user, current_user, logout_user, login_required
import requests as rq
from flask_login import login_required
from flask_mail import Message as msg


def to_dict(user):
    user_dict = {}

    user_dict["id"] = user.id
    user_dict["first_name"] = user.first_name
    user_dict["last_name"] = user.last_name
    user_dict["email"] = user.email
    return user_dict


def update():
    form = UpdateAccountFrom()
    if current_user.is_authenticated:
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return form


data = [
    {
        "question": "Do you agree with the statement?",
        "a": 25,
        "b": 50,
        "c": 75,
        "d": 100,
    },
    {
        "question": "What is your favorite color?",
        "a": 20,
        "b": 30,
        "c": 40,
        "d": 50,
    },
    {
        "question": "What is the capital of France?",
        "a": 10,
        "b": 20,
        "c": 70,
        "d": 80,
    },
    {
        "question": "What is the meaning of life?",
        "a": 5,
        "b": 10,
        "c": 15,
        "d": 85,
    },
    {
        "question": "What is your favorite food?",
        "a": 30,
        "b": 40,
        "c": 50,
        "d": 60,
    },
    {
        "question": "What is your dream job?",
        "a": 25,
        "b": 35,
        "c": 45,
        "d": 55,
    },
    {
        "question": "What is your biggest fear?",
        "a": 15,
        "b": 25,
        "c": 35,
        "d": 65,
    },
    {
        "question": "What is your favorite movie?",
        "a": 40,
        "b": 50,
        "c": 60,
        "d": 70,
    },
    {
        "question": "What is your favorite book?",
        "a": 20,
        "b": 30,
        "c": 40,
        "d": 55,
    },
    {
        "question": "What is your favorite sport?",
        "a": 35,
        "b": 45,
        "c": 55,
        "d": 65,
    },
    {
        "question": "What is your favorite hobby?",
        "a": 25,
        "b": 35,
        "c": 45,
        "d": 55,
    },
    {
        "question": "What is your favorite place to visit?",
        "a": 40,
        "b": 50,
        "c": 60,
        "d": 70,
    },
    {
        "question": "What is your favorite animal?",
        "a": 30,
        "b": 40,
        "c": 50,
        "d": 60,
    },
    {
        "question": "What is your favorite song?",
        "a": 20,
        "b": 30,
        "c": 40,
        "d": 50,
    },
    {
        "question": "What is your favorite season?",
        "a": 35,
        "b": 45,
        "c": 55,
        "d": 65,
    },
]


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Regfrom()
    data = {}  # Initialize the 'data' variable
    if form.validate_on_submit():
        password = form.password.data
        if password is not None:
            hp = md5(password.encode()).hexdigest()
            data = {
                "email": form.email.data,
                "password": hp,
                "first_name": form.first_name.data,
                "last_name": form.last_name.data,
            }
            r = rq.post(f"{root}users", json=data)
            if r.status_code != 201:
                flash("Account Creation Failed", "danger")
                return redirect(url_for("register"))
            user = r.json()[0]
            flash(f"Account Created for {user['first_name']}!", "success")
            return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Loginfrom()
    if form.validate_on_submit():
        hp = md5(form.password.data.encode()).hexdigest()
        data = {
            "email": form.email.data,
            "password": hp,
        }
        r = rq.post(f"{root}users/login", json=data)
        if r.status_code == 200:
            user_data = r.json()
            user = User(**user_data)
            login_user(user, remember=form.remember.data)
            flash(f"Welcome Back {user_data['first_name']}", "success")
            session["user_id"] = user_data["id"]
            user_data["root"] = root
            session["user_data"] = user_data
            return redirect(url_for("user_survey"))
        else:
            flash("Login Unsuccessful, Please check Credentials", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", methods=["GET"], strict_slashes=False)
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("login"))


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    image_file = url_for("static", filename="dpics/okeoma.jpg")
    return render_template(
        "home.html",
        title="Empowering Insights through Interactive Surveys",
        image_file=image_file,
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
    data=r.json()
    ur = rq.get(f"{root}users/{data['user_id']}")
    if ur.status_code != 200:
        flash("User Survey not found", "danger")
        return redirect(url_for("home"))
    return render_template(
        "response.html",
        data=data,
        user_data=ur.json()[0],
        title="Survey Response",
        update_account=update(),
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
        print(r.json())
        return render_template(
            "user_surveys.html",
            user_data=to_dict(current_user),
            title="User Survey",
            surveys=r.json(),
            update_account=update(),
        )


@app.route("/app/user/dashboard", methods=["GET", "POST"], strict_slashes=False)
@login_required
def dashboard():
    if current_user.is_authenticated:
        return render_template(
            "Dashboard.html",
            title="Dashboard",
            user_data=to_dict(current_user),
            data=data,
            update_account=update(),
        )


@app.route("/reset_password", methods=["GET", "POST"], strict_slashes=False)
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = ResetEmail()
    if request.method == "POST":
        if form.validate_on_submit():
            user = form.validate_email(form.email)
            if user and "id" in user:
                send_reset_email(user)
                flash(
                    "An email has been sent with instructions to reset your password",
                    "info",
                )
                flash(
                    "An email has been sent with instructions to reset your password",
                    "info",
                )
                return redirect(url_for("login"))
            else:
                flash("Email not found", "danger")
    return render_template("reset_request.html", title="Reset Request", form=form)


def send_reset_email(user):
    token = Token.get(id=user["id"])
    token = Token.get(id=user["id"])
    mg = msg(
        "Password Reset Request", sender="noreply@demo.com", recipients=[user["email"]]
    )
    mg.html = f"""<h1 class="text-center text-justify bg-success text-white">DataCapture</h1>
<p>To reset your password, visit the following link:</p>
<p><a href="{url_for('reset_token', token=token, _external=True)}">Reset Password</a></p>
<p>If you did not make this request then simply ignore this email and no changes will be made.</p>
<footer>
    <p>&copy; {datetime.now().year} DataCapture. All rights reserved.</p>
    <p>Corporate Symbol</p>
</footer>
"""
    mail.send(mg)


@app.route("/reset_password/<token>", methods=["GET", "POST"], strict_slashes=False)
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = Token.validate(token)
    if user is None:
        flash(f"That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPassword()
    if form.validate_on_submit():
        password = form.password.data
        if password is not None:
            hp = md5(password.encode()).hexdigest()
            data = {
                "password": hp
            }
            r = rq.put(f"{root}users/{user}", json=data)
            if r.status_code != 200:
                flash("Invalid or expired token", "warning")
                return redirect(url_for("reset_request"))
            flash(
                "Your password has been updated! You are now able to log in", "success"
            )
            flash(
                "Your password has been updated! You are now able to log in", "success"
            )
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form=form)


@app.route("/account", methods=["POST"], strict_slashes=False)
@login_required
def account():
    form = UpdateAccountFrom()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pic(form.picture.data)
            if picture_file != current_user.picture:
                current_user.picture = picture_file

        if form.first_name.data != current_user.first_name:
            current_user.first_name = form.first_name.data

        if form.last_name.data != current_user.last_name:
            current_user.last_name = form.last_name.data

        if form.email.data != current_user.email:
            current_user.email = form.email.data

        r = rq.put(
            f"{root}users/{current_user.id}", json=to_dict(current_user)
        )
        if r.status_code == 200:
            flash("Your account has been updated!", "success")
        else:
            flash("Failed to update your account", "danger")
        return redirect(request.referrer or url_for("home"))
