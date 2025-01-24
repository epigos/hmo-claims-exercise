import os


class Config:
    """
    Common configurations
    """

    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
    ASSETS_DEBUG = True
    CSRF_ENABLED = True
    test_directory_path = os.path.dirname(os.path.realpath(__file__))


class IntronConfig(Config):
    """
    Configurations
    """

    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        Config.test_directory_path, "intron_db.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_BINDS = {
        "test": "sqlite:///" + os.path.join(Config.test_directory_path, "intron_db.db")
    }


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        Config.test_directory_path, "test.db"
    )
    WTF_CSRF_ENABLED = False


app_config = {
    "config": IntronConfig,
    "testing": TestingConfig,
}
