from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, make_response, abort
import random, string
from flask_login import login_required, current_user


views = Blueprint('views', __name__)


url_dict = {}



@views.route('/home', methods=['GET', 'POST'])
def login():
    return render_template("index.html")


def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url


@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_short_url()
        url_dict[short_url] = long_url
        short_url = url_for('views.redirect_to_url', short_url=short_url, _external=True)
        return render_template('result.html', short_url=short_url)
    return render_template('dashboard.html')





@views.route('/result', methods=['GET'])
@login_required
def result():
    short_url = request.args.get('short_url')
    long_url = request.args.get('long_url')
    return render_template('result.html', short_url=short_url, long_url=long_url)



@views.route('/<string:short_url>', methods=['GET'])
def redirect_to_url(short_url):
    long_url = url_dict.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        abort(404)
