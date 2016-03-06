from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


class User(Base):
    __tablename__ = 'User'
    id_ = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    salt = Column(String)
    password_hash = Column(String)
    admin = Column(Boolean)
    articles = relationship('Article', backref='User')

    def __repr__(self):
        return '<User(login={}, salt={}, password_hash={}, admin={})>'.format(
                self.login, self.salt, self.password_hash, self.admin)


class Article(Base):
    __tablename__ = 'Article'
    id_ = Column(Integer, primary_key=True)
    title = Column(String)
    snippet = Column(String)
    text = Column(String)
    publication_date = Column(DateTime, default=datetime.now())
    last_edit = Column(DateTime, default=datetime.now())
    author_id = Column(Integer, ForeignKey('User.id_'))

    def __repr__(self):
        return '<Article(title="{}", snippet="{}", text="{}")>'.format(
                self.name, self.snippet, self.text)

