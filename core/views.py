from flask import abort, render_template, request
<<<<<<< HEAD
=======
from flask_login import login_required
>>>>>>> d422bdd7b6af01d9eb2821b37b5e9ad75cdd24b5

from . import app
from .models import User


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/user/')
def user_new():
    return render_template('user.html', user=User(), edit=True)


@app.route('/user/<int:id>/')
@login_required
def user(id):
    try:
        user = User.get(id=id)
    except User.DoesNotExist:
        abort(404, 'User not found.')
    return render_template('user.html', user=user,
                           edit=('edit' in request.args))
