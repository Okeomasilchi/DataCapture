#!/usr/bin/python3

from flask import render_template, url_for, flash, redirect, request, abort, session
from flask_web import app, root, User
import secrets
from hashlib import md5
import os
from PIL import Image
from flask_web.form import Regfrom, Loginfrom, UpdateAccountFrom
from flask_login import login_user, current_user, logout_user, login_required
import requests as rq


# @app.route("/login", methods=["GET", "POST"], strict_slashes=False)
# def login():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         user_data = storage.exist(email, data=True)
#         if user_data:
#             user = User(user_data["id"])
#             login_user(user)
#             flash("Login successful!", "success")
#             session["user_id"] = user_data["id"]  # Store user_id in session
#             return redirect(url_for("home"))
#         else:
#             flash("Invalid email or password", "danger")
#             return redirect(url_for("login"))

#     return render_template("login.html")


# @app.route("/logout", methods=["GET"], strict_slashes=False)
# def logout():
#     logout_user()
#     session.pop("user_id", None)  # Remove user_id from session
#     flash("You have been logged out.", "success")
#     return redirect(url_for("login"))


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
            print(r.status_code, r.json())
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
        user_data = r.json()
        if r.status_code == 200:
            user = User(user_data["id"])
            login_user(user, remember=form.remember.data)
            flash(f"Welcome Back {user_data['first_name']}", "success")
            session["user_id"] = user_data["id"]
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful, Please check Credentials", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    if current_user.is_authenticated:
        user_id = session["user_id"]  # Retrieve user_id from session
        r = rq.get(f"{root}users/{user_id}")
        user = r.json()[0]
        print(r.json())
        form = UpdateAccountFrom()
        image_file = url_for("static", filename="dpics/okeoma.jpg")
        if user_id:
            if r.status_code == 200:
                form.first_name.data = user["first_name"]
                form.last_name.data = user["last_name"]
                form.email.data = user["email"]
                return render_template("home.html", user=user, image_file=image_file, form=form)
        else:
            flash("User ID not found in session.", "danger")
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


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


@app.route("/account", methods=["POST"])
@login_required
def account():
    form = UpdateAccountFrom()
    # if form.validate_on_submit():
    #     old_img = None
    #     if form.picture.data:
    #         old_img = current_user.image_file
    #         pic = save_pic(form.picture.data)
    #         current_user.image_file = pic
    #     current_user.username = form.username.data
    #     current_user.email = form.email.data
    #     db.session.commit()
    #     if old_img and old_img != "default.jpg":
    #         path = os.path.join(app.root_path, "static/dpics", old_img)
    #         if os.path.exists(path):
    #             os.remove(path)
    #     flash("Account Info Updated", "success")
    #     return redirect(url_for("account"))
    # elif request.method == "GET":
    #     form.username.data = current_user.username
    #     form.email.data = current_user.email
    image_file = url_for("static", filename="dpics/okeoma.jpg")
    return render_template("account.html", title="Account",
                           image_file=image_file, form=form)
