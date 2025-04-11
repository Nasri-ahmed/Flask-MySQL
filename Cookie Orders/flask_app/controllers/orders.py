from flask import render_template, redirect, request, flash
from flask_app import app
from flask_app.models.order import Order

@app.route('/')
@app.route('/cookies')
def index():
    return render_template("index.html", orders=Order.get_all())

@app.route('/cookies/new')
def new_order():
    return render_template("new_order.html")

@app.route('/cookies/create', methods=['POST'])
def create_order():
    if not Order.validate(request.form):
        return redirect('/cookies/new')
    Order.save(request.form)
    return redirect('/cookies')

@app.route('/cookies/edit/<int:id>')
def edit_order(id):
    order = Order.get_one(id)
    return render_template("edit_order.html", order=order)

@app.route('/cookies/update/<int:id>', methods=['POST'])
def update_order(id):
    data = {
        "id": id,
        "customer_name": request.form['customer_name'],
        "cookie_type": request.form['cookie_type'],
        "number_of_boxes": request.form['number_of_boxes']
    }
    if not Order.validate(data):
        return redirect(f"/cookies/edit/{id}")
    Order.update(data)
    return redirect('/cookies')
