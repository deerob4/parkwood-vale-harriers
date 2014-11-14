from flask.ext.script import Manager, Server
from flask.ext.script.commands import Clean, ShowUrls
from app import create_app
from app.models import db

app = create_app()

manager = Manager(app)
manager.add_command('server', Server(use_debugger=True))
manager.add_command('server-nitro', Server(host='0.0.0.0', port=8080, use_debugger=True))
manager.add_command('clean', Clean())
manager.add_command('show-urls', ShowUrls())


@manager.shell
def make_shell_context():
    """
    Creates a Python shell with the below variables already imported.
    """
    return dict(app=app, db=db)


@manager.command
def create_db():
    """
    Creates the database, using the models in app.models.py
    """
    db.create_all()

if __name__ == '__main__':
    manager.run()