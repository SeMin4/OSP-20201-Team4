from flask import Flask
from flask import render_template
from flask import redirect, url_for, abort
from flask import request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
