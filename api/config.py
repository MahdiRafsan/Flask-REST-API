import os

class Config(object):
    """
    main class with application settings
    """
    BASE = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get("SECRET_KEY") or "restapiusingflask"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE, "database.db")  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class Production(Config):
    """
    settings to be used during production
    """
    pass

class Development(Config):
    """
    settings to be used while developing the app
    """
    DEBUG = True

class Testing(Config):
    """
    settings to be used while testing the app
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config = {"development": Development, "production": Production, "testing": Testing}