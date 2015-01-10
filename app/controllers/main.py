from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import current_user, login_required

from app.forms import AddSwimForm

from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def home():
    if current_user.is_authenticated():
        return redirect(url_for('main.add_training'))
    return redirect(url_for('auth.login'))


@main.route('/about')
def about():
    return render_template('about.html', current_user=current_user)


@main.route('/training/')
@login_required
def training():
    return 'All training will be here!'


@main.route('/training/running')
@login_required
def running():
    return 'Running will be here!'


@main.route('/training/cycling')
@login_required
def cycling():
    return 'Cycling will be here!'


@main.route('/training/swimming')
@login_required
def swimming():
    return 'Swimming will be here!'


@main.route('/training/add', methods=['GET', 'POST'])
@login_required
def add_training():
    form = AddSwimForm()
    return render_template('training/add_training.html', date=datetime.now().date(),
                           form=form, current_user=current_user)