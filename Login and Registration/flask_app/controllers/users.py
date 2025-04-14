from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    User.register(request.form)
    flash("Your account has been created successfully. Please log in.", "success")
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_by_email({'email': request.form['email']})
    session['user_id'] = user.id
    return redirect('/success')

@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('success.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
