from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is my homepage'

@app.route('/tuna')
def tuna():
    return 'Tuna is good'


@app.route('/profile/<username>')
def profile():
    return '<h2>Hi %s<h2>'%username

if __name__ == "__main__":
    app.run('0.0.0.0',5000)