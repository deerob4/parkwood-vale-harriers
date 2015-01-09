from flask import Flask

from app.models import db


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

    # Configures application blueprints
    from app.controllers.main import main
    app.register_blueprint(main)
    
    from app.controllers.auth import auth
    app.register_blueprint(auth)
    
    from app.controllers.ajax import ajax
    app.register_blueprint(ajax)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)