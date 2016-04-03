from flask import current_app
import uuid
import hashlib
import os

def generate_salt():
    """Generate a random password salt."""
    return uuid.uuid4().hex


def generate_password_hash(password, salt):
    """Generate a password hash using the provided salt."""
    salted_password = (password + salt).encode('utf-8')
    return hashlib.sha512(salted_password).hexdigest()


def get_theme_file(file):
    return os.path.join(current_app.config['theme'], file)