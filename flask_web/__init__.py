from flask import Flask
from flask_login import LoginManager, current_user, UserMixin
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from dotenv import load_dotenv
import os
import secrets
from PIL import Image

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


class User(UserMixin):
    def __init__(
        self, id, first_name=None, last_name=None, email=None, picture=None, **kwargs
    ):
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
        return User(user_id)

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


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


from flask_web import routs
