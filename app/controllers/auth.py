from Flask import Blueprint, render_template
from app.forms import MemberForm

auth = Blueprint('auth', __name__)

@auth.route('/register')
def register():
    form = MemberForm()
    return render_template('auth/register.html')