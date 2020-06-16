from flask import Flask
from flask import render_template
from flask import redirect, url_for, abort
from flask import request
from flask import Response
from flask import jsonify
from werkzeug.utils import secure_filename
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from MakeWordCloud import Word_Cloud

import crawling
import json

from tfidf import TF_IDF
from cosinesimilarity import Url_Similarity
from dbtocsv import ToCsv


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload/File', methods=['GET', 'POST'])
def uploadFile():
	error = None
	if request.method == 'GET':
		url = request.args.get('url')
		id = request.args.get('id')
		url_list = []		
		url_list.append(url)
		"""
		url = request.form['url']	
		url_list.append(url)		
		"""
		result = crawling.main(url_list,id)
		
		return json.dumps(result)
		
	elif request.method == 'POST':
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
    if request.method == 'GET' :
        url = request.args.get('url')
        # print("url : " + url)
        tf=TF_IDF(url, es_host, es_port)
        lstWord=[]
        lstPercent = []
        top10=tf.GetTop10()
        for word in top10:
            lstWord.append(word[0])
            lstPercent.append(word[1])
        returnResult = {
            "word":lstWord,
            "percent":lstPercent
        }
        return json.dumps(returnResult)


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
        returnResult = {
            "url":url_lst,
            "percent":sm_lst
        }
        return json.dumps(returnResult)



@app.route('/make/wordcloud', methods=['GET'])
def make_cloud_image():
    error = None
    es_host="127.0.0.1"
    es_port="9200"
    if request.method == 'GET' :
        url = request.args.get('url')
        wd=Word_Cloud(url,es_host, es_port).make_cloud_image()
        fig=plt.figure(figsize=(10,10))
        plt.imshow(wd)
        plt.axis("off")
        fname= url.split("//")[1].split(".")[0] + ".png"
        fig.savefig("static/image/"+fname)
        plt.close()
        returnResult = {
            "fname":fname
        }
        return json.dumps(returnResult)


@app.route('/down/csv')
def down_csv():
    es_host="127.0.0.1"
    es_port="9200"

    inst=ToCsv(es_host, es_port, "./static/csv/db.csv")
    df=inst.toCsv()
    returnResult = {
        "fname":"../static/csv/db.csv"
    }
    return json.dumps(returnResult)