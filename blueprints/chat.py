# khadijas code for chatbox
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from flask_socketio import SocketIO, send
from models.user import UserModel


chat = Blueprint("chat", __name__, url_prefix="/chat")

@chat.route("/")
def message():
    return render_template("messages.html")

def init_socketio(socketio): #initialise socketio event handling 
    @socketio.on("message") #define en event listener for the event "message"
    def sendMessage(data): #function triggered when user sends message
        # print(f"Received message: {message}")  # Debugging line
        user_id = session.get("user_id")

        if not user_id:
            username = "Random"

        else:
            user = UserModel.query.get(user_id)
            username = user.username if user else "Random"
            
        message = data.get("message", "")
        send(f"{username}: {message}", broadcast = True) #broadcast recieved message so all connected users can see

    @socketio.on("connect") # if user is connected message is displayed 
    def test_message():
        send("🔥 Welcome to the chat!", broadcast=True)





# chat.py
# # khadijas code for chatbox
# from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
# from flask_socketio import SocketIO, send
# from models.user import UserModel


# chat = Blueprint("chat", __name__, url_prefix="/chat")

# @chat.route("/")
# def message():
#     return render_template("messages.html")

# def init_socketio(socketio): #initialise socketio event handling 
#     @socketio.on("message") #define en event listener for the event "message"
#     def sendMessage(message): #function triggered when user sends message
#         print(f"Received message: {message}")  # Debugging line
#         send(message, broadcast = True) #broadcast recieved message so all connected users can see

#     @socketio.on("connect") # if user is connected message is displayed 
#     def test_message():
#         send("🔥 Welcome to the chat!", broadcast=True)

# messages.html

# <!-- khadijas code for chatbox  -->

# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"
#         integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA=="
#         crossorigin="anonymous"></script>
#     <title>Document</title>
# </head>
# <body>
#     <div class="messages" id="messageContainer">
#     <input placeholder="message" id= "messageInput" />
#     </div>

#     <style>
#         body {
#             font-family: sans-serif;
#             background-color: linear-gradient(black, grey);
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             height: 100vh;
#             margin: 0;
#             color: white;
#             overflow: hidden;
#         }

#         .messages {
#             width: 80%;
#             max-height: 500px;
#             background-color: rgba(0, 0, 0, 0.7);
#             padding: 20px;
#             box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
#             overflow-y: auto;
#             border-radius: 10px;
#             border: 1px solid rgb(48, 22, 48)
#         }

#         .messages p {
#             margin: 10px 0;
#             font-size: 1.2rem;
#             line-height: 1.5;
#             background-image: linear-gradient(45deg, #0db2b8, #9e28d0);
#             padding: 5px;
#             box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
#             border-radius: 8px;
#             /* animation: pulse 2s infinite ease-in-out; */
#         }

#         input {
#             width: 100%;
#             padding: 15px;
#             margin-top: 15px;
#             border-radius: 10px;
#             border: none;
#             background-color: #3a4b7a;
#             color: white;
#             font-size: 1.2rem;
#             outline: none;
#             box-sizing: border-box;
#         }

#         input::placeholder {
#             color: #b9c8d5
#         }

#         input:focus {
#             background-color: #1e2a47;
#         }

#         p {
#             margin: 5px 0;
#         }
#     </style>


#     <script>
#         const socket = io();

#         let messageContainer = document.getElementById("messageContainer");
#         if (!messageContainer) {
#             console.error("🚨 Error: .messages container not found");
#         }

#         socket.on("connect", () => {
#             let p = document.createElement("p")
#             p.innerText = "You're connected"
#             messageContainer.appendChild(p)
#         })

#         let messageInput = document.getElementById("messageInput")
#         messageInput.addEventListener("keypress", (e) => {
#             if (e.key === "Enter") {
#                 let message = messageInput.value.trim();
#                 if (message) {
#                     socket.emit("message", message)
#                     messageInput.value = "";
#                 }
#             }
#         })

#         socket.on('message', (message) => {
#             console.log("Received message:", message);  // Debugging
#             let messageElement = document.createElement("p")
#             messageElement.innerText = message
#             messageContainer.appendChild(messageElement)

#             // Auto-scroll to the bottom of the chat
#             messageContainer.scrollTop = messageContainer.scrollHeight;
#         })

#     </script>
# </body>
# </html>

