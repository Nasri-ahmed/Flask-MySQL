from flask_app import app
from flask import render_template, request, redirect
from flask_app.models.Ninja import Ninja
from flask_app.models.Dojo import Dojo

@app.route('/ninjas')
def new_ninja():
    dojos = Dojo.get_all() 
    return render_template('ninja.html', dojos=dojos)

@app.route('/ninjas/create', methods=['POST'])
def create_ninja():
    Ninja.create(request.form) 
    return redirect(f"/dojos/{request.form['dojo_id']}") 
