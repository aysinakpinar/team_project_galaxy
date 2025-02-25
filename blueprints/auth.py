# from crypt import methods

# from flask import Blueprint, render_template, redirect, url_for, flash, request, session
# from sqlalchemy.sql.operators import from_
# from wtforms.validators import email

# from forms.login_form import LoginForm
# from forms.register_form import RegisterForm
# from models.user_model import UserModel
# from extension import db
# from forms import register_form, login_form
# from werkzeug.security import generate_password_hash, check_password_hash

# auth = Blueprint("auth", __name__, url_prefix="/auth")

# # Register a new user
# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         # Check if email exists
#         existing_user = UserModel.query.filter_by(email=form.email.data).first()
#         if existing_user:
#             form.email.errors.append("Email already exists")
#             return render_template("register.html", form=form)

#         # Check if username exists
#         existing_username = UserModel.query.filter_by(username=form.username.data).first()
#         if existing_username:
#             form.username.errors.append("Username already taken")
#             return render_template("register.html", form=form)

#         try:
#             # Create new user
#             user = UserModel(
#                 username=form.username.data,
#                 password=form.password.data,
#                 email=form.email.data,
#                 location=form.location.data,
#                 age=form.age.data,
#                 weight=form.weight.data,
#                 height=form.height.data
#             )
#             db.session.add(user)
#             db.session.commit()

#             flash("Account created successfully! Please login.", "success")
#             return redirect(url_for('auth.login'))

#         except Exception as e:
#             db.session.rollback()
#             flash("An error occurred. Please try again.", "danger")
#             return render_template("register.html", form=form)

#     return render_template("register.html", form=form)


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = UserModel.query.filter_by(email=form.email.data).first()

#         # Check if user exists
#         if not user:
#             form.email.errors.append("Email not found")
#             return render_template("login.html", form=form)

#         # Check password
#         if user.password == form.password.data:
#             session['user_id'] = user.id
#             flash("Account Login Successfully", "success")
#             return redirect(url_for("homepage.ListAllSpaces"))
#         else:
#             form.password.errors.append("Password Incorrect")
#             return render_template("login.html", form=form)

#     return render_template("login.html", form=form)


# # Logout from a session
# @auth.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash("Logged out successfully!", "success")
#     return redirect(url_for("auth.login"))

