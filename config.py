import os
basedir = os.path.abspath(os.path.dirname(__file__))


class emConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nunca-lo-podras-adivinar'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'emapp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SMTPGOOGLE = {'user': 'deepcri77@gmail.com',
                  'password': '77ircpeed',
                  'server': 'smtp.gmail.com',
                  'port': 587,
                  'SSL': False}

    SMTPNEMARIS = {'user': 'carlos.barajas@nemaris.com.mx',
                   'password': 'uAMyohVz96',
                   'server': 'mail,neemaris.com.mx',
                   'port': 465,
                   'SSL': True}
