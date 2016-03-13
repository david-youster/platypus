from flask import Flask, render_template, request, redirect, session
from functools import wraps
from util import generate_salt, generate_password_hash
import db

app = Flask(__name__)
app.secret_key = '9l2+y#cit1)yvm4douh_uv=wh1cm0w3nevpv7v(8$e*qan8n3+'


def check_admin(function):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        if user_has_role('admin'):
            return function(*args, **kwargs)
        return redirect('/index')
    return wrapped_function


def check_author(function):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        if user_has_role('author'):
            return function(*args, **kwargs)
        return redirect('/index')
    return wrapped_function


def check_anon(function):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        if 'logged_in' in session:
            return redirect('/index')
        return function(*args, **kwargs)
    return wrapped_function


def user_logged_in():
    return 'logged_in' in session.keys()


def user_has_role(role_name):
    roles = session.get('roles', [])
    return role_name in roles


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title='Home',
        articles=db.get_articles())


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/admin')
@check_admin
def admin():
    return render_template('admin.html', title='Admin', roles=db.get_roles())


@app.route('/admin/createuser', methods=['POST'])
@check_admin
def admin_create_user():
    create_user(
        request.form['login'],
        request.form['password'],
        request.form.getlist('roles'))
    return redirect('/admin')


def create_user(login, password, roles):
    salt = generate_salt()
    password_hash = generate_password_hash(password, salt)
    roles = [db.get_role(role) for role in roles]
    db.create_user(login, password_hash, salt, roles)


@app.route('/article/<article_id>')
def article(article_id):
    article = db.get_article(article_id)
    return render_template('article.html', article=article)


@app.route('/author')
@check_author
def add_article():
    return render_template('author.html', title='Author')


@app.route('/author/createarticle', methods=['POST'])
@check_author
def author_create_article():
    db.create_article(
        request.form['title'],
        request.form['snippet'],
        request.form['text'])
    article_id = db.get_article_latest().id_
    return redirect('/article/{}'.format(article_id))


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', title='Error', error=str(error))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    db.init()
    app.jinja_env.globals.update(
        user_has_role=user_has_role,
        user_logged_in=user_logged_in)
    app.run(debug=True)
