from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from models.user import UserModel
from extension import db
from forms.find_friends_form import FindFriendsForm

#The user can search for other users based on their location, age, fitness level and favourite exercise.

friends = Blueprint("friends", __name__, url_prefix="/friends")

@friends.route('/find', methods=['GET', 'POST'])
def find():
    form = FindFriendsForm()

    #shows all users if no search criteria is provided
    query = UserModel.query

    #removed, this option is to show no users as default instead.
    #users = None

    location = request.args.get('location') or form.location.data
    age = request.args.get('age') or form.age.data
    fitness_level = request.args.get('fitness_level') or form.fitness_level.data
    favourite_exercise = request.args.get('favourite_exercise') or form.favourite_exercise.data

    #applies filters only if the values are provided, so can have empty fields.
    if location:
        query = query.filter(UserModel.location.ilike(f"%{location.strip()}%"))
    if age:
        query = query.filter(UserModel.age == age)  # Assuming age is an exact match
    if fitness_level:
        query = query.filter(UserModel.fitness_level.ilike(f"%{fitness_level.strip()}%"))
    if favourite_exercise:
        query = query.filter(UserModel.favourite_exercise.ilike(f"%{favourite_exercise.strip()}%"))

    #if no filter applied, show all users
    users = query.all()

    return render_template("friends.html", form=form, users=users)
