#!/usr/bin/python
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from elasticsearch import Elasticsearch

class Word_Cloud():
    def __init__(self, url, es_host, es_port):
        self.url=url
        self.es=Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
        self.word_d={}
    def get_tag(self):
        query ={"query":{"bool":{"must":{"match":{"url": self.url}}}},"_source":["url", "words", "frequencies"]}
        result=self.es.search(index="urls", body=query, size=1)
        for res in result['hits']['hits']:
            word_list=res['_source']['words']
            word_freq=res['_source']['frequencies']

        for idx in range(0, len(word_list)):
            self.word_d[word_list[idx]]=word_freq[idx]
        return self.word_d

    def make_cloud_image(self):
        word_cloud=WordCloud(
        width=400,
        height=400,
        background_color="white")

        self.get_tag()
        word_cloud=word_cloud.generate_from_frequencies(self.word_d)
        return word_cloud
    
if __name__ =="__main__":
    es_host="127.0.0.1"
    es_port="9200"
    url ="http://directory.apache.org/"

    wc=Word_Cloud(url, es_host, es_port)
    wd=wc.make_cloud_image()
    fig=plt.figure(figsize=(10,10))
    plt.imshow(wd)
    plt.axis("off")
    fname="img.png"
    fig.savefig("static/image/"+fname)
    plt.close()
    

    


