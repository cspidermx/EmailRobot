from emapp import emrdb
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from emapp import login
from time import time
import jwt
from emapp import app


class User(UserMixin, emrdb.Model):
    id = emrdb.Column(emrdb.Integer, primary_key=True)
    username = emrdb.Column(emrdb.String(64), index=True, unique=True)
    email = emrdb.Column(emrdb.String(120), index=True, unique=True)
    password_hash = emrdb.Column(emrdb.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Usuario {}>'.format(self.username)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'restablecer_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            idtkn = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(idtkn)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
