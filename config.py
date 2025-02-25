import os

# PostgreSQL Database Configuration
HOSTNAME = "127.0.0.1"        # Database hostname or IP address
PORT = 5432                   # Database port (default for PostgreSQL is 5432)
USERNAME = "postgres"        # Database username
PASSWORD = "1234"        # Database password
DATABASE = "galaxy_orm_db"          # Name of the database

# SQLAlchemy Database URI
# This is the connection string used by SQLAlchemy to connect to the PostgreSQL database.
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"

# Other SQLAlchemy Configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking system (recommended to reduce overhead)

# Flask-WTF Configuration
WTF_CSRF_ENABLED = False      # Disable Cross-Site Request Forgery (CSRF) protection (not recommended in production)
SECRET_KEY = 'default_key'    # Secret key used for session management and other cryptographic purposes