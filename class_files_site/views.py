from flask import Blueprint, render_template
from .models import User, db
import psycopg2


conn = psycopg2.connect("dbname='lessons' user='postgres' host='localhost' password='password'")


views = Blueprint('views', __name__, template_folder='templates')

@views.route('/', methods=['GET', 'POST'])
def main():
    user = User('asd', 'zaq1@WSX')
    db.session.add(user)
    db.session.commit()
    return render_template('foo.html')
