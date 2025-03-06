import os
from flask import Blueprint, request, session, flash, redirect, url_for, render_template, abort
from sqlalchemy.sql.operators import from_
from werkzeug.utils import secure_filename

from models.post import PostModel
from models.reply import ReplyModel
from models.user import UserModel
from models.like import LikeModel
from forms.post_reply_form import PostForm, ReplyForm
from extension import db

threads = Blueprint("threads", __name__, url_prefix="/threads")

# Middleware + utils
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
# view posts + handling post creation
@threads.route("/posts", methods = ['GET', 'POST'])
def view_posts():
    redirect_response = checkAuth()
    if redirect_response:
        return redirect_response

    form = PostForm()
    if form.validate_on_submit():
        user_id = get_current_user_id()
        img_path = None
        if form.img.data:
            img = form.img.data
            filename = secure_filename(img.filename)
            img_path = os.path.join('static/images/posts', filename)
            img.save(img_path)
            img_path = f"images/posts/{filename}"

        new_post = PostModel(
            poster_Id=user_id,
            text=form.text.data,
            img=img_path
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post created!", "success")
        return redirect(url_for("threads.view_posts"))

    posts = PostModel.query.order_by(PostModel.created_at.desc()).all()
    current_user = UserModel.query.get(get_current_user_id())
    return render_template("posts.html", posts=posts, form=form, current_user=current_user)


# reply
@threads.route("/reply/<int:post_id>", methods = ['GET', 'POST'])
def reply(post_id):
    redirect_response = checkAuth()
    if redirect_response:
        return redirect_response
    form = ReplyForm()
    parent_reply = None
    post = PostModel.query.get_or_404(post_id)
    if request.args.get("parent_reply_id"):
        parent_reply_id = int(request.args.get("parent_reply_id"))
        parent_reply = ReplyModel.query.get_or_404(parent_reply_id)
    
    if form.validate_on_submit():
        user_id = get_current_user_id()
        username = get_current_username()
        if not username:
            abort(500, "Username not found")
        
        img_path = None
        if form.img.data:
            img = form.img.data
            filename = secure_filename(img.filename)
            img_path = os.path.join('static/images/posts', filename)
            img.save(img_path)
            img_path = f"images/posts/{filename}"
        
        new_reply = ReplyModel(
            post_Id=post_id,
            replier_Id=user_id,
            parent_reply_id = parent_reply.id if parent_reply else None,
            username=username,
            text=form.text.data,
            img=img_path
        )
        db.session.add(new_reply)
        db.session.commit()
        flash("Reply added!", "success")
        return redirect(url_for("threads.view_post", post_id=post_id))
    return render_template("reply.html", form=form, post=post, parent_reply=parent_reply)


# view post
@threads.route("/posts/<int:post_id>", methods=['GET'])
def view_post(post_id):
    redirect_response = checkAuth()
    if redirect_response:
        return redirect_response
    post = PostModel.query.get_or_404(post_id)
    highlight_reply = request.args.get('highlight_reply', type=int)
    return render_template(
        "post.html",
        post=post,
        reply_count=len(post.replies),
        highlight_reply=highlight_reply
    )


# view reply
@threads.route("/reply/<int:reply_id>", methods=['GET'])
def view_reply(reply_id):
    redirect_response = checkAuth()
    if redirect_response:
        return redirect_response
    reply = ReplyModel.query.get_or_404(reply_id)
    return redirect(url_for("threads.view_post", post_id = reply.post_Id, highlight_reply = reply.id))


# likes
@threads.route("/like/<string:content_type>/<int:content_id>", methods=['POST'])
def like(content_type, content_id):
    redirect_response = checkAuth()
    if redirect_response:
        return redirect_response

    user_id = get_current_user_id()

    if content_type == "post":
        content = PostModel.query.get_or_404(content_id)
        if request.referrer and '/threads/posts' in request.referrer and not request.referrer.endswith(f'/posts/{content_id}'):
            redirect_route = "threads.view_posts"
            redirect_args = {} 
        else:
            redirect_route = "threads.view_post"  # Default to post page otherwise
            redirect_args = {"post_id": content_id}
    elif content_type == "reply":
        content = ReplyModel.query.get_or_404(content_id)
        redirect_route = "threads.view_post"
        redirect_args = {"post_id": content.post_Id}
    else:
        abort(400, "Invalid content type")

    # Check if the user has already liked this content
    existing_like = LikeModel.query.filter_by(
        user_id=user_id,
        post_id=content_id if content_type == "post" else None,
        reply_id=content_id if content_type == "reply" else None
    ).first()

    if existing_like:
        # Unlike: Remove the like
        db.session.delete(existing_like)
    else:
        # Like: Add a new like
        new_like = LikeModel(
            user_id=user_id,
            post_id=content_id if content_type == "post" else None,
            reply_id=content_id if content_type == "reply" else None
        )
        db.session.add(new_like)
    
    db.session.commit()
    
    # Redirect back, preserving highlight_reply if present
    highlight_reply = request.args.get('highlight_reply')
    if highlight_reply:
        redirect_args['highlight_reply'] = highlight_reply
    
    return redirect(url_for(redirect_route, **redirect_args))
