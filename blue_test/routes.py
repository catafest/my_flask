from flask import Blueprint, jsonify, request
from flask_login import login_user, current_user, logout_user, login_required

# import forms
from flask import render_template, url_for, flash, redirect, request, abort
from .forms import (RegistrationForm,RequestResetForm, ResetPasswordForm)

# import python for mail
from flask_mail import Message

api = Blueprint('api', __name__)

# root main home page
@api.route("/")
# root to home main function
@api.route("/home")
def home():
    return jsonify({'result' : 'This is main page!'})

@api.route("/register", methods=['GET', 'POST'])
def register():
    # check if the user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Your account has been created!, 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)