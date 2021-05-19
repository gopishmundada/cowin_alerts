from config import config_by_name
from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate

from .models import db

migrate = Migrate()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config_by_name[config_name])
    app.jinja_env.cache = {}

    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)
    mail.init_app(app)

    with app.app_context():
        from . import index

        app.register_blueprint(index.index_bp)

        return app
