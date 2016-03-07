from flask import Flask, render_template, request, redirect, session
from functools import wraps
from util import generate_password_hash
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


@app.route('/login', methods=['GET','POST'])
@check_anon
def login():
    if request.method == 'GET':
        return login_get()
    return login_post()


def login_get():
    return render_template('login.html', title='Login')


def login_post():
    log_in_user(request.form['login-name'], request.form['login-password'])
    return redirect('/index')


def log_in_user(login, password):
    user = db.get_user(login)
    if credentials_ok(user, password):
        session['logged_in'] = user.login
        session['roles'] = [role.name for role in user.roles]


def credentials_ok(user, password):
    if user:
        password_hash = generate_password_hash(password, user.salt)
        if password_hash == user.password_hash:
            return True
    return False


@app.route('/logout')
def logout():
    log_out_user()
    return redirect('/index')


def log_out_user():
    session.pop('logged_in', None)
    session.pop('roles', None)


@app.route('/article/<article_id>')
def article(article_id):
    article = db.get_article(article_id)
    return render_template('article.html', article=article)


@app.route('/addarticle', methods=['GET', 'POST'])
def add_article():
    if request.method == 'GET':
        return add_article_get()
    else:
        return add_article_post()


def add_article_get():
    return render_template('addcontent.html', title='Add Content')


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
