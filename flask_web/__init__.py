from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin
from models import storage
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from dotenv import load_dotenv
import requests as rq
import os

load_dotenv("./.env")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
bc = Bcrypt(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
app.config["REMEMBER_COOKIE_DURATION"] = 3600
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")
mail = Mail(app)

root = "http://0.0.0.0:5000/api/v1/"

# Define a User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        return User(user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


from flask_web import routs
