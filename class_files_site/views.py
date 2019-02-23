from flask import Blueprint, render_template


views = Blueprint('views', __name__, template_folder='templates')

@views.route('/', methods=['GET', 'POST'])
def main():
    return render_template('home.html')