import jwt
from chatapp import db, login_manager, bcrypt_app
from flask_login import UserMixin
from chatapp import app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    auth_token = db.Column(db.String(length=200))

    @property
    def password(self):
        return self.password

    @property
    def auth_token(self):
        payload = {
            'sub': self.id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm = "HS256"
        )


    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt_app.generate_password_hash(plain_text_password).decode("utf-8")

    def check_password_correction(self, attempted_password):
        return bcrypt_app.check_password_hash(self.password_hash, attempted_password)