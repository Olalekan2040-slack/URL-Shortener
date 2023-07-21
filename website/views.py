from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, make_response, abort
import random, string
from flask_login import login_required, current_user
from io import BytesIO
import base64
from website import cache
from .models import ClickTime, URL
import qrcode

views = Blueprint('views', __name__)


url_dict = {}



@views.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

def generate_qr(data):
    qr = qrcode.QRCode(version=1,
        box_size=10, 
        border=5)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return img_base64

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_short_url()
        url_dict[short_url] = long_url

        short_url_qr = generate_qr(short_url)

        short_url = url_for('views.redirect_to_url', short_url=short_url, _external=True)
        return render_template('result.html', short_url=short_url, short_url_qr=short_url_qr)
    

    # Retrieve the current user's URLs with associated click times
    user = current_user._get_current_object()
    urls = URL.query.filter_by(user_id=user.id).all()

    click_times = []
    for url in urls:
        click_times.extend(url.click_times)

    return render_template('dashboard.html', click_times=click_times)




@views.route('/result', methods=['GET'])
@cache.cached(timeout=60)  # Cache the result for 60 seconds
@login_required
def result():
    short_url = request.args.get('short_url')

    # Retrieve the analytics data for the current URL
    url = URL.query.filter_by(short_url=short_url).first()
    click_times = url.click_times if url else []

    return render_template('result.html', short_url=short_url, click_times=click_times)





@views.route('/<string:short_url>', methods=['GET'])
@cache.cached(timeout=60)  # Cache the result for 60 seconds
@login_required
def redirect_to_url(short_url):
    long_url = url_dict.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        abort(404)


   