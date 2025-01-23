from flask import Flask
from flask_migrate import Migrate

# Import the configurations
from instance.config import app_config

from .claim import claims as claims_blueprint
from .extensions import database
from .users import users as users_blueprint

blueprints = [
    users_blueprint,
    claims_blueprint,
]


def create_app(config_name: str) -> Flask:
    application = Flask(
        import_name="app",
        template_folder="templates",
        static_folder="static",
        instance_relative_config=True,
    )

    application.config.from_object(app_config[config_name])
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    database.init_app(application)

    Migrate(
        app=application,
        db=database,
        directory="intron_health_migrations",
        render_as_batch=True,
    )

    register_blueprints(application)

    return application


def register_blueprints(app: Flask) -> None:
    """
    The following registers the Blueprints with the application.
    """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
