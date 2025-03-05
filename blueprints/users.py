from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from models.user import UserModel
from models.friendship import FriendshipModel
from extension import db
from forms.user_profile_form import UserProfileForm
import os
from sqlalchemy import or_, and_

from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

UPLOAD_FOLDER = "static/profile_pics"


#Millie -User profile and ability to edit user account details

users = Blueprint("users", __name__, url_prefix="/users")

@users.route('/profile', methods=['GET'])
def profile():
    print(f"📡 Request method: {request.method}")

    # Check if a specific user_id is provided (for friends' profiles)
    user_id = request.args.get('user_id', session.get('user_id'))

    if not user_id:
        flash("You need to log in first!", "danger")
        return redirect(url_for("auth.login"))

    user = UserModel.query.get(user_id)
    if not user:
        flash("User not found!", "danger")
        return redirect(url_for("auth.login"))

    # Fetch approved friends for the profile being viewed
    friends = get_friends_of_user(user_id)

    return render_template("profile.html", user=user, friends=friends)


    # user_id = session.get('user_id')
    # if not user_id:
    #     flash("You need to log in first!", "danger")
    #     return redirect(url_for("auth.login"))
    
    # user = UserModel.query.get(user_id)
    # if not user:
    #     flash("User not found!", "danger")
    #     return redirect(url_for("auth.login"))
    
    # return render_template("profile.html", user=user)


@users.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    print(f"📡 Request method: {request.method}")

    form = UserProfileForm()
  
    # Ensure user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash("You need to log in first!", "danger")
        return redirect(url_for("auth.login"))

    # Fetch the current user from the database
    user = UserModel.query.get(user_id)
    if not user:
        flash("User not found!", "danger")
        return redirect(url_for("auth.login"))

    form = UserProfileForm(obj=user)  # Pre-fill the form with existing user data

    if form.validate_on_submit():
        print("Form submitted!") 

        # Update user attributes with new form data
        user.username = form.username.data
        user.email = form.email.data
        user.location = form.location.data
        user.age = form.age.data
        user.weight = form.weight.data
        user.height = form.height.data
        user.fitness_level = form.fitness_level.data
        user.favourite_exercise = form.favourite_exercise.data

        # Profile picture upload
        picture_file = form.profile_picture.data  

        if picture_file and isinstance(picture_file, FileStorage):  # Ensure it's a valid uploaded file
            filename = secure_filename(picture_file.filename)

            if filename:  # Avoid saving empty filenames
                filepath = os.path.join("static/profile_pics", filename)
                picture_file.save(filepath)
                user.profile_picture = filename

        # # Profile picture upload
        # picture_file = form.profile_picture.data
        # if picture_file:
        #     filename = secure_filename(picture_file.filename) 
        #     filepath = os.path.join("static/profile_pics", filename)
        #     picture_file.save(filepath) 
        #     user.profile_picture = filename  # Store new filename in database

        try:
            db.session.commit()  # Save changes
            flash("Profile updated successfully!", "success")
            return redirect(url_for("users.edit_profile"))  # Redirect to profile page
        except Exception as e:
            db.session.rollback()
            flash("An error occurred. Please try again.", "danger")

    if form.errors:
        print("❌ Form validation errors:", form.errors)  # Debugging

    if request.method == "POST":
        print("🛠 Form submission received!")

    return render_template("edit_profile.html", form=form, user=user)


def get_friends_of_user(user_id):
    friends = db.session.query(
        UserModel.id,
        UserModel.username,
        UserModel.location,
        UserModel.age,
        UserModel.fitness_level,
        UserModel.favourite_exercise
    ).join(FriendshipModel, or_(
        and_(UserModel.id == FriendshipModel.friend_id, FriendshipModel.user_id == user_id),
        and_(UserModel.id == FriendshipModel.user_id, FriendshipModel.friend_id == user_id)
    )).filter(
        FriendshipModel.status == "approved"
    ).all()
    
    return friends
