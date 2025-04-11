from flask_app.config.mysqlconnection import connectToMySQL,DB
from flask import flash


class Order:
    def __init__(self, data):
        self.id = data['id']
        self.customer_name = data['customer_name']
        self.cookie_type = data['cookie_type']
        self.number_of_boxes = data['number_of_boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL(DB).query_db(query)
        return [cls(row) for row in results]

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO orders (customer_name, cookie_type, number_of_boxes)
        VALUES (%(customer_name)s, %(cookie_type)s, %(number_of_boxes)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, {"id": id})
        return cls(result[0]) if result else None

    @classmethod
    def update(cls, data):
        query = """
        UPDATE orders
        SET customer_name = %(customer_name)s,
            cookie_type = %(cookie_type)s,
            number_of_boxes = %(number_of_boxes)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['customer_name']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
        if len(data['cookie_type']) < 2:
            flash("Cookie type must be at least 2 characters.")
            is_valid = False
        if not str(data['number_of_boxes']).isdigit() or int(data['number_of_boxes']) < 0:
            flash("Number of boxes must be a positive number.")
            is_valid = False
        return is_valid
