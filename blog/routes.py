from io import BytesIO
from flask import render_template, redirect, url_for, flash, abort, request, send_file
from blog import app, db, login_manager
from blog.forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, SearchForm
from blog.models import User, PurposePost, RelationshipPost, Fiction, Newsletter, Upload, Comment
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from bs4 import BeautifulSoup


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


# Passing searched data to the navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# @app.route('/')
# def home():
#     page = request.args.get("page", 1, type=int)
#     posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
#     return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route('/')
def home():
    page = request.args.get("page", 1, type=int)
    posts = PurposePost.query.order_by(PurposePost.date.desc()).paginate(page=page, per_page=5)
    # return render_template("index.html", all_posts=posts, current_user=current_user)
    return render_template("about.html", all_posts=posts, current_user=current_user)


@app.route("/purpose")
def purpose():
    page = request.args.get("page", 1, type=int)
    posts = PurposePost.query.order_by(PurposePost.date.desc()).paginate(page=page, per_page=5)
    return render_template("index-purpose.html", all_posts=posts, current_user=current_user)
    

@app.route("/relationship")
def relationship():
    page = request.args.get("page", 1, type=int)
    posts = RelationshipPost.query.order_by(RelationshipPost.date.desc()).paginate(page=page, per_page=5)
    return render_template("index-relationship.html", all_posts=posts, current_user=current_user)


@app.route("/fiction")
def fiction():
    page = request.args.get("page", 1, type=int)
    posts = Fiction.query.order_by(Fiction.date.desc()).paginate(page=page, per_page=5)
    return render_template("index-fiction.html", all_posts=posts, current_user=current_user)


@app.route("/newsletter")
def newsletter():
    page = request.args.get("page", 1, type=int)
    posts = Newsletter.query.order_by(Newsletter.date.desc()).paginate(page=page, per_page=5)
    return render_template("index-newsletter.html", all_posts=posts)


@app.route("/my-books", methods=["GET", "POST"])
def others():
    if request.method == "POST":
        # file = request.files["file"]
        file = request.files.get("file")
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f"Uploaded: {file.filename}"
    return render_template("others.html")


@app.route("/download/<upload_id>")
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)


@app.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        searched_post = form.searched.data
        posts = [
            PurposePost.query.filter(PurposePost.body.like("%" + searched_post + "%")), 
            RelationshipPost.query.filter(RelationshipPost.body.like("%" + searched_post + "%")), 
            Fiction.query.filter(Fiction.body.like("%" + searched_post + "%")), 
            Newsletter.query.filter(Newsletter.body.like("%" + searched_post + "%"))
            ]
        for post in posts:
            blog_posts = post.order_by(posts.title).all()
            # ordered_posts = posts.order_by(post.title).all()
        return render_template("search.html", form=form, searched=searched_post, posts=blog_posts)


# @app.route("/search", methods=["POST"])
# def search():
#     form = SearchForm()
#     if form.validate_on_submit():
#         searched_post = form.searched.data
#         posts = BlogPost.query.filter(BlogPost.body.like("%" + searched_post + "%"))
#         ordered_posts = posts.order_by(BlogPost.title).all()
#         return render_template("search.html", form=form, searched=searched_post, posts=ordered_posts)


@app.route('/register', methods=["GET", "POST"]) 
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


@app.route('/login', methods=["GET", "POST"])
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# @app.route("/post/<int:post_id>", methods=["GET", "POST"])
# @login_required
# def show_post(post_id):
#     form = CommentForm()
#     posts = [
#             PurposePost.query.get(post_id), 
#             RelationshipPost.query.get(post_id), 
#             Fiction.query.get(post_id), 
#             Newsletter.query.get(post_id)
#             ]
#     for post in posts:
#         # requested_post = BlogPost.query.get(post_id)
#         if form.validate_on_submit():
#             if not current_user.is_authenticated:
#                 flash("You need to login or register to comment.", "info")
#                 return redirect(url_for("login"))
#             new_comment = Comment(
#                 text=form.comment.data,
#                 comment_author=current_user,
#                 parent_post=post
#             )
#             db.session.add(new_comment)
#             db.session.commit()
#     return render_template("post.html", form=form, post=post, title=post.title, current_user=current_user)


