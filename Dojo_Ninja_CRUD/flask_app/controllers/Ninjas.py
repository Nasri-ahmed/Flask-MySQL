from flask_app import app
from flask import render_template, request, redirect

@app.route('/ninjas')
def new_ninja():
    from flask_app.models.Dojo import Dojo
    dojos = Dojo.get_all()
    return render_template('ninja.html', dojos=dojos)

@app.route('/ninjas/create', methods=['POST'])
def create_ninja():
    from flask_app.models.Ninja import Ninja
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "age": request.form['age'],
        "dojo_id": request.form['dojo_id']
    }
    Ninja.create(data)
    return redirect(f"/dojos/{request.form['dojo_id']}") 

@app.route('/ninjas/delete/<int:ninja_id>')
def delete_ninja(ninja_id):
    from flask_app.models.Ninja import Ninja
    ninja = Ninja.get_by_id(ninja_id)  # Optional: Check if the ninja exists
    dojo_id = ninja.dojo_id if ninja else None
    Ninja.delete(ninja_id)
    return redirect(f"/dojos/{dojo_id}")

@app.route('/ninjas/edit/<int:ninja_id>')
def edit_ninja(ninja_id):
    from flask_app.models.Ninja import Ninja
    from flask_app.models.Dojo import Dojo
    
    ninja = Ninja.get_by_id(ninja_id)
    dojos = Dojo.get_all()
    return render_template('edit_ninja.html', ninja=ninja, dojos=dojos)

@app.route('/ninjas/update/<int:ninja_id>', methods=['POST'])
def update_ninja(ninja_id):
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "age": request.form['age'],
        "dojo_id": request.form['dojo_id'],
        "id": ninja_id
    }
    
    from flask_app.models.Ninja import Ninja
    Ninja.update(data)
    return redirect(f"/dojos/{data['dojo_id']}")
