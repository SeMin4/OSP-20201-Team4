from flask import Flask, render_template, url_for
from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
from MakeWordCloud import Word_Cloud

app = Flask(__name__)
es_host="127.0.0.1"
es_port="9200"


@app.route('/')
def make_cloud_image():

    url ="http://madlib.apache.org/"
    wd=Word_Cloud(url,es_host, es_port).make_cloud_image()
    fig=plt.figure(figsize=(10,10))
    plt.imshow(wd)
    plt.axis("off")
    
    fname="img.png"
    fig.savefig("static/"+fname)
    
    return render_template("WordCloud.html", fname=fname)
