#Searching users based on their location 
#Millie & Lubica

friends = Blueprint("friends", __name__, url_prefix="/friends")

@friends.route('/find', methods=['GET'])
def find_friends():
    form = FindFriendsForm()


    return render_template("friends.html", form=form)
