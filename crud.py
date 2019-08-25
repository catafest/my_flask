#from flask import Flask, request, jsonify
from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

from flask import Flask 
from flask import render_template
from forms import AddUser
from flask import request

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
# create a wrarp of localhost
@app.route('/')
def home():
	return 'Hello world'

# endpoint to create new user
@app.route("/adduser", methods=["POST"])
def add_user():
    #
    form = AddUser()
    if form.is_submitted():
        result = request.form
        return render_template('adduser.html', result = result)
    else:
        print("ok!")
        return render_template('signup.html', form = form)
    username = request.json['username']
    email = request.json['email']

    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return new_user

# endpoint to show all users
@app.route("/adduser", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return result.data

# endpoint to get user detail by id
@app.route("/adduser/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.user

# endpoint to update user
@app.route("/adduser/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.user

# endpoint to delete user
@app.route("/adduser/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.user
if __name__ == '__main__':
    app.run()
