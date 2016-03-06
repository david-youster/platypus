from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)
session = scoped_session(sessionmaker(autocommit=False, 
        autoflush=False, 
        bind=engine))
Base = declarative_base()
Base.query = session.query_property()
from model import Article, User, Role

def init():
    Base.metadata.create_all(bind=engine)


def create_article(title, text):
    article = model.Article(title=title, snippet=text, text=text)
    session.add(article)
    session.commit()


def get_articles():
    return session.query(Article).all()


def get_article(article_id):
    return session.query(Article).filter(Article.id_ == article_id).first()
