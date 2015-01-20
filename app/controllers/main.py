from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import current_user, login_required

from app.forms import AddSwimForm
from app.models import User

from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def home():
    if current_user.is_authenticated():
        return redirect(url_for('main.add_training'))
    return redirect(url_for('auth.login'))


@main.route('/training/')
@login_required
def training():
    return 'All training will be here!'


@main.route('/runners/<runnername>')
@login_required
def runners(runnername):
    user = User.query.filter_by(username=runnername).first_or_404()
    if user.username == current_user.username:
        return render_template('profiles/own_profile.html', current_user=current_user)
    return 'no permissions...', 402


@main.route('/training/add', methods=['GET', 'POST'])
@login_required
def add_training():
    form = AddSwimForm()
    return render_template('training/add_training.html', date=datetime.now().date(),
                           form=form, current_user=current_user)