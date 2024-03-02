#!/usr/bin/python3

from flask import render_template, url_for, flash, redirect, request, session
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
                try:
                    send_reset_email(user)
                except Exception as e:
                    flash("There was a problem sending the email. Please try again soon", "Warning")
                else:
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
    mg.html = f"""<h1 style="position: fixed; top: 0; width: 50%; text-align: center; color: #28a745;">DataCapture</h1>
<p>To reset your password, visit the following link:</p>
<p><a style="display: inline-block; padding: 10px 20px; margin: 10px 0; color: #fff; background-color: #007bff; border: none; border-radius: 5px; text-decoration: none;
        cursor: pointer; background-color: #009c5b;" href="{url_for('reset_token', token=token, _external=True)}">Reset Password</a></p>
<p>If you did not make this request then simply ignore this email and no changes will be made.</p>
<footer style="margin-top: 50px; text-align: center; border-top: 1px solid #000; font-size: 14px; color: #777;">
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
        return redirect(request.referrer or url_for("user_survey"))

from flask_web import app_route
""" error pages """

# @app.errorhandler(500)
# def internal_server_error(error):
#     return render_template('500.html'), 500

