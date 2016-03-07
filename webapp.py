from flask import Flask, render_template, request, redirect, session
from functools import wraps
from user import generate_password_hash
import db

app = Flask(__name__)
app.secret_key = '9l2+y#cit1)yvm4douh_uv=wh1cm0w3nevpv7v(8$e*qan8n3+'


def check_admin(function):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        if 'admin' in session['roles']:
            return function(*args, **kwargs)
        return redirect('/index')
    return wrapped_function


def check_author(function):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        if 'author' in session['roles']:
            return function(*args, **kwargs)
        return redirect('/index')
    return wrapped_function


def check_anon(function):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        if 'logged_in' in session:
            return  redirect('/index')
        return function(*args, **kwargs)
    return wrapped_function


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html', 
            title='Home',
            articles=db.get_articles())


@app.route('/login')
@check_anon
def login():
    return render_template('login.html', title='Login')


@app.route('/login', methods=['POST'])
@check_anon
def login_post():
    log_in_user(request.form['login-name'], request.form['login-password'])
    return redirect('/index')


def log_in_user(login, password):
    user = db.get_user(login)
    if credentials_ok(user, password):
        session['logged_in'] = user.login


def credentials_ok(user, password):
    if user:
        password_hash = generate_password_hash(password, user.salt)
        if password_hash == user.password_hash:
            return True
    return False


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
