from calendar import month_name
from flask.ext.login import current_user
from app.models import db, Activity, User


def performance_data(month):
    """Creates a dictionary object with training data

    This function is used throughout the system to create
    a collection of a particular user's training activities.
    It performs several queries to the db and uses a number
    of loops and list comprehensions in order to
    """

    # Creates a list of months - January, February, etc.
    months = [month_name[x].lower() for x in range(1, 13)]

    # Queries the db for all of the user's activities.
    all_activities = Activity.query.filter_by(user_id=current_user.get_id()).all()

    # Queries the db for all of the user's different activities.
    all_runs = Activity.query.filter_by(user_id=current_user.get_id(), sport='running').all()
    all_cycles = Activity.query.filter_by(user_id=current_user.get_id(), sport='cycling').all()
    all_swims = Activity.query.filter_by(user_id=current_user.get_id(), sport='swimming').all()

    # Creates a dict with month names and values - Jan: 1 etc.
    month_map = dict(zip(months, range(1, 13)))

    # Sets the total monthly calorie and hourly goal.
    calorie_goal = 40000
    hour_goal = 100

    # [0] contains the calories burned; [1] contains the hours.
    total_run_data = [0, 0]
    total_cycle_data = [0, 0]
    total_swim_data = [0, 0]

    # Generates a list containing the data for every running activity using the above queries.
    run_list = [{'id': run.id, 'date': run.date.strftime('%d %b %y'), 'effigy': run.effigy, 'calories': run.calories,
                 'start': run.start, 'finish': run.finish, 'hours': run.hours, 'opinion': run.opinion} for run in
                all_runs if run.date.month == month_map[month]]

    cycle_list = [
        {'id': cycle.id, 'date': cycle.date.strftime('%d %b %y'), 'effigy': cycle.effigy, 'calories': cycle.calories,
         'start': cycle.start, 'finish': cycle.finish, 'hours': cycle.hours, 'opinion': cycle.opinion} for cycle in
        all_cycles if cycle.date.month == month_map[month]]

    swim_list = [
        {'id': swim.id, 'date': swim.date.strftime('%d %b %y'), 'effigy': swim.effigy, 'calories': swim.calories,
         'start': swim.start, 'finish': swim.finish, 'hours': swim.hours, 'opinion': swim.opinion} for swim in all_swims
        if swim.date.month == month_map[month]]

    # Updates the total_sport_data variables with the total calories and hours of each sport.
    for run in all_runs:
        if run.date.month == month_map[month]:
            total_run_data[0] += run.calories
            total_run_data[1] += run.hours

    for cycle in all_cycles:
        if cycle.date.month == month_map[month]:
            total_cycle_data[0] += cycle.calories
            total_cycle_data[1] += cycle.hours

    for swim in all_swims:
        if swim.date.month == month_map[month]:
            total_swim_data[0] += swim.calories
            total_swim_data[1] += swim.hours

    # Takes all the above data and creates a large dict structure by which it can be accessed.
    user_data = {
        'progress_data': {
            'running': {
                'calories': {
                    'value': total_run_data[0],
                    'percentage': total_run_data[0] / calorie_goal * 100
                },
                'hours': {
                    'value': total_run_data[1],
                    'percentage': total_run_data[1] / hour_goal * 100
                }
            },
            'cycling': {
                'calories': {
                    'value': total_cycle_data[0],
                    'percentage': total_cycle_data[0] / calorie_goal * 100
                },
                'hours': {
                    'value': total_cycle_data[1],
                    'percentage': total_cycle_data[1] / hour_goal * 100
                }
            },
            'swimming': {
                'calories': {
                    'value': total_swim_data[0],
                    'percentage': total_swim_data[0] / calorie_goal * 100
                },
                'hours': {
                    'value': total_swim_data[1],
                    'percentage': total_swim_data[1] / hour_goal * 100
                }
            }
        },
        'sport_data': {
            'running': run_list,
            'swimming': swim_list,
            'cycling': cycle_list
        },
        'month': month.title()
    }

    return user_data