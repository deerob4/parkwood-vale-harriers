import os

from flask import Flask
from app.models import db


def create_app():
    """
    Application factory that creates the application instance.
    """

    app = Flask(__name__)

    # Sets configuration variables used application-wise
    app.config['SECRET_KEY'] = 'vYqTMY88zsuXSG7R4xYdPxYk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'

    # Configures SQLAlchemy
    db.init_app(app)

    # Configures application blueprints
    from app.controllers.main import main
    app.register_blueprint(main)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()