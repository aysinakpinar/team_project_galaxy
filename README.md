## Project guidance
This repo contains the seed codebase for the Galaxy project in Python (using
Flask and Pytest).

Create repo in the GitHub account.
Everyone in the team should then clone this repo to their local machine to work on it.

> NOTE: If you encounter a `ModuleNotFound` error, deactivate and then reactivate your virtual env. If that doesn't help, please reach out to your coach.

## Setup

```shell
# Set up the virtual environment
; python -m venv galaxy_venv

# Activate the virtual environment
; source galaxy_venv/bin/activate

# Install dependencies
(galaxy_venv); pip install -r requirements.txt

# Install the virtual browser we will use for testing
(galaxy_venv); playwright install
# If you have problems with the above, contact your coach

# Create a test and development database
(galaxy_venv); createdb galaxy_db
(galaxy_venv); createdb galaxy_db_test

# Open lib/database_connection.py and change the database names
(galaxy_venv); open lib/database_connection.py

# Run the tests (with extra logging)
(galaxy_venv); pytest -sv

# Run the app
(galaxy_venv); python app.py
```

# Now visithttp://127.0.0.1:5000/index in your browser
## Install dependencies in requirement.txt

## Folder structure
```zsh
.
├── README.md
├── app.py # entry point
├── blueprints # business logic
├── config.py # config connection to database
├── extension.py
├── forms # user input 
├── models # tables
├── requirement.txt
├── static # additional assets
├── templates # html files
├── tests
└── venv
```
### db migration
```shell
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### config file:
```py
class Config(object):
    TESTING = False

class DevelopmentConfig(Config):
    DEV_DATABASE_NAME = "galaxy_db"
    SQLALCHEMY_DATABASE_URI = f"postgresql://localhost/{DEV_DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "default_key"

class TestingConfig(Config):
    TEST_DATABASE_NAME = "galaxy_db_test"
    SQLALCHEMY_DATABASE_URI = f"postgresql://localhost/{TEST_DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "default_key"
```
## PR4-Aysin
signup method was implemented in blueprints/auth
forms/signup_form was created to use in templates/signup.html template
templates/signup.html was created to render the signup form.
Signup validation rules were tested in test_user using Faker (requires '''pip install faker''') to generate test inputs.
requirements.txt was updated to include faker library.
To do:
Test the rendering of the signup form and page, ensuring error and success messages display correctly.
Password hash with bcrypt

## PR6-Aysin
- Users table was updated for the relationships:
    - one to many for workouts and gyms
    - many to many for friendships and exercises
- workouts table was updated:
    - many to many for exercises
- friendships table was created.
- gyms table was created.
- exercises table was updated:
    - intensity, 3 options, easy, meduium, hard
- assosciations model was created for many to many relationships

## PR17-Aysin
- Users can create a new workout plan.
- Users can add new exercises to the workout plan.
- Users can remove the exercises from the workout plan.
- Users can mark the exercises as done and undone.
- New model was created to store workout specific exercises with workout_id and exercise_id and also done columns to mark them as done.
- base.html was updated to show Workout, Friends, Dashboard, GymThreads and Log out buttons at nav bar when users are logged in. Otherwise onl login and sign up buttons are visible. 
- 3_exercise_seed.py was update to include 30 different exercises. galaxy_db database needs to be seeded first to see all of the exercises in the drop down menu to add exercises to the workout. 
- Please first create a new migration. upgrade the db and seed all of the seed files (if already seeded first clean the tables and retry seeding)
'''
python seeds/0_user_seed.py
python seeds/1_friendship_seed.py
python seeds/2_user_point_seed.py
python seeds/3_exercise_seed.py
python seeds/4_quote_seed.py
python seeds/5_gym_seed.py
python seeds/6_workout_seed.py
python seeds/7_workout_exercise_seed.py
'''
## PR26
- Users can display the exercises in the workout page.
- Users can also add user specific suggested exercises to the workouts.
- Bugs were fixed for displaying, removing and marking the exercises done for each workouts.
- Mistral chatbot is responding but a bit late (about 9 secs response).
- To use chatbot 
        running Mistral 7
    - pip install -r requirements.txt
    - brew install ollama
    - ollama start
    in another terminal
    - ollama --version #check if it was installed
    - ollama pull mistral:7b-instruct-q4_K_M (may take some time to download)
    - ollama serve (opens the port for mistral) #should run during running the app.
    - ollama run mistral
    - flask run (in another terminal)
- enum in exercise model changed to string
## PR32
- users can display the exercise tutorials.
- exercises are listed in the workouts page under each workout.
- mistral was updated with a slower version mistral:7b-instruct-q4_K_M.
- Chatbot was implemented on the navbar.
- refer to the PR26 to run the chatbot.

## Khadija PR  REAL-Time chat feature

- pip install -r requirements.txt

or pip install flask-socketio  // enables websocket cocmmunication in flask
pip install python-socketio  // provides socketio server implmentation
pip install eventlet  // library required for socketio (all added to requirements.txt)

- Users can view a list of active users in the sidebar
(sidebar displays a list of all active users except the logged in user,
each user is clickable, click to start orivate chat, has to be done for oth users)
- Users can send and recieve messages in real time
(messages are displayed in chat window with senders name)
- Users can join and leave private chat rooms
(clicking on a user joins their private chat room, 
leaving a chat room is handled automatically when switching to another user)
- Users can see when other users are online or offline
(the list of active users updates in real-time as users connect or disconnect)
- Users can only chat with other users who are currently online

messages.html : contains chat interface, handles user interactions & websocket communication using js
chat.py : defines flask routes & socketio event handlers for chat feature, manages user connections, room joining, messaging
app.py : initialises flask app and integrates socketio, starts app using socketio.run(app, debug=true) (comments in app.py to explain my code)


