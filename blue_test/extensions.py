#use SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
#use LoginManager
from flask_login import LoginManager
#create login_manager
login_manager = LoginManager()
#create db
db = SQLAlchemy()