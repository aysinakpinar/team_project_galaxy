from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from forms import FindFriendsForm
from models.user import UserModel
from extension import db
from forms.FindFriendsForm import FindFriendsForm

#Searching users based on their location 
#Millie & Lubica

friends = Blueprint("friends", __name__, url_prefix="/friends")

@friends.route('/find', methods=['GET', 'POST'])
def find():
    form = FindFriendsForm()
    users = []

    if form.validate_on_submit():
        location = form.location.data
        users = UserModel.query.filter(UserModel.location == location).all()

        if not users:
            return "No friends found"
            # return render_template("friends.html", form=form, users=users)
        
        return render_template("friends.html", form=form, users=users)
    
    return render_template("friends.html", form=form, users=users)
    
    # else:
    #     return "No friends found"

    # friends = UserModel.query.filter(
    # (UserModel.location == form.location.data) &
    # (UserModel.username != form.username.data)
    # ).all()
    
    # if not friends:
    #     return "No friends found"
    
    # return render_template("friends.html", form=form)

    
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         location = request.form['location']
#         return redirect(url_for('show_results', location=location))
#     return render_template('friends.html')



    #users = []


    # if form.validate_on_submit():
    #     location = form.location.data
    #     users = UserModel.query.filter(UserModel.location == form.location).all()
        
    


    # return render_template("friends.html", form=form, users=users)
