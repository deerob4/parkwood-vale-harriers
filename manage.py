from flask.ext.script import Manager, Server
from flask.ext.script.commands import Clean, ShowUrls

from app import create_app
from app.models import db, User, Activity

import os

app = create_app()

manager = Manager(app)

manager.add_command('server', Server(use_debugger=True))
manager.add_command('server-codio', Server(host='0.0.0.0', port=5000, use_debugger=True))
manager.add_command('clean', Clean())
manager.add_command('show-urls', ShowUrls())

# 2258 lines on 16/3/15

@manager.shell
def make_shell_context():
    """Creates a Python shell with the below variables already imported."""
    return dict(app=app, db=db, User=User, Activity=Activity)


@manager.command
def createdb():
    """Creates the database, using the models in app.models.py"""
    db.create_all()
    return 'Database has been created.'

if __name__ == '__main__':
    manager.run()