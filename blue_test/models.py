#imports for user model
from datetime import datetime
from .extensions import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from blue_test import login_manager
from flask_login import UserMixin

# import db from base folder, see dot
from .extensions import db 

#load the user by id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# create the Texts mode
class Texts(db.Model):
    # primary key 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    txt_content = db.Column(db.String(1000))
    
# create the User model
'''
id = id key for user
username = name
email = user email
password = user password

'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"