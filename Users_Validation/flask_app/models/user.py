import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL, DB

EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DB).query_db(query)
        return [cls(user) for user in results]

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, {'id': user_id})
        return cls(result[0]) if result else None

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, {'email': email})
        return cls(result[0]) if result else None

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email) 
            VALUES (%(first_name)s, %(last_name)s, %(email)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
            UPDATE users 
            SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at=NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def delete(cls, user_id):
        query = "DELETE FROM users WHERE id = %(user_id)s;"
        return connectToMySQL(DB).query_db(query, {'user_id': user_id})

    @staticmethod
    def validate_user(data):
        is_valid = True

        if not data['first_name'].strip():
            flash("First name is required.", "error")
            is_valid = False
        if not data['last_name'].strip():
            flash("Last name is required.", "error")
            is_valid = False
        if not data['email'].strip():
            flash("Email is required.", "error")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Email must be valid.", "error")
            is_valid = False
        elif User.get_by_email(data['email']):
            flash("Email already exists.", "error")
            is_valid = False

        return is_valid
