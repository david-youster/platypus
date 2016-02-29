from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', title='Error', error=str(error))


if __name__ == '__main__':
    app.run(debug=True)