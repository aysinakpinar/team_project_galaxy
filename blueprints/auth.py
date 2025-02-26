from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from sqlalchemy.sql.operators import from_
from wtforms.validators import email

from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from models.user import UserModel
from extension import db
from forms import register_form, login_form

auth = Blueprint("auth", __name__, url_prefix="/auth")

# ----- login route -- | Michal | ------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        submitted_email = form.email.data
        submitted_password = form.password.data
        # check for the data in the database
        found_user = UserModel.query.filter_by(email=submitted_email).first()
        # if wrong email
        if not found_user:
            form.email.errors.append("Wrong email address")
        # if wrong password
        elif found_user.password != submitted_password:
            form.password.errors.append("Wrong password")
        # if successfully logged in
        else:
            # ||CHANGE REQUIRED|| - redirection to another page and session user_id
            # redirect("/user-dashboard") ???
            # session['user_id'] = found_user.id
            print("Success")
        return render_template("login.html", form=form)
    return render_template("login.html", form=form)

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


    
