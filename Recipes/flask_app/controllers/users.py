from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/recipes')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email({"email": request.form['email']})
    if not user:
        flash("Invalid Email/Password", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/recipes')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')