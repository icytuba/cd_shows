from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @staticmethod
    def validate_reg(user):
        is_valid=True
        if User.get_user_by_email(user):
            flash("Email already associated with existing account", "register")
            is_valid=False
        if len(user['first_name'])<2:
            flash("First name must be at least 2 characters", "register")
            is_valid=False
        if len(user['last_name'])<2:
            flash("Last name must be at least 2 characters", "register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address")
            is_valid=False
        if len(user['password'])<6:
            flash("Password must be at least 6 characters", "register")
            is_valid=False
        if user['password'] != user['conf_pw']:
            flash("Passwords must match", "register")
            is_valid=False
        return is_valid

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('tv_shows_schema').query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('tv_shows_schema').query_db(query, data)
        if len(result)<1:
            return False
        return cls(result[0])
