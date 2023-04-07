import os
from flask import Flask, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_gravatar import Gravatar
from flask_mail import Mail
from functools import wraps

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ckeditor = CKEditor(app)
Bootstrap(app)


mail = Mail(app)


login_manager = LoginManager()
login_manager.init_app(app)

from blog.users.routes import users
from blog.posts.routes import posts
from blog.main.routes import main

login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

gravatar = Gravatar(app, size=100, rating="g", default="retro", force_default=False, force_lower=False, use_ssl=False, base_url=None)


app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)