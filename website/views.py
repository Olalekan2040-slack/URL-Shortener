from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, make_response, abort



views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
def login():
    return render_template("index.html")
