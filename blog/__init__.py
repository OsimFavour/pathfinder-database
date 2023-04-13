import os
from flask import Flask, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_gravatar import Gravatar
from flask_mail import Mail
from functools import wraps
from blog.config import Config
from google_auth_oauthlib.flow import Flow


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


db = SQLAlchemy()
ckeditor = CKEditor()
bootstrap = Bootstrap()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

# google_flow = Flow.from_client_secrets_file(
#     client_secrets_file=client_secrets_file,
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.profile", "openid"],
#     redirect_uri="http://127.0.0.1:5000/login?provider=google"
#     )

google_flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    "google_client_secret.json",
    scopes=["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_uri="http://localhost:5000/login?provider=google"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper


def create_app(config_class=Config):
    
    app = Flask(__name__)
    app.app_context().push()
    app.config.from_object(Config)
    
    db.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    gravatar = Gravatar(app, size=100, rating="g", default="retro", force_default=False, force_lower=False, use_ssl=False, base_url=None)

    gravatar.init_app(app)
    
    
    from blog.users.routes import users
    from blog.posts.routes import posts
    from blog.main.routes import main
    from blog.errors.handlers import errors
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app