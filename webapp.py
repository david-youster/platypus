from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import model

app = Flask(__name__)

engine = create_engine('sqlite:///test.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, 
        autoflush=False, 
        bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', articles=get_articles())


@app.route('/article/<article_id>')
def article(article_id):
    article = get_article(article_id)
    return render_template('article.html', article=article)


@app.route('/addarticle')
def add_article():
    return render_template('addcontent.html', title='Add Content')


@app.route('/addarticle', methods=['POST'])
def add_article_post():
    create_article(request.form['title'], request.form['text'])
    return redirect('/addarticle')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', title='Error', error=str(error))


def create_article(title, text):
    article = model.Article(title=title, snippet=text, text=text)
    db_session.add(article)
    db_session.commit()


def get_articles():
    return db_session.query(model.Article).all()


def get_article(article_id):
    return None

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
