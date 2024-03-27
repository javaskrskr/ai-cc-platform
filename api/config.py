from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
print(basedir)
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SESSION_TYPE = environ.get('SESSION_TYPE')
    UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')
    ROOT_PATH = environ.get('ROOT_PATH')
    SESSION_PERMANENT = environ.get('SESSION_PERMANENT')
    PERMANENT_SESSION_LIFETIME = int(environ.get('PERMANENT_SESSION_LIFETIME'))
    DEBUG = environ.get('DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY')
    UPLOAD_EXTENSIONS = ['.mp4', '.mp3', '.m4a']


class DevConfig(Config):
    """Development config."""
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    OPENAI_API_KEY = environ.get('OPENAI_API_KEY')


class ProdConfig(Config):
    """Production config."""
    FLASK_ENV = "production"
    FLASK_DEBUG = False
    OPENAI_API_KEY = environ.get('OPENAI_API_KEY')