#!/usr/bin/python

import sys
from elasticsearch import Elasticsearch
import math

class TF_IDF():
    
    def __init__(self, url, es_host, es_port):
        self.url=url
        self.id=0
        self.size=0
        self.word_d={}
        self.word_list=[]
        self.freq_list=[]
        self.top10=[]
        self.es=Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
        self.lst=[]


    def OwnProcess(self):
        query ={"query":{"bool":{"must":{"match":{"url": self.url}}}},
            "_source":["url", "words", "frequencies"]}
        result=self.es.search(index="urls", body=query, size=1)
        self.size=result['hits']['total']['value']
        for res in result['hits']['hits']:
            self.id=res['_id']
            self.word_list.append(res['_source']['words'])
            self.freq_list.append(res['_source']['frequencies'])
        
        for idx in range(0, len((self.word_list)[0])):
            self.word_d[self.word_list[0][idx]]=self.freq_list[0][idx]
    

    def All_Process(self):
        
        top_dic={}
        self.OwnProcess()

        query={ "query":{"bool":{"must":[{"match_all":{}}],
            "must_not":[{"match": {"id": str(self.id)}}]}}, "size": str(self.size)}
        result=self.es.search(index="urls", body=query)

        for res in result["hits"]["hits"]:
            other_url=res['_source']['url']
            if(other_url==self.url):
                continue
            self.Other_process_doc(res['_source']['words'], res['_source']['frequencies'])
        
        idf_d=self.compute_idf()

        tf_d=self.compute_tf(self.word_list[0], self.freq_list[0])
        cnt=0
        for word,tfval in tf_d.items():
            cnt+=1
            top_dic[word]=tfval*idf_d[word] 
           
        return top_dic

    def GetTop10(self):

        dic=self.All_Process()

        dic=sorted(dic.items(), reverse=True, key=lambda item: item[1])

        self.top10=dic[0:10]
            
        return self.top10 
        

    def Other_process_doc(self, other_key, other_val):
        self.word_list.append(other_key)
        self.freq_list.append(other_val)
        for i in range(0, len(other_key)):
            if other_key[i] not in self.word_d.keys():
                self.word_d[other_key[i]]=other_val[i]
            else:
                self.word_d[other_key[i]]+=other_val[i]
    
    def compute_tf(self, other_key, other_val):
        bow=set()
        wordcount_d={}

        for i in range(0, len(other_key)):
            wordcount_d[other_key[i]]=other_val[i]
            bow.add(other_key[i])
        
        tf_d={}
     
        for word,cnt in wordcount_d.items():
            tf_d[word]=cnt/float(len(bow))
        return tf_d

    def compute_idf(self):
        Dval=len(self.word_list)
        bow=set()

        for i in range(0, Dval):
            for tok in self.word_list[i]:
                bow.add(tok)
        
        idf_d={}
       
        for t in bow:
            cnt=0
            for s in self.word_list:
                if t in s:
                    cnt+=1
            idf_d[t]=math.log(Dval/float(cnt))

        return idf_d        


if __name__ == "__main__":

    es_host="127.0.0.1"
    es_port="9200"
    
    url = "http://cassandra.apache.org/" # 찾고자 하는 url
    input_url="http://archiva.apache.org/"
    a="http://directory.apache.org/"
    b="http://madlib.apache.org/"
    c="http://openoffice.apache.org"

    instance = TF_IDF(c, es_host, es_port)
    top10=instance.GetTop10()

    for tup in top10:
        print("word: %10s\ttf-idf: %.10f" %(tup[0], tup[1]))

    #es.indices.delete(index='urls', ignore=[400,404])

    es=Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
    query={ "query":{"bool":{"must":[{"match_all":{}}]}}}
    result=es.search(index="urls", body=query)

    for res in result['hits']['hits']:
        print(res)
