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



    return render_template("friends.html", form=form)
