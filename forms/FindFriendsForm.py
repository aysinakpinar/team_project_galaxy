#Millie & Lubica

class FindFriendsForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    #favourite exercise.