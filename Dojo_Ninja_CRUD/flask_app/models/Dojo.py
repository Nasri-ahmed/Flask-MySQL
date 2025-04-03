from flask_app.config.mysqlconnection import DB, connectToMySQL

class Dojo:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.update_at = data.get('update_at', None)
        self.ninja = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        result = connectToMySQL(DB).query_db(query)
        return [cls(row) for row in result]

    @classmethod
    def get_by_id(cls, dojo_id):
        query = "SELECT * FROM dojos WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, {"id": dojo_id})
        if result:
            return cls(result[0])
        return None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO dojos (name) VALUES (%(name)s);"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE dojos SET name = %(name)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
