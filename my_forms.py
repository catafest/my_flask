from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email
from wtforms import validators
from passlib.hash import sha256_crypt

class NormalUser(FlaskForm):
    username = StringField('Username', [InputRequired("Please enter your name."),validators.Length(min=1, max=30)])
    email = StringField('Email', [InputRequired("Please enter your email address."), validators.Email()])
    submit = SubmitField('Sign up')