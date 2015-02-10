from flask import Flask
from flask.ext.login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

from app.models import db, User


def create_app():
    """Generates an instance of the app.

    This function contains all the config values
    for the different parts of the app; it returns
    a variable 'app' that contains all these values
    for use throughout the rest of the application.
    """
    app = Flask(__name__)

    # Sets the application into debug mode
    app.debug = True

    # Sets configuration variables used application-wise
    app.config['SECRET_KEY'] = 'vYqTMY88zsuXSG7R4xYdPxYk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'

    # Configures SQLAlchemy
    db.init_app(app)

    # Configures the login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Sets the login view.
    login_manager.login_message_category = 'warning'

    toolbar = DebugToolbarExtension(app)

    # Loads the current user by running a query on the id
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

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