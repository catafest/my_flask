#import for flask and 
from flask import Flask
#from os import environ

#import python files project
from .extensions import db, login_manager
from .models import Texts
from .routes import api
from .views import main

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    
    #app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    #app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
    #init the app with db 
    db.init_app(app)
    #init login_manager
    login_manager.init_app(app)
    #register both main and api blueprint
    app.register_blueprint(main)
    app.register_blueprint(api)

    return app
