from flask import Flask
from flask import render_template
from flask import redirect, url_for, abort
from flask import request
from cosinesimilarity import Url_Similarity
app = Flask(__name__)
es_host="127.0.0.1"
es_port="9200"

@app.route('/')
def index():
    url = "http://cassandra.apache.org/"
    cs=Url_Similarity(url, es_host, es_port)
    url_lst=[]
    sm_lst=[]
    top3=cs.GetTop3()
    for url in top3:
        url_lst.append(url[0])
        sm_lst.append(url[1])
    return render_template('cs_html.html', url=url_lst, cs=sm_lst)
