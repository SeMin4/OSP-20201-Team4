from flask import Flask
from flask import render_template
from flask import redirect, url_for, abort
from flask import request
from flask_dropzone import Dropzone



app = Flask(__name__)
dropzone = Dropzone(app=app)

app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'text'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/file', methods=['GET', 'POST'])
def getFibonacci():
    error = None
    if request.method == 'POST':
        return