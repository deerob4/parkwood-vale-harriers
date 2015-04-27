Parkwood Vale Harriers Running Club
===============================
This is an application for the Park Vale Harriers running club,
allowing them to choose a team of runners for their charity event. This is a project for my AS Computing coursework.

Application Features
---------------------
- [X] The ability to add runners into the application and CRUD their personal data
- [X] The ability to add times from each workout and work out the number of calories burnt
- [X] The ability to track fitness improvement over time
- [X] The ability to compare results with other runners
- [X] Individual accounts for each runner
- [X] The ability to work out the best final team

Installation
------------
The system can be installed locally in the same manner as all Flask projects:

1. Clone the repository
2. Create a virtualenv using the Python 3 interpreter - `virtualenv -p /usr/bin/python3.4 env`
3. Activate the virtualenv - `source env/bin/activate`
4. Install the package requirements - `pip install -r requirements.txt`
5. Create the database - `python manage.py createdb`
6. Run the script - `python manage.py runserver`
7. Navigate to localhost:5000 to view the application

External Libraries Used
-----------------------
A number of external libraries and packages have been used throughout the system, for both the Python and Javascript elements.

### Python
- [Flask](https://github.com/mitsuhiko/flask) - main framework
- [Flask-Login](https://github.com/maxcountryman/flask-login/) - provides auth cookie management
- [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy) - provides Flask bindings for SQLAlchemy ORM
- [Flask-WTF](https://github.com/lepture/flask-wtf) - provides Flask bindings for WTForms library

### JavaScript and CSS
- [jQuery](https://github.com/jquery/jquery)
- [Bootstrap](https://github.com/twbs/bootstrap)
- [Bootstrap Datepicker](https://github.com/eternicode/bootstrap-datepicker)
- [Chart.js](https://github.com/nnnick/Chart.js/)
- [DataTables](https://github.com/DataTables/DataTables)
- [pickadate](https://github.com/amsul/pickadate.js/)
- [Animate.css](https://github.com/daneden/animate.css)