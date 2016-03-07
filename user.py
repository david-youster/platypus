import uuid
import hashlib


def generate_salt() -> str:
    """Generate a random password salt."""
    return uuid.uuid4().hex


def generate_password_hash(password:str, salt:str) -> str:
    """Generate a password hash using the provided salt."""
    salted_password = (password + salt).encode('utf-8')
    return hashlib.sha512(salted_password).hexdigest()

