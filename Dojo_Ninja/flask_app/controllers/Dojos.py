from flask_app import app
from flask import render_template, request, redirect
from flask_app.models.Dojo import Dojo
from flask_app.models.Ninja import Ninja

@app.route('/dojos')
def index():
    all_dojos = Dojo.get_all()  
    return render_template("index.html", dojos=all_dojos)

@app.route('/dojos/<int:dojo_id>')
def dojo_show(dojo_id):
    dojo = Dojo.get_by_id(dojo_id)  
    ninjas = Ninja.get_by_dojo(dojo_id)  
    return render_template('show.html', dojo=dojo, ninjas=ninjas)

@app.route('/dojos/create', methods=['POST'])
def create_dojo():
    data = request.form
    Dojo.create(data)  
    return redirect('/dojos')
