import os
import json


class Config:

    # SECRET_KEY = 8BYkEfBA6O6donzWlSihBXox7C0sKR6b
    SECRET_KEY = os.environ.get("WEB_PATHFINDER_SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = sqlite:///blog.db
    SQLALCHEMY_DATABASE_URI = os.environ.get("WEB_PATHFINDER_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MY_EMAIL")
    MAIL_PASSWORD = os.environ.get("MY_PASSWORD")

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    GOOGLE_CLIENT_ID = "931067967702-hgr1u7l6v1ldcq769md1j8h6ijhljkdt.apps.googleusercontent.com"
    
    