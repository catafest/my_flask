from flask import Flask
from flask import render_template, redirect, url_for, session, logging
from flask import render_template_string
from flask import request

from flask import send_file
from io import BytesIO

from flask import flash

import random

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


from flask_wtf import FlaskForm
from wtforms  import FileField, SubmitField
import sqlite3

from forms import AddUser
from my_forms import NormalUser

app = Flask (__name__)

app.config['SECRET_KEY'] = 'abcdefg'
# set SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'server.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email
    '''
    def __rep_(self):
        return '<User %r>' % self.username
    '''
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/users/", methods=['GET'])
def users():
    users = User.query.all()
    #return users_schema.jsonify(users)
    all_users = users_schema.dump(users)
    return jsonify(all_users.data)

@app.route("/users/<id>", methods=['POST'])
def user_post(id):
    user_post = User.query.get(id)
    print(user_post)
    username = request.json['username']
    email = request.json['email']
    user_post.username = username
    user_post.email = email
    db.session.commit()
    return user_schema.jsonify(user_post)

@app.route("/users/<id>", methods=['PUT'])
def user_put(id):
    user_put = User.query.get(id)
    print(user_put)
    username = request.json['username']
    email = request.json['email']
    user_put.username = username
    user_put.email = email
    db.session.commit()
    return user_schema.jsonify(user_put)

@app.route("/users/<id>", methods=['DELETE'])
def user_delete(id):
    user_delete = User.query.get(id)
    print(user_delete)
    db.session.delete(user_delete)
    db.session.commit()
    return user_schema.jsonify(user_delete)

# create a wrarp of localhost

@app.route('/',methods = ['GET','POST'])
def home():
    # test flash message
    out = random.randint(1,10)
    if out in range(1,3):
        flash(str(out),"warning" )
    if out in range(4,6):
        flash("This is a flash test for home.html with result:","success")
    if out in range(7,10):
        flash("This is a flash test for home.html with result:","danger")  
    return render_template("home.html")

@app.route('/about')
def about():
        return 'The about page'
 
class UploadForm(FlaskForm):
    file = FileField()
    submit = SubmitField("Submit")
    download = SubmitField("Download")
    
@app.route('/upload',methods = ['GET','POST'])
def upload():
    form = UploadForm() 
    if request.method == "POST" and form.validate():
        if form.validate_on_submit():
            file_name = form.file.data
            file_database(name = file_name.filename,data = file_name.read())
            print("File {}".format(file_name.filename))
            return render_template("upload.html", form = form)
    return render_template("upload.html", form = form)

def file_database(name,data):
    con=sqlite3.connect("file_upload.db")
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS my_table (name TEXT, data BLOP) """)
    cursor.execute("""INSERT INTO my_table (name , data ) VALUES (?,?) """, (name, data))
    con.commit()
    cursor.close()
    con.close()
    
@app.route('/download', methods=['GET','POST'])
def download():
    form = UploadForm()
    if request.method == "POST":
        con = sqlite3.connect("file_upload.db")
        cursor = con.cursor()
        cur_ex = cursor.execute(""" SELECT * FROM my_table """)
        for i in cur_ex.fetchall():
            name=i[0]
            data=i[1]
            break
        con.commit()
        cursor.close()
        con.close()
        return send_file(BytesIO(data), attachment_filename='test', as_attachment=True)
    return render_template("home.html", form = form)

# fix Exception error , like 404
@app.errorhandler(Exception)
def page_not_found(e):
    flash(e, type(e))  
    return render_template_string('''
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          {% set printed_messages = dict() %}
          {% for category, message in messages %}
            {% if message not in printed_messages %}
              <p style="color: {{category}}">{{message}}</p>
              {% set x = printed_messages.__setitem__(message, "value")  %}
            {% endif %}
          {% endfor %}
        {% endif %}
      {% endwith %}
    ''')

'''
@app.route('/register', methods = ['GET','POST'])
def signup():
    form = NormalUser()
    if form.is_submitted():
        result = request.form
        return render_template('register.html', result = result)
    else:
        print("ok!")
    return render_template('register.html', form = form)
'''
@app.route('/register', methods = ['GET','POST'])
def signup():
    form = NormalUser(request.form)
    if request.method == 'POST' and form.validate():
        uname = form.username.data
        uemail = form.email.data
        flash('You were successfully logged in')
        return redirect(url_for('index'))
    else:
        flash('Error on signup task!')
    return render_template('register.html', form = form)

# the default name main
if __name__ == '__main__':
    app.run(debug=True)