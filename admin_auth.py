from flask_login import UserMixin
from functools import wraps
from flask_login import current_user
from flask import abort

class Admin(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username
    
    @staticmethod
    def get(user_id):
        # For demo purposes, we have one admin
        if user_id == '1':
            return Admin('1', 'admin')
        return None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.username != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function