from flask import Blueprint
 
users = Blueprint("users", __name__)


@users.route('/register', methods=["GET", "POST"]) 
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # flash(f"Account created for {form.name.data}!", "success")
        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!", "danger")
            return redirect(url_for("login"))
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
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form, current_user=current_user)


@users.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again!", "danger")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password Incorrect, Please try again!", "danger")
            return redirect(url_for("login"))
        else:
            login_user(user)
            next_page = request.args.get("next")
            print(next_page)
            # if next_page:
            #     return redirect(next_page)
            # # else:
            # return redirect(url_for("home"))
            # return redirect(next_page)
            return redirect(next_page) if next_page else redirect(url_for("home"))
    return render_template("login.html", title="Login", form=form, current_user=current_user)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@users.route("/reset-password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("login"))
    return render_template("reset-request.html", title="Reset Password", form=form)


@users.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
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
        return redirect(url_for("login"))
    return render_template("reset-token.html", title="Reset Password", form=form)

    