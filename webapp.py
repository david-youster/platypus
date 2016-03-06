from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html', 
            title='Home', 
            articles=db.get_articles())


@app.route('/article/<article_id>')
def article(article_id):
    article = db.get_article(article_id)
    return render_template('article.html', article=article)


@app.route('/addarticle')
def add_article():
    return render_template('addcontent.html', title='Add Content')


@app.route('/addarticle', methods=['POST'])
def add_article_post():
    db.create_article(request.form['title'], request.form['text'])
    return redirect('/addarticle')


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', title='Error', error=str(error))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    db.init()
    app.run(debug=True)
