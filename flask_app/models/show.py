from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Show:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.network = db_data['network']
        self.release_date = db_data['release_date']
        self.description = db_data['description']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.creator = None
    
    @staticmethod
    def validate_show(show):
        is_valid=True
        if len(show['title'])<3:
            flash("Title must be at least 3 characters", "show")
            is_valid=False
        if len(show['network'])<3:
            flash("Network must be at least 3 characters", "show")
            is_valid=False
        if not show['release_date']:
            flash("Release Date cannot be left blank", "show")
            is_valid=False
        if len(show['description'])<3:
            flash("Description must be at least 3 characters", "show")
        return is_valid
    
    @classmethod
    def create_show(cls, data):
        query = "INSERT INTO shows (user_id, title, network, release_date, description) \
            VALUES (%(user_id)s, %(title)s, %(network)s, %(release_date)s, %(description)s);"
        return connectToMySQL('tv_shows_schema').query_db(query, data)

    @classmethod
    def get_all_shows(cls):
        query= "SELECT * FROM shows LEFT JOIN users ON users.id = shows.user_id;"
        results = connectToMySQL('tv_shows_schema').query_db(query)
        if not results:
            results = []
            return results
        all_shows = []
        for row in results:
            user_data={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            creator = user.User(user_data)

            show_data={
                'id': row['id'],
                'title': row['title'],
                'network': row['network'],
                'release_date': row['release_date'],
                'description': row['description'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            show = cls(show_data)
            show.creator = creator
            all_shows.append(show)
        return all_shows


    @classmethod
    def get_one_show_by_id(cls, data):
        query = "SELECT * FROM shows LEFT JOIN users ON users.id = shows.user_id WHERE shows.id = %(id)s;"
        result = connectToMySQL('tv_shows_schema').query_db(query, data)
        show = cls(result[0])
        user_data={
                'id': result[0]['users.id'],
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name'],
                'email': result[0]['email'],
                'password': result[0]['password'],
                'created_at': result[0]['users.created_at'],
                'updated_at': result[0]['users.updated_at']
            }
        show.creator = user.User(user_data)
        return show

    @classmethod
    def edit_show(cls, data):
        query = "UPDATE shows SET title = %(title)s , network = %(network)s, release_date = %(release_date)s, \
            description = %(description)s WHERE id = %(id)s"
        return connectToMySQL('tv_shows_schema').query_db(query, data)

    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL('tv_shows_schema').query_db(query, data)
