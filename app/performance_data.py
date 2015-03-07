from calendar import month_name
from flask.ext.login import current_user
from app.models import db, Activity, User


def performance_data(month):
    months = [month_name[x].lower() for x in range(1, 13)]
    all_activities = Activity.query.filter_by(user_id=current_user.get_id()).all()
    all_runs = Activity.query.filter_by(user_id=current_user.get_id(), sport='running').all()
    all_cycles = Activity.query.filter_by(user_id=current_user.get_id(), sport='cycling').all()
    all_swims = Activity.query.filter_by(user_id=current_user.get_id(), sport='swimming').all()

    month_map = dict(zip(months, range(1, 13)))  # Creates a dict with month names and values - Jan: 1 etc

    calorie_goal = 40000
    hour_goal = 100

    # [0] contains the calories burned; [1] contains the hours
    total_run_data = [0, 0]
    total_cycle_data = [0, 0]
    total_swim_data = [0, 0]

    run_list = [{'id': run.id, 'date': run.date.strftime('%d %b %y'), 'effigy': run.effigy, 'calories': run.calories, 'hours': run.hours, 'opinion': run.opinion} for run in all_runs if run.date.month == month_map[month]]

    cycle_list = [{'id': cycle.id, 'date': cycle.date.strftime('%d %b %y'), 'effigy': cycle.effigy, 'calories': cycle.calories, 'hours': cycle.hours, 'opinion': cycle.opinion} for cycle in all_cycles if cycle.date.month == month_map[month]]

    swim_list = [{'id': swim.id, 'date': swim.date.strftime('%d %b %y'), 'effigy': swim.effigy, 'calories': swim.calories, 'hours': swim.hours, 'opinion': swim.opinion} for swim in all_swims if swim.date.month == month_map[month]]

    print(run_list, cycle_list, swim_list)

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