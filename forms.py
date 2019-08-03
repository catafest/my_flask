from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
class SignUpForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Sign up')

class AddUser(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    email = StringField('Email')
    submit = SubmitField('Sign up')


