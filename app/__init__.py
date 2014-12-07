from flask import Flask
from flask_assets import Environment

from app.models import db
from app import assets

from webassets.loaders import PythonLoader


def create_app():
    """Generates an instance of the app.

    This function contains all the config values
    for the different parts of the app; it returns
    a variable 'app' that contains all these values
    for use throughout the rest of the application.
    """
    app = Flask(__name__)

    # Sets configuration variables used application-wise
    app.config['SECRET_KEY'] = 'vYqTMY88zsuXSG7R4xYdPxYk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'  # May change to MySQL/PostgreSQL

    # Configures SQLAlchemy
    db.init_app(app)

    # Configures Flask-Assets, registering the asset bundles
    assets_env = Environment()
    assets_env.init_app(app)
    assets_loader = PythonLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # Configures application blueprints
    from app.controllers.main import main
    app.register_blueprint(main)
    
    from app.controllers.auth import auth
    app.register_blueprint(auth)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)