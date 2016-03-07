from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists
from user import generate_salt, generate_password_hash

_DATABASE = 'sqlite:///test.db'

engine = create_engine(_DATABASE, echo=True)
session = scoped_session(sessionmaker(autocommit=False, 
        autoflush=False, 
        bind=engine))
Base = declarative_base()
Base.query = session.query_property()
from model import Article, User, Role


def init():
    Base.metadata.create_all(bind=engine)
    if not database_exists(_DATABASE):
        init_role_table()
        init_user_table()


def init_role_table():
    create_role('admin')
    create_role('author')


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


def create_article(title, text):
    article = Article(title=title, snippet=text, text=text)
    session.add(article)
    session.commit()


def get_users():
    return session.query(User).all()


def get_roles():
    return session.query(Role).all()


def get_articles():
    return session.query(Article).all()


def get_user(login):
    return session.query(User).filter(User.login == login).first()


def get_role(name):
    return session.query(Role).filter(Role.name == name).first()


def get_article(article_id):
    return session.query(Article).filter(Article.id_ == article_id).first()

