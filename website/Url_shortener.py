from flask import Flask, render_template, request, redirect, Blueprint
import string, random

url_shortener = Blueprint('url_shortener', __name__)
# In-memory dictionary to store shortened URLs
url_dict = {}

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

# @app.route('/', methods=['GET', 'POST'])
def shorten_url():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_short_url()
        url_dict[short_url] = long_url
        return render_template('result.html', short_url=short_url)
    return render_template('index.html')

# @app.route('/<string:short_url>')
def redirect_to_long_url(short_url):
    long_url = url_dict.get(short_url)
    if long_url:
        return redirect(long_url)
    return 'Invalid or expired URL'
