from flask import Blueprint, render_template, flash
from app.forms import AddSwimForm

from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('layout.html')


@main.route('/training/')
def training():
    return 'All training will be here!'


@main.route('/training/running')
def running():
    return 'Running will be here!'


@main.route('/training/cycling')
def cycling():
    return 'Cycling will be here!'


@main.route('/training/swimming')
def swimming():
    return 'Swimming will be here!'


@main.route('/training/add', methods=['GET', 'POST'])
def add_training():
    form = AddSwimForm()
    return render_template('training/add_training.html', date=datetime.now().date(), form=form)