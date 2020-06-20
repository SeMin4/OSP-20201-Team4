#!/usr/bin/python

import sys
from elasticsearch import Elasticsearch
import numpy as np

class Url_Similarity():
    
    def __init__(self, url, es_host, es_port):
        self.url=url
        self.id=0
        self.size=0
        self.word_list=[]
        self.word_d={}
        self.other_d={}
        self.es=Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
    
    def SetUrl(self, url):
        self.url=url

    def Process_Own_Sentence(self):
        query ={"query":{"bool":{"must":{"match":{"url": self.url}}}},
            "_source":["url", "words", "frequencies"]}
        result=self.es.search(index="urls", body=query, size=1)

        self.size=result['hits']['total']['value']
    
        for res in result['hits']['hits']:
            self.id=res['_id']
            self.word_list=res['_source']['words']
            freq=res['_source']['frequencies']
           
        for idx in range(0, len(self.word_list)):
            self.word_d[self.word_list[idx]]=freq[idx]
    
    def AllProcess(self):
        cos_dic={}
        self.Process_Own_Sentence()
        query={ "query":{"bool":{"must":[{"match_all":{}}],
            "must_not":[{"match": {"id": str(self.id)}}]}}, "size": str(self.size)}
        result=self.es.search(index="urls", body=query)
    
        for res in result["hits"]["hits"]:
            other_url=res['_source']['url']
            if(other_url==self.url):
                continue
            other_word=res['_source']['words']
            other_freq=res['_source']['frequencies']
            
            self.Process_Other_Sentence(other_word, other_freq)
            cos=self.CosineSimilarity(other_word)
            cos_dic[other_url]=cos
        return cos_dic
    
    def GetTop3(self):
        cos_dic=self.AllProcess()
        cos_list=sorted(cos_dic.items(), reverse=True, key=lambda item: item[1])        
        return cos_list[0:3]
        
    def Process_Other_Sentence(self, other_word, other_freq):
        self.other_d=self.word_d.copy()
        
        for idx in range(0, len(other_word)):
            self.other_d[other_word[idx]]=other_freq[idx]
    
    def CosineSimilarity(self, other_word):
        v1=self.Make_Vector(self.word_list)
        v2=self.Make_Vector(other_word)

        dotpro=np.dot(v1,v2)
        cossimil=dotpro/(np.linalg.norm(v1)*np.linalg.norm(v2))

        return cossimil

    def Make_Vector(self, other_word):
        v=[]
        for w in self.other_d.keys():
            val=0
            for t in other_word:
                if w==t:
                    val+=1
            v.append(val)
        return v

if __name__ =="__main__":

        es_host="127.0.0.1"
        es_port="9200"
        url = "http://cassandra.apache.org/"
        URL = Url_Similarity(url, es_host, es_port)
        for tup in URL.GetTop3():
             print("url: %-30s\tCosineSimilarity: %.10f" %(tup[0], tup[1]))

