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
    gender = StringField('Gender')
    work = StringField('Work')
    city = StringField('City')
    submit = SubmitField('Sign up')


