from flask import render_template, request, redirect, url_for, flash, session
from flask_app import app
from flask_app.models.user import User

@app.route('/')
def read_all():
    users = User.get_all()
    return render_template("index.html", users=users)

@app.route('/user/new')
def new_user():
    return render_template("new_user.html")

@app.route('/users/create', methods=['POST'])
def create_user():
    session['form_data'] = request.form

    if not User.validate_user(request.form):
        return redirect(url_for('new_user'))

    session.pop('form_data', None)
    User.save(request.form)
    return redirect(url_for('read_all'))

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.get_by_id(user_id)
    return render_template("show.html", user=user) if user else redirect(url_for('read_all'))

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.get_by_id(user_id)
    return render_template("edit.html", user=user) if user else redirect(url_for('read_all'))

@app.route('/users/update', methods=['POST'])
def update_user():
    user_id = request.form['id']
    User.update(request.form)
    return redirect(url_for('show_user', user_id=user_id))

@app.route('/user/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    User.delete(user_id)
    return redirect(url_for('read_all'))
