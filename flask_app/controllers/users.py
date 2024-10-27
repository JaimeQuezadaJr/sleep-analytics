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

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/user/edit/<int:id>')
def edit_user_page(id):
    data = {
            "id":id,
    }
    return render_template('edit_profile.html', user = user.User.get_user_by_id(data))

@app.route('/register_page')
def register_page():
    return render_template('register.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/register', methods = ['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect('/register_page')
    if 'profile_pic' not in request.files:
        flash('No file part in form', 'register')
        return redirect("/register_page")
    file = request.files['profile_pic']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No file uploaded', 'register')
        return redirect("/register_page")
    # If invalid file type
    if not allowed_file(file.filename):
        flash("File type is incorrect. Only .png, .jpg, .jpeg, .gif files allowed", 'register')
        return redirect("/register_page")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(os.path.join(app.root_path,'static','images', filename))
        # Save the file itself in the /static/images folder
        file.save(os.path.join(app.root_path,'static','images', filename)) 
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "city": request.form['city'],
            "state": request.form['state'],
            "email": request.form['email'],
            "password": pw_hash,
            "profile_pic": filename
        }
        user_id = user.User.save_user(data)
        session['user_id'] = user_id
    return redirect("/dashboard")