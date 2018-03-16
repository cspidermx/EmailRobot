from flask import Flask
from config import emConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(emConfig)
emrdb = SQLAlchemy(app)
migratedb = Migrate(app, emrdb)
login = LoginManager(app)
login.login_view = 'login'

from emapp import routes, models
