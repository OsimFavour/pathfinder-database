from flask_wtf import FlaskForm
from blog.models import User 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo ,ValidationError


class RegisterForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    # remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RequestResetForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email, you must register first.")


class ResetPasswordForm(FlaskForm): 
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")