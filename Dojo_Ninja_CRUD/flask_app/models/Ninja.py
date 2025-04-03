from flask_app.config.mysqlconnection import DB, connectToMySQL

class Ninja:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.update_at = data.get('update_at', None)
        self.dojo_id = data['dojo_id']

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO ninjas (first_name, last_name, age, dojo_id) 
            VALUES (%(first_name)s, %(last_name)s, %(age)s, %(dojo_id)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_by_dojo(cls, dojo_id):
        query = "SELECT * FROM ninjas WHERE dojo_id = %(dojo_id)s;"
        results = connectToMySQL(DB).query_db(query, {"dojo_id": dojo_id})
        return [cls(row) for row in results] if results else []

    @classmethod
    def get_by_id(cls, ninja_id):
        query = "SELECT * FROM ninjas WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, {"id": ninja_id})
        if result:
            return cls(result[0])
        return None

    @classmethod
    def delete(cls, ninja_id):
        query = "DELETE FROM ninjas WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, {"id": ninja_id})

    @classmethod
    def update(cls, data):
        query = """
            UPDATE ninjas
            SET first_name = %(first_name)s, last_name = %(last_name)s, age = %(age)s, dojo_id = %(dojo_id)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(DB).query_db(query, data)
