from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, current_user, UserMixin
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from dotenv import load_dotenv
from flask_admin import Admin, BaseView, expose
from flask_web.api import APIClient
import os
import secrets
from PIL import Image
import requests as rq

load_dotenv("./.env")
# http://localhost:5001/app/survey/response/1bb7123c-eea0-41dd-b914-acc0f8e5035a
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
admin = Admin(app, name='DataCapture', template_mode='bootstrap4')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
app.config["REMEMBER_COOKIE_DURATION"] = 14 * 24 * 60 * 60  # 14 days in seconds
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")
mail = Mail(app)

api = APIClient("http://localhost:5000/api/v1/")

class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/analytics_index.html')

class UserView(BaseView):
    @expose('/')
    def user(self):
        # Get the ID from the request parameters
        id_param = request.args.get('id')
        data = {'id': id_param}
        data = rq.get(root + "users/" + id_param)
        info = {}
        
        if data.status_code == 200:
            info = data.json()[0]
            print(info)
            return self.render('admin/user.html', info=info)
        return self.render('admin/user.html', error={"message": "User not found"})

admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
admin.add_view(UserView(name='UserView', endpoint='user'))


# Represents a user in the system.
class User(UserMixin):
    """
    Represents a user in the system.

    Args:
        id (int): The unique identifier of the user.
        first_name (str, optional): The first name of the user. Defaults to None.
        last_name (str, optional): The last name of the user. Defaults to None.
        email (str, optional): The email address of the user. Defaults to None.
        picture (str, optional): The profile picture of the user. Defaults to None.
        **kwargs: Additional attributes that can be set dynamically.

    Attributes:
        id (int): The unique identifier of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        picture (str): The profile picture of the user.

    Methods:
        get(user_id): Static method that returns a User instance based on the given user_id.
    """

    def __init__(
        self, id, first_name=None, last_name=None, email=None, picture=None, **kwargs
    ):
        """
        Initialize a User instance.

        Args:
            id (int): The unique identifier of the user.
            first_name (str, optional): The first name of the user. Defaults to None.
            last_name (str, optional): The last name of the user. Defaults to None.
            email (str, optional): The email address of the user. Defaults to None.
            picture (str, optional): The profile picture of the user. Defaults to None.
            **kwargs: Additional attributes that can be set dynamically.
        """
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
        else:
            self.id = id
            self.first_name = first_name
            self.last_name = last_name
            self.email = email
            self.picture = picture

    @staticmethod
    def get(user_id):
        """
        Static method that returns a User instance based on the given user_id.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            User: The User instance with the specified user_id.
        """
        return User(user_id)


# Saves the profile picture.
def save_pic(form_pic):
    """
    Saves the profile picture.

    Args:
        form_pic (FileStorage): The uploaded profile picture.

    Returns:
        str: The filename of the saved picture.
    """
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    new_file_name = rand_hex + f_ext
    path = os.path.join(app.root_path, "static/dpics", new_file_name)

    size = (125, 125)
    img = Image.open(form_pic)
    img.thumbnail(size)
    img.save(path)

    return new_file_name


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("error_404.html"), 404


from flask_web import auth_routs

