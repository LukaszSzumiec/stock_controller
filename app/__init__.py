from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

from config import Config

app.config.from_object(Config)
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

from app.models.model import Company, User
migrate = Migrate(app, db)

from app.routes import *
from app.models.model import Company, User
