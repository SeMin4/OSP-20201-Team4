from flask import Flask
from flask import render_template
from flask import redirect, url_for, abort
from flask import request
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
import crawling



app = Flask(__name__)
dropzone = Dropzone(app=app)

app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'text'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload/File', methods=['GET', 'POST'])
def getFibonacci():
	error = None
	if request.method == 'POST':
		url_list = []		

		f = request.files['file']
		if f.filename != "":
			print("file OKOKOKO")
			#f.save(secure_filename(f.filename))
			f1 = open(f.filename,'r')
			url_list = f1.readlines()
			f1.close()
		
		else:
			print("file nononono")
			url = request.form['url']
			print("URL : " , url)	
			url_list.append(url)		
		

		crawling.main(url_list)
		return
