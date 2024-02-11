from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
import requests as rq
from flask_web import root


class Regfrom(FlaskForm):
    first_name = StringField('First Name',
                        validators=[DataRequired(), Length(min=2, max=21)])
    last_name = StringField('Last Name',
                        validators=[DataRequired(), Length(min=2, max=21)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        r = rq.get(f"{root}users/validate", json={"email": field.data})
        if r.status_code == 200:    
            email = r.json()['response']
            if email:
                raise ValidationError(f"{field.data} already in use by another user")


class Loginfrom(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
    remember = BooleanField('Remeber Me')
    submit = SubmitField('Login')
    
    def validate_email(self, field):
        r = rq.get(f"{root}users/validate", json={"email": field.data, "data": True})
        if r.status_code == 200:    
            user = r.json()
            if not user:
                raise ValidationError(f"{field.data} not found")




class UpdateAccountFrom(FlaskForm):
    first_name = StringField('First Name',
                        validators=[DataRequired(), Length(min=2, max=21)])
    last_name = StringField('Last Name',
                        validators=[DataRequired(), Length(min=2, max=21)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Image", validators=[FileAllowed(["jpeg", "png", "jpg"])])
    submit = SubmitField('Update')
