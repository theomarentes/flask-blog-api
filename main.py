import os
import sqlalchemy as sa
from config import app_config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


# register instances of classes as variables
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()


def app_init():
    # create the flask app instance/object. core of the application
    app = Flask(__name__)

    # import dotenv and load the environment variables
    from dotenv import load_dotenv

    load_dotenv()

    # set app configuration to settings in config.py file
    app.config.from_object("config.app_config")

    # create json web token object
    jwt = JWTManager(app)

    # connect to sqlalchemy database
    db.init_app(app)

    # connect schemas with marshmallow
    ma.init_app(app)

    # connect jwt and bcrypt. allows for authentication
    jwt.init_app(app)
    bcrypt.init_app(app)

    # register CLI commands with app instance
    from commands import db_command

    app.register_blueprint(db_command)

    # register controller blueprints
    from controllers import registered_controllers

    for controller in registered_controllers:
        app.register_blueprint(controller)
    
    '''
    # start sqlalchemy engine and inspect db
    db_engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db_inspect = sa.inspect(db_engine)

    # check if blogposts table exists
    if not db_inspect.has_table("blogposts"):
        # drop all tables, create new tables and seed database
        with app.app_context():
            db.drop_all()
            db.create_all()
            from commands import seed_db
            seed_db()
            app.logger.info("Database initialized!")
    else:
        app.logger.info("Database already exists!")
    '''
    
    return app
