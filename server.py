from flask import Flask
from flask import render_template
from flask import request
# import forms class
from forms import SignUpForm
from forms import AddUser


#from flask import jsonify
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
    password = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    gender = db.Column(db.String(5), unique=True)
    work = db.Column(db.String(33), unique=True)
    city = db.Column(db.String(15), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.password = password
        self.email = email
        self.gender = gender
        self.work = work
        self.city = city
    # add 27 aug 
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.email}')"
    
#this is a UserSchema for User model
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

#home pages routes

# create a wrarp of localhost
@app.route('/')
def home():
    return render_template('home.html')

# open about.html page 
@app.route('/about')
def about():
    return render_template('about.html')

#blog pages routes

# open blog.html page 
@app.route('/blog')
def blog():
    posts = [{'title':'Title 1', 'author': 'author 1'},{'title': 'Title 2', 'author':'author 2'}]
    return render_template('blog.html', author = 'catafest', sunny=True, posts = posts)
# creaza a regula variabila ( variable rules)

# open blog.html with id
@app.route('/blog/<blog_id>')
def blogpost(blog_id):
    return 'This is the post '+str(blog_id)


#authentication pages routes

# open signup.html
@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result = result)
    else:
        print("ok!")
    return render_template('signup.html', form = form)

# using request:URLparameters./s, form and json 

# request using the URL parameter :
# http://127.0.0.1:5000/url_parameter?my_parameter=my_value
# the result will be: The my_parameter is: my_value
@app.route("/url_parameter")
def url_parameter():
    my_parameter = request.args.get('my_parameter')
    return '<h1>The my_parameter is: {}</h1>'.format(my_parameter)
# request using the URL many parameters :
# http://127.0.0.1:5000/url_parameters?my_p1=val1&my_p2=val2
# the result will be: The my_p1 is: val1
# The my_p2 is: val2
# Use both my_p1 and my_p2 also you get an error like this:
# The browser (or proxy) sent a request that this server could not understand.
@app.route("/url_parameters")
def url_parameters():
    my_p1 = request.args.get('my_p1')
    my_p2 = request.args['my_p2']
    return '''<h1>The my_p1 is: {}</h1>
<h1>The my_p2 is: {}</h1>
'''.format(my_p1,my_p2)
 # request with HTML source code in python area
@app.route("/request_with_form", methods=['POST','GET'])
def request_with_form():
    if request.method == 'POST':
         # in this case I used request.form.get
        my_parameter = request.form.get("my_parameter")
        return '<h1>The parameter my_parameter is: {}</h1>'.format(my_parameter)
    return '''<form action="" method="POST">
Input of my_parameter <input type="text" name="my_parameter">
<input type="submit">
</form>'''
@app.route("/request_with_json", methods=['POST','GET'])
def request_with_json():
    import requests
    res = requests.post('http://localhost:5000/request_with_json', json={"my_parameter":"my_value"})
    if res.ok:
        return res
    
# 

# open adduser.html
@app.route('/adduser', methods = ['GET','POST'])
def adduser():
    form = AddUser()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result = result)
    else:
        username = request.json('username')
        password = request.json['password']
        email = request.json['email']
        gender = request.json['gender']
        work = request.json['work']
        city = request.json['city']
        new_user = User(username, password, email, gender, work, city)
        db.session.add(new_user)
        db.session.commit()
        return render_template('adduser.html', form = form)
    return render_template('adduser.html', form = form)

@app.route('/register', methods = ['GET','POST'])
def register():
    form = AddUser(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.username.data
        email = form.username.data
        gender = form.username.data
        work = form.username.data
        city = form.username.data
        new_user = User(username, password, email, gender, work, city)
        db.session.add(new_user)
        db.session.commit()
        return render_template('about.html')
    else:
        return render_template('adduser.html', form = form)


@app.route("/users", methods=['GET'])
def users():
    users = User.query.all()
    result =  users_schema(users)
    #result = users_schema.dump(users)
    return render_template('user.html', result = result)

@app.route("/allusers",methods = ['GET'])
def allusers():
    users= User.query.all()
    allusers=[]
    for user in users:
        result=allusers.append({'username': user.username})
    return render_template('user.html', result = result)

@app.route("/adduser/<id>", methods=["GET"])
def get_user():
    all_users = User.query.get(id)
    result = users_schema.dump(all_users)
    return result.data

'''
        keywords = Keyword.query.all()
        result = keywords_schema.dump(keywords)
        return [d['keyword'] for d in result.data]
'''

@app.route("/users/add", methods=['POST'])
def user_add():
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']
    new_user = User(username, email)
    db.session.add(new_user)
    db.session.commit() 
    return user_schema.new_user

# the default name main
if __name__ == '__main__':
    manager.run()
    app.run(debug=True)

