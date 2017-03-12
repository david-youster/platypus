from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists
from datetime import datetime
from util import generate_salt, generate_password_hash, read_config_file


class DuplicateLoginException(Exception):

    def __init__(self, message):
        super(DuplicateLoginException, self).__init__(message)

_DATABASE = 'sqlite:///platypus.db'
_DEV_DATABASE = 'sqlite:///platypus-dev.db'
database = _DEV_DATABASE if read_config_file('dev') else _DATABASE

setup = database_exists(database)
engine = create_engine(database, echo=True)
session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))
Base = declarative_base()
Base.query = session.query_property()
from model import Article, User, Role


def init():
    Base.metadata.create_all(bind=engine)
    if not setup:
        init_role_table()
        init_user_table()


def init_role_table():
    create_role('admin')
    create_role('author')
    create_role('editor')


def init_user_table():
    roles = [get_role('admin'), get_role('author')]
    salt = generate_salt()
    password_hash = generate_password_hash('admin', salt)
    create_user('admin', password_hash, salt, roles)


def create_user(login, password_hash, salt, roles):
    user = User(login=login, password_hash=password_hash, salt=salt)
    for role in roles:
        user.roles.append(role)
    session.add(user)
    try:
        session.commit()
    except IntegrityError as e:
        raise DuplicateLoginException(
            'User with login "{}" already exists'.format(login))


def create_role(name):
    role = Role(name=name)
    session.add(role)
    session.commit()


def create_article(title, snippet, text, author):
    article = Article(title=title, snippet=snippet, text=text, author=author)
    session.add(article)
    session.commit()


def get_users():
    return session.query(User).all()


def get_roles():
    return session.query(Role).all()


def get_articles():
    return session.query(Article).order_by(Article.id_.desc()).all()


def get_articles_paginated(page_number, page_size):
    query = session.query(Article).order_by(Article.id_.desc())
    return query.offset(page_number*page_size-page_size).limit(page_size).all()


def get_articles_by_author(login):
    author = get_user(login)
    return session.query(Article).filter(Article.author == author).order_by(
        Article.id_.desc()).all()


def get_user(login):
    return session.query(User).filter(User.login == login).first()


def get_role(name):
    return session.query(Role).filter(Role.name == name).first()


def get_article(article_id):
    return session.query(Article).filter(Article.id_ == article_id).first()


def get_article_latest():
    return session.query(Article).order_by(Article.id_.desc()).first()


def update_article(article_id, title, snippet, text):
    article = get_article(article_id)
    article.title, article.snippet, article.text = title, snippet, text
    article.last_edit = datetime.now()
    session.commit()


def update_user_password(
        login, old_password, new_password, confirmed_password):
    user = get_user(login)
    old_password_hash = generate_password_hash(old_password, user.salt)
    if old_password_hash != user.password_hash:
        raise Exception('Incorrect password.')
    if new_password != confirmed_password:
        raise Exception('Password and confirm password fields don\'t match.')
    user.salt = generate_salt()
    user.password_hash = generate_password_hash(
        new_password, user.salt)
    session.commit()


def delete_user(login):
    session.query(User).filter(User.login == login).delete(
        synchronize_session='evaluate')
    session.commit()


def delete_article(article_id):
    session.query(Article).filter(Article.id_ == article_id).delete(
        synchronize_session='evaluate')
    session.commit()


def get_article_count():
    return session.query(Article).count()
