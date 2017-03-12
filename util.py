from flask import current_app, url_for
import uuid
import hashlib
import binascii
import json
import os


class Pager:

    def __init__(self, current_page, total_pages):
        self.current_page = int(current_page)
        self.total_pages = int(total_pages)

    def __str__(self):
        return '{} {} {}'.format(
            self.render_previous_link(),
            self.render_page_number(),
            self.render_next_link())

    def render_previous_link(self):
        if self.current_page <= 1:
            return ''
        href = url_for('index', page=self.current_page-1)
        return '<a href="{}">Previous</a>'.format(href)

    def render_page_number(self):
        return '{}/{}'.format(self.current_page, self.total_pages)

    def render_next_link(self):
        if self.current_page >= self.total_pages:
            return ''
        href = url_for('index', page=self.current_page+1)
        return '<a href="{}">Next</a>'.format(href)


def generate_salt():
    """Generate a random password salt."""
    return uuid.uuid4().hex


def generate_password_hash(password, salt):
    """Generate a password hash using the provided salt."""
    salted_password = (password + salt).encode('utf-8')
    return hashlib.sha512(salted_password).hexdigest()


def generate_secret_key():
    return str(binascii.hexlify(os.urandom(24)))


def get_theme_file(file):
    return os.path.join(current_app.config['theme'], file)


def read_config_file(key):
    with open('config.json', 'r') as f:
        return json.loads(f.read())[key]


def save_config_file(config):
    with open('config.json', 'w') as f:
        f.write(json.dumps(
            config,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')))