@app.route("/purpose-post/<int:purpose_post_id>", methods=["GET", "POST"])
@login_required
def show_purpose_post(purpose_post_id):
    form = CommentForm()
    requested_post = PurposePost.query.get(purpose_post_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-purpose.html", form=form, post=requested_post, title=requested_post.title, current_user=current_user, is_purpose=True)


@app.route("/relationship/<int:relationship_post_id>", methods=["GET", "POST"])
@login_required
def show_relationship_post(relationship_post_id):
    form = CommentForm()
    requested_post = RelationshipPost.query.get(relationship_post_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-relationship.html", form=form, post=requested_post, title=requested_post.title, current_user=current_user, is_relationship=True)


@app.route("/fiction/<int:fiction_post_id>", methods=["GET", "POST"])
@login_required
def show_fiction_post(fiction_post_id):
    form = CommentForm()
    requested_post = Fiction.query.get(fiction_post_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-fiction.html", form=form, post=requested_post, title=requested_post.title, current_user=current_user, is_fiction=True)


@app.route("/newsletter/<int:newsletter_id>", methods=["GET", "POST"])
@login_required
def show_newsletter(newsletter_id):
    form = CommentForm()
    requested_post = newsletter.query.get(newsletter_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-newsletter.html", form=form, post=requested_post, title=requested_post.title, current_user=current_user, is_newsletter=True)



@app.route("/about")
def about():
    posts = PurposePost.query.order_by(PurposePost.date.desc())
    return render_template("about.html", all_posts=posts, current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)


# @app.route("/new-post", methods=["GET", "POST"])
# @admin_only
# def add_new_post():
#     form = CreatePostForm()
#     # soup = BeautifulSoup(form.body.data, "html.parser")
#     if form.validate_on_submit():
#         new_post = PurposePost(
#             title=form.title.data,
#             subtitle=form.subtitle.data,
#             body=form.body.data,
#             img_url=form.img_url.data,
#             author=current_user
#         )
#         db.session.add(new_post)
#         db.session.commit()
#         return redirect(url_for("home"))
#     return render_template("make-post.html", form=form, current_user=current_user)


@app.route("/new-post-purpose", methods=["GET", "POST"])
@admin_only
def add_for_purpose():
    form = CreatePostForm()
    # soup = BeautifulSoup(form.body.data, "html.parser")
    if form.validate_on_submit():
        new_post = PurposePost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", title="Post-Purpose", form=form, current_user=current_user, add_for_purpose=True)


@app.route("/new-post-relationship", methods=["GET", "POST"])
@admin_only
def add_for_relationship():
    form = CreatePostForm()
    # soup = BeautifulSoup(form.body.data, "html.parser")
    if form.validate_on_submit():
        new_post = Newsletter(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", title="Post-Relationship", form=form, current_user=current_user, add_for_relationship=True)


@app.route("/new-post-fiction", methods=["GET", "POST"])
@admin_only
def add_for_fiction():
    form = CreatePostForm()
    # soup = BeautifulSoup(form.body.data, "html.parser")
    if form.validate_on_submit():
        new_post = Fiction(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", title="Post-Fiction", form=form, current_user=current_user, add_for_fiction=True)


@app.route("/new-post-newsletter", methods=["GET", "POST"])
@admin_only
def add_for_newsletter():
    form = CreatePostForm()
    # soup = BeautifulSoup(form.body.data, "html.parser")
    if form.validate_on_submit():
        new_post = Newsletter(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", title="Post-Newsletters", form=form, current_user=current_user, add_for_newsletter=True)


# @app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
# @admin_only
# def edit_post(post_id):
#     post = BlogPost.query.get(post_id)
#     edit_form = CreatePostForm(
#         title=post.title,
#         subtitle=post.subtitle,
#         img_url=post.img_url,
#         author=current_user,
#         body=post.body
#     )
#     soup = BeautifulSoup(edit_form.body.data, "html.parser")
#     if edit_form.validate_on_submit():
#         post.title = edit_form.title.data
#         post.subtitle = edit_form.subtitle.data
#         post.img_url = edit_form.img_url.data
#         post.body = soup.text
#         db.session.commit()
#         return redirect(url_for("show_post", post_id=post.id))

#     return render_template("make-post.html", form=edit_form, current_user=current_user)


@app.route("/edit-post-purpose/<int:purpose_post_id>", methods=["GET", "POST"])
@admin_only
def edit_purpose_post(purpose_post_id):
    post = PurposePost.query.get(purpose_post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    soup = BeautifulSoup(edit_form.body.data, "html.parser")
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = soup.text
        db.session.commit()
        return redirect(url_for("show_purpose_post", purpose_post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_purpose=True)


@app.route("/edit-post-relationship/<int:relationship_post_id>", methods=["GET", "POST"])
@admin_only
def edit_relationship_post(relationship_post_id):
    post = RelationshipPost.query.get(relationship_post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    soup = BeautifulSoup(edit_form.body.data, "html.parser")
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = soup.text
        db.session.commit()
        return redirect(url_for("show_relationship_post", relationship_post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_relationship=True)


@app.route("/edit-post-fiction/<int:fiction_post_id>", methods=["GET", "POST"])
@admin_only
def edit_fiction_post(fiction_post_id):
    post = Fiction.query.get(fiction_post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    soup = BeautifulSoup(edit_form.body.data, "html.parser")
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = soup.text
        db.session.commit()
        return redirect(url_for("show_fiction_post", fiction_post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_fiction=True)


@app.route("/edit-post-newsletter/<int:newsletter_id>", methods=["GET", "POST"])
@admin_only
def edit_newsletter(newsletter_id):
    post = Newsletter.query.get(newsletter_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    soup = BeautifulSoup(edit_form.body.data, "html.parser")
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = soup.text
        db.session.commit()
        return redirect(url_for("show_newsletter", newsletter_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_newsletter=True)



# @app.route("/delete/<int:post_id>")
# @admin_only
# def delete_post(post_id):
#     post_to_delete = BlogPost.query.get(post_id)
#     db.session.delete(post_to_delete)
#     db.session.commit()
#     return redirect(url_for('home'))


@app.route("/delete-purpose-post/<int:purpose_post_id>", methods=["POST"])
@admin_only
def delete_purpose_post(purpose_post_id):
    post_to_delete = PurposePost.query.get(purpose_post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete-relationship-post/<int:relationship_post_id>", methods=["POST"])
@admin_only
def delete_relationship_post(relationship_post_id):
    post_to_delete = RelationshipPost.query.get(relationship_post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete-fiction-post/<int:fiction_post_id>", methods=["POST"])
@admin_only
def delete_fiction_post(fiction_post_id):
    post_to_delete = Fiction.query.get(fiction_post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete-newsletter/<int:newsletter_id>", methods=["POST"])
@admin_only
def delete_newsletter(newsletter_id):
    post_to_delete = Newsletter.query.get(newsletter_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

