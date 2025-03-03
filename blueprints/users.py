from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from models.user import UserModel
from extension import db
from forms.user_profile_form import UserProfileForm

#Millie -User profile and ability to edit user account details

users = Blueprint("users", __name__, url_prefix="/users")

@users.route('/profile', methods=['GET', 'POST'])
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
        print("Form submitted!")  # Debugging line

        # Update user attributes with new form data
        user.username = form.username.data
        user.email = form.email.data
        user.location = form.location.data
        user.age = form.age.data
        user.weight = form.weight.data
        user.height = form.height.data
        user.fitness_level = form.fitness_level.data
        user.favourite_exercise = form.favourite_exercise.data

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

    return render_template("profile.html", form=form)
