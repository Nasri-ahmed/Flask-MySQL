from flask_app.config.mysqlconnection import connectToMySQL, DB
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re, datetime

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        hashed_pw = bcrypt.generate_password_hash(data['password'])
        data = {
            **data,
            "password": hashed_pw
        }
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls(results[0])
        return None

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls(results[0])
        return None

    @staticmethod
    def validate_register(data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.")
            is_valid = False
        elif User.get_by_email({"email": data['email']}):
            flash("Email already exists.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if not any(char.isupper() for char in data['password']) or not any(char.isdigit() for char in data['password']):
            flash("Password must have at least one uppercase letter and one number.")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        user = User.get_by_email({"email": data['email']})
        if not user:
            flash("Invalid email.")
            return False
        if not bcrypt.check_password_hash(user.password, data['password']):
            flash("Invalid password.")
            return False
        return user
