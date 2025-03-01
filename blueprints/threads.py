from flask import Blueprint, request, session, flash, redirect, url_for, render_template, abort
from sqlalchemy.sql.operators import from_

from models.post import PostModel
from models.reply import ReplyModel
from models.user import UserModel
from forms.post_reply_form import PostForm, ReplyForm
from extension import db

threads = Blueprint("threads", __name__, url_prefix="/threads")

# Middleware:
# checkAuth
def checkAuth():
    if "user_id" not in session:
        flash("⚠️ Please login to access this page.", "danger")
        return redirect(url_for("auth.login"))
    
# get user_id from session
def get_current_user_id():
    return session["user_id"]

# get username by querying UserModel
def get_current_username():
    user_id = get_current_user_id()
    if user_id:
        user = UserModel.query.get(user_id)
        return user.username
    return None


# Features
# create post
@threads.route("/create", methods = ['GET', 'POST'])
def create_post():
    redirect_response = checkAuth()
    if redirect_response:
        return redirect_response
    form = PostForm()
    if form.validate_on_submit():
        user_id = get_current_user_id()
        new_post = PostModel(
            poster_Id = user_id,
            text = form.text.data,
            img = form.img.data if form.img.data else None
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post created!", "success")
        return redirect(url_for("threads.view_posts"))
    return render_template("create_post.html", form = form)


# reply
@threads.route("/reply/<int:post_id>", methods = ['GET', 'POST'])
def reply(post_id):
    redirect_response = checkAuth()
    if redirect_response:
        return redirect_response
    form = ReplyForm()
    post = PostModel.query.get_or_404(post_id)
    if form.validate_on_submit():
        user_id = get_current_user_id()
        username = get_current_username()
        if not username:
            abort(500, "Username not found")

        new_reply = ReplyModel(
            post_Id = post_id,
            replier_Id = user_id,
            username = username,
            text = form.text.data,
            img = form.img.data if form.img.data else None
        )
        db.session.add(new_reply)
        db.session.commit()
        flash("Reply added!", "success")
        return redirect(url_for("threads.view_posts", post_id = post_id))
    return render_template("reply.html", form = form, post = post)


# view posts
@threads.route("/posts", methods = ['GET'])
def view_posts():
    redirect_response = checkAuth()
    if redirect_response:
        return redirect_response
    posts = PostModel.query.all()
    return render_template("posts.html", posts = posts)


# view post
@threads.route("/posts/<int:post_id>", methods = ['GET'])
def view_post(post_id):
    redirect_response = checkAuth()
    if redirect_response:
        return redirect_response
    post = PostModel.query.get_or_404(post_id)
    return render_template("post.html", post = post, reply_count=len(post.replies))

# view reply
# likes
# need to set up a utility for images