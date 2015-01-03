from flask.ext.script import Manager, Server
from flask.ext.script.commands import Clean, ShowUrls
from app import create_app
from app.models import db

import os

app = create_app()

manager = Manager(app)
manager.add_command('server', Server(use_debugger=True))
manager.add_command('server-c9', Server(host=os.getenv('IP'), port=os.getenv('PORT'), use_debugger=True))
manager.add_command('clean', Clean())
manager.add_command('show-urls', ShowUrls())


@manager.shell
def make_shell_context():
    """Creates a Python shell with the below variables already imported."""
    return dict(app=app, db=db)


@manager.command
def createdb():
    """Creates the database, using the models in app.models.py"""
    db.create_all()

if __name__ == '__main__':
    manager.run()