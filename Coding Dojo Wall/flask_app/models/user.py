from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "coding_dojo_wall"
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return None
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        
        # Email validation
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            flash("Email already registered", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format", "register")
            is_valid = False
            
        # Name validation
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if not user['first_name'].isalpha():
            flash("First name can only contain letters", "register")
            is_valid = False
            
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if not user['last_name'].isalpha():
            flash("Last name can only contain letters", "register")
            is_valid = False
            
        # Password validation
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match", "register")
            is_valid = False
            
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if not user['email']:
            flash("Please enter your email", "login")
            is_valid = False
        if not user['password']:
            flash("Please enter your password", "login")
            is_valid = False
        return is_valid