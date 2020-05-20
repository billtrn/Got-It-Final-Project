from main.configs.base import Config


class DevelopmentConfig(Config):
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Chillduck56!@localhost/final_project_dev'

    # Flask
    DEBUG = True

    TESTING = False


config = DevelopmentConfig
