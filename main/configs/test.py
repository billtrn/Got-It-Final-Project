from main.configs.base import Config


class TestConfig(Config):
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Chillduck56!@localhost/final_project_test'

    # Flask
    DEBUG = False

    TESTING = True


config = TestConfig
