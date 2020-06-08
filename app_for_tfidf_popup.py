from flask import Flask
from flask import render_template
from flask import redirect, url_for, abort
from flask import request
from tfidf import TF_IDF
app = Flask(__name__)
es_host="127.0.0.1"
es_port="9200"

@app.route('/')
def index():
    url = "http://cassandra.apache.org/"
    tf=TF_IDF(url, es_host, es_port)
    lst=[]
    top10=tf.GetTop10()
    for word in top10:
        lst.append(word[0])
    return render_template('tfidf_html.html', result=lst)
