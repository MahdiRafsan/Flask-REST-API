import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config, config
db = SQLAlchemy()

def create_app(env=None):
    """
    create core application
    :param env: environment used to run the app
    :return: an instance of the app
    """
    app = Flask(__name__)
    
    if env is None:
        app.config.from_object(config[os.getenv("FLASK_ENV", "development")])
    else:
       app.config.from_object(config[env])    
    
    db.init_app(app)
    
    # blueprints
    from .user import user
    from .todo import todo
    
    app.register_blueprint(user)
    app.register_blueprint(todo)

    create_database(app)

    return app

def create_database(app):
    """
    create a database if not already created
    :param app: application instance
    :return: None 
    """

    if not os.path.exists(Config().SQLALCHEMY_DATABASE_URI):
        db.create_all(app=app)