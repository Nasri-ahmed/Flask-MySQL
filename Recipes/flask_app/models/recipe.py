from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = "recipes_schema"

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_minutes = data['under_30_minutes']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO recipes (name, description, instructions, under_30_minutes, date_made, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30_minutes)s, %(date_made)s, %(user_id)s);
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def get_all_with_users(cls):
        from flask_app.models.user import User  # Import local pour éviter la circularité
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for row in results:
            recipe = cls(row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            recipe.user = User(user_data)
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_by_id_with_user(cls, data):
        from flask_app.models.user import User  # Import local pour éviter la circularité
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        if result:
            recipe = cls(result[0])
            user_data = {
                "id": result[0]["users.id"],
                "first_name": result[0]["first_name"],
                "last_name": result[0]["last_name"],
                "email": result[0]["email"],
                "password": result[0]["password"],
                "created_at": result[0]["users.created_at"],
                "updated_at": result[0]["users.updated_at"]
            }
            recipe.user = User(user_data)
            return recipe
        return False

    @classmethod
    def update(cls, data):
        query = """
        UPDATE recipes
        SET name=%(name)s, description=%(description)s, instructions=%(instructions)s,
            under_30_minutes=%(under_30_minutes)s, date_made=%(date_made)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters", "recipe")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters", "recipe")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters", "recipe")
            is_valid = False
        if not recipe.get('date_made'):
            flash("Date made is required", "recipe")
            is_valid = False
        return is_valid