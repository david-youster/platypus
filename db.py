from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists
from util import generate_salt, generate_password_hash, read_config_file

config = read_config_file()

_DATABASE = 'sqlite:///{}.db'.format(config['title'])

setup = database_exists(_DATABASE)
engine = create_engine(_DATABASE, echo=True)
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
    session.commit()


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
