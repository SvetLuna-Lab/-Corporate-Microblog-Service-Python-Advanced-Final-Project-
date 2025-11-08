# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .api.routes import api_bp
    from .api.errors import errors_bp

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(errors_bp)

    return app
