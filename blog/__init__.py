import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_gravatar import Gravatar
from flask_mail import Mail
from functools import wraps


app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ckeditor = CKEditor(app)
Bootstrap(app)

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MY_EMAIL")
app.config["MAIL_PASSWORD"] = os.environ.get("MY_PASSWORD")
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)

from blog import routes

login_manager.login_view = "login"
login_manager.login_message_category = "info"

gravatar = Gravatar(app, size=100, rating="g", default="retro", force_default=False, force_lower=False, use_ssl=False, base_url=None)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

