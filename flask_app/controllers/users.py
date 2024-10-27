from fileinput import filename
from flask_app import ALLOWED_EXTENSIONS, app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user
import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')