from flask import render_template, redirect, session, request, flash, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect(url_for('index'))
    
    
    pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    
    
    data = {
        "first_name": request.form['first_name'].strip(),
        "last_name": request.form['last_name'].strip(),
        "email": request.form['email'].lower().strip(),
        "password": pw_hash
    }
    
   
    user_id = User.save(data)
    
    if not user_id:
        flash("A technical error occurred. Please try again.", "register")
        return redirect(url_for('index'))
  
    session['user_id'] = user_id
    flash("Your account has been created successfully!", "register_success")
    return redirect(url_for('wall'))

@app.route('/login', methods=['POST'])
def login():
   
    if not request.form['email'] or not request.form['password']:
        flash("Please fill in all fields.", "login")
        return redirect(url_for('index'))
    
  
    user = User.get_by_email({"email": request.form['email'].lower().strip()})
    
    if not user:
        flash("Invalid email or password.", "login")
        return redirect(url_for('index'))
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid email or password.", "login")
        return redirect(url_for('index'))
    
   
    session['user_id'] = user.id
    return redirect(url_for('wall'))

@app.route('/wall')
def wall():
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id': session['user_id']
    }
    
    user = User.get_by_id(data)
    if not user:
        return redirect('/logout')
    
    posts = Post.get_all()
    print("Retrieved posts:", posts)  
    
    return render_template("wall.html", user=user, posts=posts)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been successfully logged out.", "logout")
    return redirect(url_for('index'))