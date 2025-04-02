from flask_app.config.mysqlconnection import DB, connectToMySQL

class Ninja:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.update_at = data['update_at']
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
