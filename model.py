from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


user_role = Table('UserRole', Base.metadata,
        Column('user_id', Integer, ForeignKey('User.id_')),
        Column('role_id', Integer, ForeignKey('Role.id_')))


class User(Base):
    __tablename__ = 'User'
    id_ = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    salt = Column(String)
    password_hash = Column(String)
    articles = relationship('Article', backref='User')
    roles = relationship('Role', secondary=user_role, backref='users')

    def __repr__(self):
        return '<User(login="{}", password_hash="{}",  salt="{}")>'.format(
                self.login, self.password_hash, self.salt)


class Role(Base):
    __tablename__ = 'Role'
    id_ = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return '<Role(name="{}")>'.format(self.name)


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
        r = '<Article(title="{}", snippet="{}", text="{}", author={})>'
        return r.format(self.name, self.snippet, self.text, self.author_id)

