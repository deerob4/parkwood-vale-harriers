from flask import Blueprint, render_template
from app.forms import NewSwimForm

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('layout.html')


@main.route('/training/swimming/new')
def new_swimming():
    form = NewSwimForm()
    return render_template('training/swimming.html', form=form)