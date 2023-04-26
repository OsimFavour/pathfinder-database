from flask import render_template, url_for, flash, redirect, abort, current_app, Blueprint
from flask_login import current_user, login_required
from blog import db, admin_only, google_login_required
from blog.models import PurposePost, RelationshipPost, Fiction, Newsletter, Comment
from blog.posts.forms import CreatePostForm, CommentForm, SearchForm, NewsletterPostForm
from blog.posts.utils import search_posts
from bs4 import BeautifulSoup


posts = Blueprint("posts", __name__)


@posts.route("/purpose-post/<int:purpose_post_id>", methods=["GET", "POST"])
@login_required
def show_purpose_post(purpose_post_id):
    form = CommentForm()
    requested_post = PurposePost.query.get(purpose_post_id)
    # Get the next three posts
    all_posts =  PurposePost.query.order_by(PurposePost.date.desc()).all()
    # Find the index of the requested post
    index = all_posts.index(requested_post)
    # Calculate the indices of the next three posts
    next_indices = [(index + i + 1) % len(all_posts) for i in range(3)]
    # Get the next three posts
    next_posts = [all_posts[i] for i in next_indices]
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("users.login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            purpose_parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-purpose.html", form=form, post=requested_post, next_posts=next_posts, title=requested_post.title, current_user=current_user, is_purpose=True)


@posts.route("/relationship/<int:relationship_post_id>", methods=["GET", "POST"])
@login_required
def show_relationship_post(relationship_post_id):
    form = CommentForm()
    requested_post = RelationshipPost.query.get(relationship_post_id)
    all_posts =  RelationshipPost.query.order_by(RelationshipPost.date.desc()).all()
    index = all_posts.index(requested_post)
    next_indices = [(index + i + 1) % len(all_posts) for i in range(3)]
    next_posts = [all_posts[i] for i in next_indices]
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("users.login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            relationship_parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-relationship.html", form=form, post=requested_post, next_posts=next_posts, title=requested_post.title, current_user=current_user, is_relationship=True)


@posts.route("/fiction/<int:fiction_post_id>", methods=["GET", "POST"])
@login_required
def show_fiction_post(fiction_post_id):
    form = CommentForm()
    requested_post = Fiction.query.get(fiction_post_id)
    all_posts =  Fiction.query.order_by(Fiction.date.desc()).all()
    index = all_posts.index(requested_post)
    next_indices = [(index + i + 1) % len(all_posts) for i in range(3)]
    next_posts = [all_posts[i] for i in next_indices]

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("users.login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            fiction_parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-fiction.html", form=form, post=requested_post, next_posts=next_posts, title=requested_post.title, current_user=current_user, is_fiction=True)


@posts.route("/newsletter/<int:newsletter_id>", methods=["GET", "POST"])
@login_required
def show_newsletter(newsletter_id):
    form = CommentForm()
    requested_post = Newsletter.query.get(newsletter_id)
    next_posts = Newsletter.query.order_by(Newsletter.date.desc()).limit(4).all()
    # all_posts =  Newsletter.query.order_by(Newsletter.date.desc()).all()
    # index = all_posts.index(requested_post)
    # next_indices = [(index + i + 1) % len(all_posts) for i in range(3)]
    # next_posts = [all_posts[i] for i in next_indices]
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("users.login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post-newsletter.html", form=form, post=requested_post, next_posts=next_posts, title=requested_post.title, current_user=current_user, is_newsletter=True)


# MAKE NEW POSTS

@posts.route("/new-post-purpose", methods=["GET", "POST"])
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
        return redirect(url_for("main.home"))
    return render_template("make-post.html", title="Post-Purpose", form=form, current_user=current_user, add_for_purpose=True)


@posts.route("/new-post-relationship", methods=["GET", "POST"])
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
        return redirect(url_for("main.home"))
    return render_template("make-post.html", title="Post-Relationship", form=form, current_user=current_user, add_for_relationship=True)


@posts.route("/new-post-fiction", methods=["GET", "POST"])
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
        return redirect(url_for("main.fiction"))
    return render_template("make-post.html", title="Post-Fiction", form=form, current_user=current_user, add_for_fiction=True)


@posts.route("/new-post-newsletter", methods=["GET", "POST"])
@admin_only
def add_for_newsletter():
    form = NewsletterPostForm()
    # soup = BeautifulSoup(form.body.data, "html.parser")
    if form.validate_on_submit():
        new_post = Newsletter(
            title=form.title.data,
            body=form.body.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("main.newsletter"))
    return render_template("make-post.html", title="Post-Newsletters", form=form, current_user=current_user, add_for_newsletter=True)


# EDIT POSTS


@posts.route("/edit-post-purpose/<int:purpose_post_id>", methods=["GET", "POST"])
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
        return redirect(url_for("posts.show_purpose_post", purpose_post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_purpose=True)


@posts.route("/edit-post-relationship/<int:relationship_post_id>", methods=["GET", "POST"])
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
        return redirect(url_for("posts.show_relationship_post", relationship_post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_relationship=True)


@posts.route("/edit-post-fiction/<int:fiction_post_id>", methods=["GET", "POST"])
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
        return redirect(url_for("posts.show_fiction_post", fiction_post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_fiction=True)


@posts.route("/edit-post-newsletter/<int:newsletter_id>", methods=["GET", "POST"])
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
        return redirect(url_for("posts.show_newsletter", newsletter_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user, edit_for_newsletter=True)


# DELETE POSTS


@posts.route("/delete-purpose-post/<int:purpose_post_id>", methods=["POST"])
@admin_only
def delete_purpose_post(purpose_post_id):
    post_to_delete = PurposePost.query.get(purpose_post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.home'))


@posts.route("/delete-relationship-post/<int:relationship_post_id>", methods=["POST"])
@admin_only
def delete_relationship_post(relationship_post_id):
    post_to_delete = RelationshipPost.query.get(relationship_post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.home'))


@posts.route("/delete-fiction-post/<int:fiction_post_id>", methods=["POST"])
@admin_only
def delete_fiction_post(fiction_post_id):
    post_to_delete = Fiction.query.get(fiction_post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.home'))


@posts.route("/delete-newsletter/<int:newsletter_id>", methods=["POST"])
@admin_only
def delete_newsletter(newsletter_id):
    post_to_delete = Newsletter.query.get(newsletter_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.home'))


# SEARCH POSTS

# Passing searched data to the navbar
@current_app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@posts.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.searched.data
        all_posts = search_posts(query)
        return render_template("search.html", form=form, searched=query, posts=all_posts)
    return render_template("errors/400.html"), 400


@posts.route("/post/<int:post_id>")
def show_searched_post(post_id):
    post = None

    purpose_post = PurposePost.query.filter_by(id=post_id).first()
    relationship_post = RelationshipPost.query.filter_by(id=post_id).first()
    fiction_post = Fiction.query.filter_by(id=post_id).first()
    newsletters = Newsletter.query.filter_by(id=post_id).first()

    if purpose_post:
        post = purpose_post
    elif relationship_post:
        post = relationship_post
    elif fiction_post:
        post = fiction_post
    elif newsletters:
        post = newsletters

    if not post:
        return render_template("404.html"), 404
    
    return render_template("post.html", post=post)