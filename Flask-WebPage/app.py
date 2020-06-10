from flask import Flask
from flask import render_template
from flask import redirect, url_for, abort
from flask import request
from flask import Response
from flask import jsonify
from werkzeug.utils import secure_filename
import crawling
import json

from tfidf import TF_IDF
from cosinesimilarity import Url_Similarity



app = Flask(__name__)

app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'text'

@app.route('/')
def index():
	return render_template('index.html', len= 0, results = "")

@app.route('/upload/File', methods=['GET', 'POST'])
def uploadFile():
	error = None
	if request.method == 'POST':
		url_list = []		
		f = request.files['file']
		f.save(secure_filename(f.filename))
		f1 = open(f.filename,'r')
		url_list = f1.readlines()
		f1.close()
		"""
		url = request.form['url']	
		url_list.append(url)		
		"""
		result = crawling.main(url_list)
		return render_template('index.html', len = len(result), results = result)


@app.route('/analysis/tfidf', methods=['GET'])
def tfidfAnalysis() :
	error = None
	es_host="127.0.0.1"
	es_port="9200"
	if request.method == 'GET':
		url = request.args.get('url')
		# print("url : " + url)
		tf=TF_IDF(url, es_host, es_port)
		lstWord=[]
		lstPercent = []
		top10=tf.GetTop10()
		for word in top10:
			lstWord.append(word[0])
			lstPercent.append(word[1])

		return jsonify(
			word=json.dumps(lstWord),
			percent=json.dumps(lstPercent)
		)


@app.route('/analysis/cosineSimilarity', methods=['GET'])
def cosineSimilariyAnaylsis() :
	error = None
	es_host="127.0.0.1"
	es_port="9200"
	if request.method == 'GET':
		url = request.args.get('url')
		cs=Url_Similarity(url, es_host, es_port)
		url_lst=[]
		sm_lst=[]
		top3=cs.GetTop3()
		for url in top3:
			url_lst.append(url[0])
			sm_lst.append(url[1])
		return jsonify(
			word=json.dumps(url_lst),
			percent=json.dumps(sm_lst)
		)