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

# Now visithttp://127.0.0.1:5000/index in your browser
###### Install dependencies in requirement.txt

###### Folder structure
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
flask db init
flask db migrate -m "Initial migration"
flask db upgrade