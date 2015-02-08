from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask.ext.login import current_user, login_required

from app.models import User, Activity, db

from datetime import datetime
from random import randint

import re

main = Blueprint('main', __name__)

current_date = datetime.now().date()


@main.route('/')
def home():
    if current_user.is_authenticated():
        return redirect(url_for('main.add_training'))
    return redirect(url_for('auth.login'))


@main.route('/training/')
@login_required
def training():
    return 'All training will be here!'


@main.route('/profiles/<username>', methods=['GET', 'POST'])
@login_required
def profiles(username):
    if request.method == 'POST':
        def update_user(user, element, redirect_user):
            db.session.add(user)
            db.session.commit()
            flash('Your %s has been successfully changed!' % element, 'success')
            if redirect_user:
                return redirect(url_for('main.profiles', username=user.username))

        def validation_error(message):
            flash(message, 'warning')
            return redirect(url_for('main.profiles', username=current_user.username))

        user = User.query.filter_by(id=current_user.get_id()).first()
        
        # If the user tried to change their name
        if request.form.get('name'):
            only_letters = re.compile(r'^[A-Za-z\-" "]*$')
            if only_letters.match(request.form.get('name')):
                user.name = request.form.get('name').title()
                user.username = request.form.get('name').lower().replace(' ', '').replace('-', '') + str(randint(1, 10))
                update_user(user, 'name and username', False)
                return redirect(url_for('main.profiles', username=user.username))
            else:
                validation_error('Your name may only contain letters.')

        # If the user tried to change their email
        elif request.form.get('email'):
            valid_email = re.compile(r'^.+@[^.].*\.[a-z]{2,10}$')
            if valid_email.match(request.form.get('email')):
                user.email = request.form.get('email')
                update_user(user, 'email', True)
            else:
                validation_error('You must enter a valid email.')

        # If the user tried to change their phone number
        elif request.form.get('phone'):
            valid_phone = re.compile(
                r'^\s*\(?(020[78]\)? ?[1-9][0-9]{2} ?[0-9]{4})|(0[1-8][0-9]{3}\)? ?[1-9][0-9]{2} ?[0-9]{3})\s*$')
            if valid_phone.match(request.form.get('phone')):
                user.phone = request.form.get('phone')
                update_user(user, 'phone number', True)
            else:
                validation_error('You must enter a valid UK phone number.')

        # If the user tried to change their dob
        elif request.form.get('dob'):
            user.dob = request.form.get('dob')
            update_user(user, 'date of birth', True)

        # If the user tried to change their weight
        elif request.form.get('weight'):
            check_integer = re.compile(r'^-?[0-9]+$')
            if not check_integer.match(request.form.get('weight')):
                validation_error('You must enter a number.')
            elif not 10 <= int(request.form.get('weight')) <= 100:
                validation_error('Your weight must be between 10kg - 100kg.')
            else:
                user.weight = request.form.get('weight')
                update_user(user, 'weight', True)

    possible_user = User.query.filter_by(username=username).first_or_404()
    if current_user.username == possible_user.username:
        activity_number = len(Activity.query.filter_by(user_id=current_user.get_id()).all())
        total_users = len(User.query.all())

        return render_template('profiles/own_profile.html', current_user=current_user, activity_number=activity_number,
                               total_users=total_users)
    abort(403)

    return redirect(url_for('main.profiles', username=current_user.username))


@main.route('/training/add', methods=['GET', 'POST'])
@login_required
def add_training():
    activities = Activity.query.filter_by(user_id=current_user.get_id(), date=current_date).all()
    total_calories = 0
    for activity in activities:
        total_calories += activity.calories
    return render_template('training/add_training.html', date=current_date,
                           current_user=current_user, activities=activities, total_calories=total_calories)