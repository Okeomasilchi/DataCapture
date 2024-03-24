from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    IntegerField,
)
from flask_login import current_user
import requests as rq
from flask_web import root, app
import jwt
import re
from flask_wtf import FlaskForm
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    ValidationError,
    Optional,
)
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
    role = SelectField(
        "Role",
        choices=[("user", "User"), ("admin", "Admin"), ("root", "Root")],
        default="user",
    )
    verification_pin = IntegerField("Verification Pin", validators=[Optional()])
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

    def validate_verification_pin(self, verification_pin):
        if self.role.data in ["admin", "root"] and not verification_pin.data:
            raise ValidationError(
                "Verification pin is required for Admin or Root role."
            )
        elif self.role.data in ["admin", "root"] and verification_pin.data != 01234:
            raise ValidationError("Invalid verification pin")


class Loginfrom(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember Me")
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
        # print(r.status_code)
        if r.status_code == 200:
            user = r.json()
            if type(user) is bool:
                if user is False:
                    raise ValidationError()
            # print(r.json())
            if "id" not in user[0]:
                user = None
                raise ValidationError()
            return user[0]


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
    def get(id=None, minutes=10):
        if id is None:
            id = current_user.id
        current_time = datetime.datetime.now()
        target_time = current_time + datetime.timedelta(minutes)
        # Convert expiration time to Unix timestamp
        exp_time = int(target_time.timestamp())
        payload = {"id": id, "exp": exp_time}
        token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
        return token

    @staticmethod
    def validate(token):
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            user_id = payload["id"]
            exp_time = payload["exp"]

            current_time = datetime.datetime.now()
            current_time_unix = int(current_time.timestamp())

            if current_time_unix > exp_time:
                # print(f"current_time_unix: {current_time_unix} > exp_time: {exp_time}")
                return None

            return user_id
        except Exception as e:
            # print(e, "Exception")
            return None
