from flask import Flask
from flask import render_template, request, redirect, session, url_for
from flask.ext.assets import Bundle, Environment
from functools import wraps
from markdown import markdown
from bleach import clean
from util import generate_salt, generate_password_hash, get_theme_file
import db

app = Flask(__name__)


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


def user_login():
    return session.get('logged_in', None)


def user_logged_in():
    return 'logged_in' in session.keys()


def user_has_role(role_name):
    return role_name in session.get('roles', [])


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template(
        get_theme_file('index.html'),
        title='Home',
        articles=db.get_articles())


@app.route('/login', methods=['GET', 'POST'])
@check_anon
def login():
    if request.method == 'GET':
        return login_get()
    return login_post()


def login_get():
    return render_template(get_theme_file('login.html'), title='Login')


def login_post():
    log_in_user(request.form['login-name'], request.form['login-password'])
    return redirect(url_for('index'))


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
    return redirect(url_for('index'))


def log_out_user():
    session.pop('logged_in', None)
    session.pop('roles', None)


@app.route('/admin')
@check_admin
def admin():
    return render_template(
        get_theme_file('admin.html'),
        title='Admin',
        roles=db.get_roles(),
        users=db.get_users())


@app.route('/admin/createuser', methods=['POST'])
@check_admin
def admin_create_user():
    create_user(
        request.form['login'],
        request.form['password'],
        request.form.getlist('roles'))
    return redirect(url_for('admin'))


def create_user(login, password, roles):
    salt = generate_salt()
    password_hash = generate_password_hash(password, salt)
    roles = [db.get_role(role) for role in roles]
    db.create_user(login, password_hash, salt, roles)


@app.route('/admin/deleteuser/<user_login>')
@check_admin
def admin_delete_user(user_login):
    db.delete_user(user_login)
    return redirect(url_for('admin'))


@app.route('/admin/displayuser/<user_login>')
@check_admin
def admin_display_user(user_login):
    return 'Not implemented'


@app.route('/author')
@check_author
def author():
    return render_template(
        get_theme_file('author.html'),
        title='Author',
        articles=db.get_articles_by_author(session.get('logged_in')))


@app.route('/article/display/<article_id>')
def article_display(article_id):
    article = db.get_article(article_id)
    article.text = markdown(article.text)
    return render_template(get_theme_file('article.html'), article=article)


@app.route('/article/delete/<article_id>')
def article_delete(article_id):
    db.delete_article(article_id)
    return redirect(url_for('author'))


@app.route('/article/edit/<article_id>', methods=['GET', 'POST'])
def article_edit(article_id):
    if request.method == 'GET':
        return article_edit_get(article_id)
    return article_edit_post(article_id)


def article_edit_get(article_id):
    article = db.get_article(article_id)
    if (article and not user_has_role('editor') and
            article.author.login != session.get('logged_in', None)):
        return redirect(url_for('index'))
    return render_template(
        get_theme_file('editarticle.html'),
        article=article,
        title='Edit Article')


def article_edit_post(article_id):
    db.update_article(
        article_id,
        request.form['title'],
        request.form['snippet'],
        clean(request.form['text']))
    return redirect(url_for('article_display', article_id=article_id))


@app.route('/author/createarticle', methods=['POST'])
@check_author
def author_create_article():
    db.create_article(
        request.form['title'],
        request.form['snippet'],
        clean(request.form['text']),
        db.get_user(session.get('logged_in')))
    article_id = db.get_article_latest().id_
    return redirect(url_for('article_display', article_id=article_id))


@app.errorhandler(404)
def not_found(error):
    return render_template(
        get_theme_file('error.html'),
        title='Error',
        error=str(error))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


def init():
    init_app()
    init_assets()
    db.init()


def init_app():
    app.config['theme'] = 'basic'
    app.secret_key = '9l2+y#cit1)yvm4douh_uv=wh1cm0w3nevpv7v(8$e*qan8n3+'
    app.jinja_env.globals.update(
        user_login=user_login,
        user_has_role=user_has_role,
        user_logged_in=user_logged_in,
        get_theme_file=get_theme_file)


def init_assets():
    assets = Environment(app)
    assets.url = app.static_url_path
    with app.app_context():
        scss = Bundle(
            get_theme_file('sass/web.scss'),
            filters='pyscss',
            output=get_theme_file('styles/web.css'))
        assets.register('scss_web', scss)


if __name__ == '__main__':
    init()
    app.run(debug=True, host='0.0.0.0')
