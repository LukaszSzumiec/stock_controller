import os
from app import app

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'you-will-never-guess'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(base_dir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
