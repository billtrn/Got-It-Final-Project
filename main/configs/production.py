from main.configs.base import Config


class ProductionConfig(Config):
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Chillduck56!@localhost/final-project-prod'

    # Flask
    DEBUG = False

    TESTING = False


config = ProductionConfig
