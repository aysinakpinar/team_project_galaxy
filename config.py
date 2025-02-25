class Config(object):
    TESTING = False

class DevelopmentConfig(Config):
    DEV_DATABASE_NAME = "galaxy_db"
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:528376@localhost/{DEV_DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TEST_DATABASE_NAME = "galaxy_db_test"
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:528376@localhost/{TEST_DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
