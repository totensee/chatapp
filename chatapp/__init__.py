from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config["SECRET_KEY"] = "6e18c6a94bc97d5ea85c68cf"
db = SQLAlchemy(app)
bcrypt_app = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
login_manager.login_message = None

from chatapp import routes, api, models