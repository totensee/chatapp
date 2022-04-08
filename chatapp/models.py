from chatapp import db, login_manager, bcrypt_app, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # profile_picture_url = db.Column(db.String, default="") # Set default url
    _chats = db.Column(db.String(), default="")
    _servers_in = db.Column(db.String(), default="")

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt_app.generate_password_hash(plain_text_password).decode("utf-8")

    @property
    def chats(self):
        return self._chats.split(";")

    @chats.setter
    def chats(self, chat):
        self._chats += f";{chat}"

    @property
    def servers_in(self):
        return self._servers_in.split(";")

    @servers_in.setter
    def servers_in(self, server):
        self._servers_in += f";{server}"

    def check_password_correction(self, attempted_password):
        return bcrypt_app.check_password_hash(self.password_hash, attempted_password)

class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    msg_from = db.Column(db.Integer(), nullable=False)
    msg_to = db.Column(db.Integer(), nullable=False)
    content = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.Float(), nullable=False)
    seen = db.Column(db.Boolean(), nullable=False)


class Server(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    owner = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    last_message = db.Column(db.Float(), nullable=False, default=0)

class ServerMessage(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    server_id = db.Column(db.Integer(), nullable=False)
    msg_from = db.Column(db.Integer(), nullable=False)
    content = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.Float(), nullable=False)
    bot = db.Column(db.Float(), nullable=False, default=0)

class Bot(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    auth_token = db.Column(db.String(), nullable=True)
    _servers_in = db.Column(db.String(), default="")

    @property
    def servers_in(self):
        return self._servers_in.split(";")

    @servers_in.setter
    def servers_in(self, server):
        self._servers_in += f";{server}"