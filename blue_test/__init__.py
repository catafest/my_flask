from flask import Flask
from os import environ 


from .extensions import db
from .models import Texts
from .routes import api
from .views import main


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    #app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    #app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(api)

    return app