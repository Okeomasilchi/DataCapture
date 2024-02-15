from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
import requests as rq
from flask_web import root
from itsdangerous import TimeedJSONWebSignatureSerializer as Sz

import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


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
        r = rq.get(f"{root}users/validate", json={"email": field.data, "data": True})
        if r.status_code == 200:
            user = r.json()
            if not user:
                raise ValidationError(f"{field.data} not found")
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
        r = rq.get(f"{root}users/validate", json={"email": field.data, "data": True})
        if r.status_code == 200:
            user = r.json()
            if not user:
                raise ValidationError(f"{field.data} not found")
        raise ValidationError(f"{field.data} not found")


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
    def get(expiration=1800, id=None):
        if id is None:
            id = current_user.id
        s = Sz(current_user.secret, expiration)
        return s.dumps({"id": id}).decode("utf-8")

    @staticmethod
    def validate(token):
        s = Sz(current_user.secret)
        try:
            user_id = s.loads(token)["id"]
        except Exception as e:
            return None
        return user_id
