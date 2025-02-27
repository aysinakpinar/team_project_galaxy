# khadijas code for chatbox
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from flask_socketio import SocketIO, send


chat = Blueprint("chat", __name__, url_prefix="/chat")

@chat.route("/")
def message():
    return render_template("messages.html")

def init_socketio(socketio): #initialise socketio event handling 
    @socketio.on("message") #define en event listener for the event "message"
    def sendMessage(message): #function triggered when user sends message
        send(message, broadcast = True) #broadcast recieved message so all connected users can see




