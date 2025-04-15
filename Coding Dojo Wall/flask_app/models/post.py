from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Post:
    DB = "coding_dojo_wall"
    
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None  

    @classmethod
    def save(cls, data):
        query = """INSERT INTO posts (content, user_id, created_at, updated_at) 
                VALUES (%(content)s, %(user_id)s, NOW(), NOW())"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        print("Save result:", result)  
        return result

    @classmethod
    def get_all(cls):
        query = """SELECT posts.*, users.first_name, users.last_name 
                FROM posts
                JOIN users ON posts.user_id = users.id
                ORDER BY posts.created_at DESC"""
        results = connectToMySQL(cls.DB).query_db(query)
        print("Raw SQL results:", results)  
        
        posts = []
        for row in results:
            post_data = {
                'id': row['id'],
                'content': row['content'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            post = cls(post_data)
            post.creator = {
                'first_name': row['first_name'],
                'last_name': row['last_name']
            }
            posts.append(post)
        
        print("Processed posts:", posts)  
        return posts

    @classmethod
    def delete(cls, post_id):
        query = "DELETE FROM posts WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, {"id": post_id})

    @staticmethod
    def validate_post(data):
        is_valid = True
        if len(data['content'].strip()) < 1:
            flash("Post content cannot be empty", "post")
            is_valid = False
        return is_valid