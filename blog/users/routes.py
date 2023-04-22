import requests
import secrets
import string
from flask import render_template, redirect, url_for, flash, abort, session, request, Blueprint
from flask_login import current_user, login_user, logout_user
from blog import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, REDIRECT_URI, JAVASCRIPT_ORIGINS, google_flow, db
from blog.models import User
from blog.users.utils import send_reset_email
from blog.users.forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from sqlalchemy.exc import IntegrityError
from cachecontrol.wrapper import CacheControl
from werkzeug.security import generate_password_hash, check_password_hash
 
users = Blueprint("users", __name__)


@users.route('/register', methods=['GET', 'POST']) 
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # flash(f"Account created for {form.name.data}!", "success")
        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!", "danger")
            return redirect(url_for("users.login"))
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hash_and_salted_password
        )
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("main.home"))
    return render_template("register.html", title="Register", form=form, current_user=current_user)


@users.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again!", "danger")
            return redirect(url_for("users.login"))
        elif not check_password_hash(user.password, password):
            flash("Password Incorrect, Please try again!", "danger")
            return redirect(url_for("users.login"))
        else:
            login_user(user)
            next_page = request.args.get("next")
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
    return render_template('login.html', title='Login', form=form, current_user=current_user)


@users.route("/google-register", methods=["GET", "POST"])
def google_register():
    if request.method == "POST":
        authorization_url, state = google_flow.authorization_url()
        session["state"] = state
        session["register"] = True  # Set flag to indicate registration
        print(state)
        return redirect(authorization_url)
    return redirect(url_for("main.home"))


@users.route("/google-login", methods=["GET", "POST"])
def google_login():
    if request.method == "POST":
        authorization_url, state = google_flow.authorization_url()
        session["state"] = state
        session["register"] = False   # Set flag to indicate login
        print(state)
        return redirect(authorization_url)
    return redirect(url_for("main.home"))


@users.route("/callback")
def callback():
    try:
        google_flow.fetch_token(authorization_response=request.url)
        state = session["state"]
        is_registering = session["register"]    # Get flag to determine flow
        if not state == request.args.get("state"):
            abort(400)
        credentials = google_flow.credentials
        request_session = requests.session()
        cached_session = CacheControl(request_session)
        token_request = Request(session=cached_session)
        google_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )
        print(google_info)

        user = User.query.filter_by(email=google_info['email']).first()
    
        alphabet = string.ascii_letters + string.digits  
        password = ''.join(secrets.choice(alphabet) for i in range(12)) 
        
        hash_and_salted_google_password = generate_password_hash(
            password,
            method="pbkdf2:sha256",
            salt_length=8
        )

        if user and is_registering:
            flash("You've already signed up with that email, log in instead!", "danger")

        elif user is None and is_registering:
            # Register User
            user = User(
                google_id=google_info["sub"], 
                name=google_info['name'], 
                email=google_info['email'], 
                password=hash_and_salted_google_password
                )
            db.session.add(user)
        elif user is None and not is_registering:
            # User is logging in but is not registered
            flash("You need to register here", "info")
            return redirect(url_for("users.register"))
        else:
            # User is logging in
            if not check_password_hash(user.password, password):
                flash("Incorrect password", "danger")
                return redirect(url_for("users.login"))

        user.google_id = google_info["sub"]
        db.session.commit()

        # session["google_id"] = google_info["sub"]
        # session["name"] = google_info["name"]
        # session["email"] = google_info['email']
        # user_name = google_user['name']

        # Redirect to the main page
        login_user(user)
        next_page = request.args.get("next")
        print(next_page)
        return redirect(next_page) if next_page else redirect(url_for("main.home"))

    except ValueError as e:
        # Invalid token
        abort(400, str(e))

    except IntegrityError:
        db.session.rollback()
        flash("Username already exists, please choose a different name.", "info")
        return redirect(url_for("users.register"))

    except Exception as e:
        # Other error
        print(e)
        abort(500, "An error occurred while processing the request")


@users.route('/logout')
def logout():
    if session.get("state") == request.args.get("state"):
        session.clear()
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/reset-password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("users.login"))
    return render_template("reset-request.html", title="Reset Password", form=form)


@users.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )
        user.password = hash_and_salted_password
    
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template("reset-token.html", title="Reset Password", form=form)

    