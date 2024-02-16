#!/usr/bin/python3

from flask import render_template, url_for, flash, redirect, request, abort, session
from flask_web import app, root, User, mail
import secrets
from hashlib import md5
import os
from PIL import Image
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
            user = User(user_data["id"])
            login_user(user, remember=form.remember.data)
            flash(f"Welcome Back {user_data['first_name']}", "success")
            session["user_id"] = user_data["id"]
            user_data["root"] = root
            session["user_data"] = user_data
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful, Please check Credentials", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", methods=["GET"], strict_slashes=False)
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/", methods=["GET"], strict_slashes=False)
@login_required
def home():
    if current_user.is_authenticated:
        user_id = session["user_id"]
        r = rq.get(f"{root}users/{user_id}")
        user = r.json()[0]
        form = UpdateAccountFrom()
        image_file = url_for("static", filename="dpics/okeoma.jpg")
        if user_id:
            if r.status_code == 200:
                return render_template(
                    "home.html",
                    user=user,
                    user_data=session.get("user_data"),
                    image_file=image_file,
                    form=form,
                )
        else:
            flash("User ID not found in session.", "danger")
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route("/app/create_survey", methods=["GET"], strict_slashes=False)
@login_required
def create_survey():
    if current_user.is_authenticated:
        return render_template(
            "create_survey.html",
            user_data=session.get("user_data"),
            title="Create Survey",
        )



@app.route("/reset_password", methods=["GET", "POST"], strict_slashes=False)
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = ResetEmail()
    if request.method == "POST":
        user = form.validate_on_submit()
        if user and "id" in user:
            send_reset_email(user)
            flash("An email has been sent with instructions to reset your password", "info")
            return redirect(url_for("login"))
        else:
            flash("Email not found", "danger")
    return render_template("reset_request.html", title="Reset Request", form=form)


def send_reset_email(user):
    token = Token.get(id=user['id'], expires_sec=1800)
    msg = msg(
        "Password Reset Request",
        sender="noreply@demo.com",
        recipients=[user['email']])
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
"""

@app.route("/reset_password/<token>", methods=["GET", "POST"], strict_slashes=False)
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = Token.validate(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPassword()
    if form.validate_on_submit():
        password = form.password.data
        if password is not None:
            hp = md5(password.encode()).hexdigest()
            data = {
                "password": hp,
                }
            r = rq.put(f"{root}users/{user}", json=data)
            if r.status_code != 200:
                flash("Invalid or expired token", "warning")
                return redirect(url_for("reset_request"))
            flash("Your password has been updated! You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form=form)


def save_pic(form_pic):
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    new_file_name = rand_hex + f_ext
    path = os.path.join(app.root_path, "static/dpics", new_file_name)

    size = (125, 125)
    img = Image.open(form_pic)
    img.thumbnail(size)
    img.save(path)

    return new_file_name
