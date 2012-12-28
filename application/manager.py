from application import app
from flask import render_template
from application.models import *


@app.route('/')
@app.route('/index')
def hello():
    return render_template('info/index.html', title='Change title')


@app.route('/hello/<username>')
def hello_username(username):
    return "Hello %s" % username
