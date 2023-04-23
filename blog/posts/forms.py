from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class NewsletterPostForm(FlaskForm):
    title = StringField("Newsletter Title", validators=[DataRequired()])
    body = CKEditorField("Newsletter Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class CommentForm(FlaskForm):
    comment = CKEditorField("Comments", validators=[DataRequired()], render_kw={"style": "font-weight: bold;"})
    submit = SubmitField("Submit Comment")
    
   