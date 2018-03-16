import os
basedir = os.path.abspath(os.path.dirname(__file__))


class emConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nunca-lo-podras-adivinar'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'emapp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
