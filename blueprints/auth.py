#from crypt import methods

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from sqlalchemy.sql.operators import from_
from wtforms.validators import email

#from forms.login_form import LoginForm
#from forms.register_form import RegisterForm
from models.user import UserModel
from extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from forms.signup_form import SignupForm

auth = Blueprint("auth", __name__, url_prefix="/auth")

# Register a new user
#Aysin's code for signup
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    
    if request.method == 'POST':
        print("🔍 Received POST request")

        if form.validate_on_submit():
            print(f"✅ Valid form data - Username: {form.username.data}, Email: {form.email.data}, Location: {form.location.data}")

            # Check if email already exists
            if UserModel.query.filter_by(email=form.email.data).first():
                form.email.errors.append("Email already exists")
                return render_template("signup.html", form=form)

            # Check if username already exists
            if UserModel.query.filter_by(username=form.username.data).first():
                form.username.errors.append("Username already taken")
                return render_template("signup.html", form=form)

            try:
                # Create new user
                user = UserModel(
                    username=form.username.data,
                    password=form.password.data,  
                    email=form.email.data,
                    location=form.location.data,
                )
                db.session.add(user)
                db.session.commit()

                flash("🎉 Account created successfully! Please login.", "success")

                # ✅ **Redirect instead of rendering the template** (Prevents form resubmission issue)
                return redirect(url_for('auth.signup'))

            except Exception as e:
                db.session.rollback()
                flash("⚠️ An error occurred. Please try again.", "danger")

                return render_template("signup.html", form=form)

    # GET request - Just render the form
    return render_template("signup.html", form=form)

# Logout from a session
@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.modified = True

    #resp = make_response(redirect(url_for("auth.login")))
    resp = make_response("Logged out successfully!")
    resp.set_cookie('user_id', expires=0)

    flash("Logged out successfully!", "success")
    return resp