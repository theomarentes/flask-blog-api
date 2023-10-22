import os


class BaseConfig(object):
    # sqlalchemy database uri - required to connect to the database
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # access .env to get "SQLALCHEMY_DATABASE_URI"
        db = os.environ.get("SQLALCHEMY_DATABASE_URI")

        # if database uri is null, return value error
        if db is None:
            raise ValueError("DATABASE_URI Not Found")
        
        return db
    
    # jwt secret key - required to verify tokens
    @property
    def JWT_SECRET_KEY(self):
        # access .env to get JWT_SECRET_KEY
        secret = os.environ.get("JWT_SECRET_KEY")
        return secret


class DevelopmentConfig(BaseConfig):
    DEBUG=True
    

class ProductionConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    TESTING=True


# get "FLASK_ENV" variable from .flaskenv file
env = os.environ.get("FLASK_ENV")

if env == "development":
    app_config = DevelopmentConfig()

elif env == "testing":
    app_config = TestConfig()

else:
    app_config = ProductionConfig()