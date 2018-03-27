from flask import Flask
from config import emConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(emConfig)
emrdb = SQLAlchemy(app)
migratedb = Migrate(app, emrdb)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)


from emapp import routes, models, emailfunc, errors


emailfunc.maint(1)
