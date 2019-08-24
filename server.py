from flask import Flask
from flask import render_template
from flask import request
# import forms class
from forms import SignUpForm
from forms import AddUser


from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#migrate 
from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand


app = Flask (__name__)
app.config['SECRET_KEY'] = 'abcdefg'
# set SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'server.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

# create migrate object with db 
migrate = Migrate(app, db)
# create manager 
manager = Manager(app)
# create db command for manager 
manager.add_command('db', MigrateCommand)

# add new columns into database 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    gender = db.Column(db.String(5), unique=True)
    work = db.Column(db.String(33), unique=True)
    city = db.Column(db.String(15), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.gender = gender
        self.work = work
        self.city = city
    '''
    def __rep_(self):
        return '<User %r>' % self.username
    '''
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# create a wrarp of localhost
@app.route('/')
def home():
    return 'Hello world'

@app.route('/about')
def about():
        return 'The about page'
@app.route('/blog')
def blog():
    posts = [{'title':'Title 1', 'author': 'author 1'},{'title': 'Title 2', 'author':'author 2'}]
    return render_template('blog.html', author = 'catafest', sunny=True, posts = posts)
# creaza a regula variabila ( variable rules)
@app.route('/blog/<blog_id>')
def blogpost(blog_id):
    return 'This is the post '+str(blog_id)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result = result)
    else:
        print("ok!")
    return render_template('signup.html', form = form)

@app.route('/adduser', methods = ['POST'])
def adduser():
    form = AddUser()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result = result)
    else:
        #username = request.json['username']
        #email = request.json['email']

        #new_user = User(username, email)
        #db.session.add(new_user)
        #db.session.commit()
        print("ok!")
    #return jsonify(new_user)

    return render_template('adduser.html', form = form)


@app.route("/users/", methods=['GET'])
def users():
    users = User.query.all()
    #return users_schema.jsonify(users)
    all_users = users_schema.dump(users)
    return jsonify(all_users.data)

@app.route("/adduser/<id>", methods=["GET"])
def get_user():
    all_users = User.query.get(id)
    result = users_schema.dump(all_users)
    return jsonify(result.data)

'''
        keywords = Keyword.query.all()
        result = keywords_schema.dump(keywords)
        return jsonify([d['keyword'] for d in result.data])
'''

@app.route("/users/add", methods=['POST'])
def user_add():
    username = request.json['username']
    email = request.json['email']
    new_user = User(username, email)
    db.session.add(new_user)
    db.session.commit() 
    return user_schema.jsonify(new_user)

# the default name main
if __name__ == '__main__':
    manager.run()
    app.run(debug=True)

