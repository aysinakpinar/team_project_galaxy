# 🌌 Galaxy Project

This repository contains the seed codebase for the **Galaxy** project built with **Python**, **Flask**, **SQLAlchemy**, and **Pytest**. It includes features like workout planning, real-time chat, Google Maps integration, and an AI chatbot.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/aysinakpinar/team_project_galaxy.git
```

### 2. Set Up Virtual Environment

```bash
python -m venv galaxy_venv
source galaxy_venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install playwright
```

> **Note**: If you encounter a `ModuleNotFoundError`, deactivate and reactivate your virtual environment. If issues persist, contact your coach.

---

## 🔐 Environment Variables

This project uses a `.env` file to store sensitive environment variables like the **Google Maps API key**.

### 1. Create a `.env` File in the Project Root

```bash
touch .env
```

### 2. Add Your Google Maps API Key

Inside the `.env` file, add:

```env
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### 3. Load Environment Variables

Ensure you’re using a library like `python-dotenv` (included in `requirements.txt`) and have this in your config or app setup:

```python
from dotenv import load_dotenv
load_dotenv()
```

Then, access the key like:

```python
import os
api_key = os.getenv("GOOGLE_MAPS_API_KEY")
```

> Never commit your `.env` file to version control. Add it to `.gitignore`.

---

## ⚙️ Database Setup

### 1. Create Databases

```bash
createdb galaxy_db
createdb galaxy_db_test
```

### 2. Run Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. Seed the Databases

```bash
python seeds/0_user_seed.py
python seeds/1_friendship_seed.py
python seeds/2_user_point_seed.py
python seeds/3_exercise_seed.py
python seeds/4_quote_seed.py
python seeds/5_gym_seed.py
python seeds/6_workout_seed.py
python seeds/7_workout_exercise_seed.py
```

---

## 🧠 AI Chatbot Setup (Mistral 7B)

Uses [Mistral 7B](https://ollama.com/library/mistral) via [Ollama](https://ollama.com/).

### Instructions

1. **Install Ollama**:
   ```bash
   brew install ollama
   ```

2. **Start Ollama**:
   ```bash
   ollama start
   ```

3. **Download the Mistral Model**:
   ```bash
   ollama pull mistral:7b-instruct-q4_K_M
   ```

4. **Serve the Model**:
   ```bash
   ollama serve
   ```

5. **Run the Flask App in a Separate Terminal**:
   ```bash
   flask run
   ```

> Keep `ollama serve` running. The chatbot may respond with some delay (~9s).

---

## 💬 Real-Time Chat (Socket.IO)

### Install Required Packages

```bash
pip install flask-socketio python-socketio eventlet
```

These are already included in `requirements.txt`.

### Features

- Real-time private messaging
- Active user tracking
- Automatic room joining/switching
- SocketIO server integration (`app.py`)
- Interface handled by `messages.html` and `chat.py`

Use this to start your app:

```python
socketio.run(app, debug=True)
```

---

## 📁 Project Structure

```text
.
├── README.md
├── .env                    # Environment variables (not committed)
├── app.py                  # Entry point
├── blueprints/             # Business logic
├── config.py               # Environment config
├── extension.py
├── forms/                  # User input forms
├── models/                 # Database tables
├── requirement.txt
├── static/                 # Static assets (CSS/JS)
├── templates/              # HTML templates
├── tests/                  # Test suite
└── venv/                   # Virtual environment
```

---

## 🧪 Run Tests

```bash
pytest -sv
```

---

## 🖥️ Run the App

```bash
python app.py
```

Then open: [http://127.0.0.1:5000/home](http://127.0.0.1:5000/home)

---


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


