from flask import Blueprint, render_template, flash
from app.forms import AddSwimForm

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('layout.html')


@main.route('/swimming/add', methods=['GET', 'POST'])
def add_swim():
    form = AddSwimForm()
    if form.validate_on_submit():
        print('woo!')
    for error in form.errors.items():
        flash(error[1][0], 'warning')
    return render_template('training/swimming.html', form=form)