# user.py

# from datetime import datetime, timezone
# from extension import db
# from models.associations import user_exercise
# from models.friendship import FriendshipModel


# class UserModel(db.Model):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(200), nullable=False, unique=True)
#     password = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), nullable=False, unique=True)
#     profile_picture = db.Column(db.String(200), nullable=True)
#     location = db.Column(db.String(200), nullable=False)
#     age = db.Column(db.Integer, nullable=True)
#     weight = db.Column(db.Integer, nullable=True)
#     height = db.Column(db.Integer, nullable=True)
#     fitness_level = db.Column(db.String(200), nullable=True)
#     favorite_exercise = db.Column(db.String(200), nullable=True)
#     created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


#     # Relationships
#     workouts = db.relationship(
#         "WorkoutModel", 
#         backref="user", 
#         lazy=True, 
#         cascade="all, delete"
#     )
#     gyms = db.relationship(
#         "GymModel", 
#         backref="user", 
#         lazy=True, 
#         cascade="all, delete"
#     )
#     # Many-to-Many with Exercises
#     exercises = db.relationship(
#         "ExerciseModel", 
#         secondary=user_exercise, 
#         back_populates="users"
#     ) 
#     def add_friend(self, friend):
#         """Creates a friendship between two users."""
#         if not FriendshipModel.query.filter_by(user_id=self.id, friend_id=friend.id).first():
#             friendship = FriendshipModel(user_id=self.id, friend_id=friend.id)
#             db.session.add(friendship)
#             db.session.commit()

# app.py

# from config import TestingConfig 
# from extension import db
# from flask import Flask
# from flask_migrate import Migrate
# from models.user import UserModel
# from models.workout import WorkoutModel
# from models.exercise import ExerciseModel
# from models.friendship import FriendshipModel
# from models.gym import GymModel
# from flask_sqlalchemy import SQLAlchemy
# from blueprints.auth import auth
# from blueprints.dashboard import dashboard
# import os
# from blueprints.friends import friends

# #khaadijas chat cod
# from blueprints.chat import chat, init_socketio
# from flask_socketio import SocketIO # Importing Socketio for real time communications

# socketio = SocketIO(cors_allowed_origins="*") #allows all domains to connect using socketio


# def create_app(config_class=None):
#     #create and configure the Flask App
#     app = Flask(__name__)

#     if config_class is None:
#         if os.getenv("FLASK_ENV") == "testing":
#             from config import TestingConfig
#             app.config.from_object(TestingConfig)
#         else:
#             from config import DevelopmentConfig
#             app.config.from_object(DevelopmentConfig)
#     else:
#         app.config.from_object(config_class)

#     if "SQLALCHEMY_DATABASE_URI" not in app.config:
#         raise RuntimeError("❌ SQLALCHEMY_DATABASE_URI is missing from config.py!")

#     # Initialize extensions
#     db.init_app(app)  # Initialize the SQLAlchemy instance with the Flask app
#     migrate = Migrate(app, db)  # Create a Migrate instance for database migrations

#     # Test database connection
#     try:
#         with app.app_context():  # Ensure the code runs within the Flask application context
#             with db.engine.connect() as connection:  # Establish a connection to the database
#                 print("PostgreSQL connection successful!")
#     except Exception as e:
#         print("Failed to connect to PostgreSQL:", str(e))  # Print the error message if connection fails

#     # Registering blueprints
#     app.register_blueprint(auth, url_prefix='/auth')
#     app.register_blueprint(dashboard, url_prefix='/dashboard') #register user route
#     app.register_blueprint(friends)

#     #khadijas chat code
#     app.register_blueprint(chat, url_prefix='/chat')
#     socketio.init_app(app) #connects flask app w socetio for real time chat
#     init_socketio(socketio)


#     return app

# if __name__ == "__main__":
#     app = create_app()

#     # # Test database connection
#     # try:
#     #     with app.app_context():  # Ensure the code runs within the Flask application context
#     #         with db.engine.connect() as connection:  # Establish a connection to the database
#     #             print("PostgreSQL connection successful!")
#     # except Exception as e:
#     #     print("Failed to connect to PostgreSQL:", str(e))  # Print the error message if connection fails

#     # app.run(debug=True)

# #khadijas chat code
#     socketio.run(app, debug=True) #starts app using socketio server