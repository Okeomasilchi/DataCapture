from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
import requests as rq
from flask_web import root, app
import jwt
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import datetime


class Regfrom(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=21)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=21)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("Password should be at least 8 characters long")
        if not re.search(r"\d", password.data):
            raise ValidationError("Password should contain at least one digit")
        if not re.search(r"[A-Z]", password.data):
            raise ValidationError(
                "Password should contain at least one uppercase letter"
            )
        if not re.search(r"[a-z]", password.data):
            raise ValidationError(
                "Password should contain at least one lowercase letter"
            )
        if not re.search(r"[!@#$%^&*()\-_=+{};:,<.>]", password.data):
            raise ValidationError(
                "Password should contain at least one special character"
            )

    def validate_email(self, field):
        r = rq.get(f"{root}users/validate", json={"email": field.data})
        if r.status_code == 200:
            email = r.json()["response"]
            if email:
                raise ValidationError(f"{field.data} already in use by another user")


class Loginfrom(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remeber Me")
    submit = SubmitField("Login")

    def validate_email(self, field):
        r = rq.get(f"{root}users/validate", json={"email": field.data})
        if r.status_code == 200:
            email = r.json()["response"]
            if not email:
                raise ValidationError(f"{field.data} not found")


class UpdateAccountFrom(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=21)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=21)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField(
        "Update Profile Image", validators=[FileAllowed(["jpeg", "png", "jpg"])]
    )
    submit = SubmitField("Update")


class ResetEmail(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, field):
        user = None
        r = rq.get(f"{root}users/validate", json={"email": field.data, "data": True})
        if r.status_code == 200:
            user = r.json()[0]
            if "id" not in user:
                user = None
                raise ValidationError(f"{field.data} {r.json()} {r.status_code} not found")
            return user


class ResetPassword(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Change Password")

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("Password should be at least 8 characters long")
        if not re.search(r"\d", password.data):
            raise ValidationError("Password should contain at least one digit")
        if not re.search(r"[A-Z]", password.data):
            raise ValidationError(
                "Password should contain at least one uppercase letter"
            )
        if not re.search(r"[a-z]", password.data):
            raise ValidationError(
                "Password should contain at least one lowercase letter"
            )
        if not re.search(r"[!@#$%^&*()\-_=+{};:,<.>]", password.data):
            raise ValidationError(
                "Password should contain at least one special character"
            )


class Token:
    @staticmethod
    def get(id=None):
        if id is None:
            raise
        current_time = datetime.datetime.now()
        target_time = current_time + datetime.timedelta(minutes=10)
        # Convert expiration time to Unix timestamp
        exp_time = int(target_time.timestamp())
        payload = {
            "id": id,
            "exp": exp_time
        }
        token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm='HS256')
        return token

    @staticmethod
    def validate(token):
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=['HS256'])
            user_id = payload["id"]
            exp_time = payload["exp"]

            current_time = datetime.datetime.now()
            current_time_unix = int(current_time.timestamp())

            if current_time_unix > exp_time:
                # print(f"current_time_unix: {current_time_unix} > exp_time: {exp_time}")
                return None

            return user_id
        except jwt.ExpiredSignatureError as e:
            # print(e, "ExpiredSignatureError")
            return None
        except jwt.DecodeError as e:
            # print(e, "DecodeError")
            return None
        except jwt.InvalidTokenError as e:
            # print(e, "InvalidTokenError")
            return None
        except Exception as e:
            # print(e, "Exception")
            return None
