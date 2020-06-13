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
        self.top10=[]
        self.es=Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
        self.sums=0
        self.lst=[]


    def OwnProcess(self):
        query ={"query":{"bool":{"must":{"match":{"url": self.url}}}},
            "_source":["url", "words", "frequencies"]}
        result=self.es.search(index="urls", body=query, size=1)
        self.size=result['hits']['total']['value']
        for res in result['hits']['hits']:
            self.id=res['_id']
            self.word_list.append(res['_source']['words'])
            val=res['_source']['frequencies']
        
        for idx in range(0, len((self.word_list)[0])):
            self.word_d[self.word_list[0][idx]]=val[idx]
    
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

        tf_d=self.compute_tf(self.word_list[0])

        for word,tfval in tf_d.items():
            top_dic[word]=tfval*idf_d[word]
            self.sums=self.sums+top_dic[word]
        
        #print(self.sums)

    
        #디비 내 문서 전체 tf-idf 확인할 때 이거 쓰기
        '''
        for i in range(0, len(self.word_list)):
            tf_d=self.compute_tf(self.word_list[i])
            self.sums=0
            for word,tfval in tf_d.items():
                top_dic[word]=tfval*idf_d[word]
                print(word, tfval*idf_d[word])
                self.sums=self.sums+top_dic[word]
            print("-------------------------------------")
            print(self.sums)
            self.lst.append(self.sums)
            print("-------------------------------------")
        
        for i in self.lst:
            print(i, end=" ")
        '''
        
        return top_dic

    def GetTop10(self):

        dic=self.All_Process()

        dic=sorted(dic.items(), reverse=True, key=lambda item: item[1])

        self.top10=dic[0:10]
            
        return self.top10 
        

    def Other_process_doc(self, other_key, other_val):
        self.word_list.append(other_key)
        for word in other_key:
            if word not in self.word_d.keys():
                self.word_d[word]=0
            self.word_d[word]+=1
    
    def compute_tf(self, other_key):
        bow=set()
        wordcount_d={}

        for tok in other_key:
            if tok not in wordcount_d.keys():
                wordcount_d[tok]=0
            wordcount_d[tok]+=1
            bow.add(tok,)
        
        tf_d={}
        for word,cnt in wordcount_d.items():
            tf_d[word]=cnt/float(len(bow))
        return tf_d
    def compute_idf(self):
        Dval=len(self.word_list)
        bow=set()

        for i in range(0, Dval):
            for tok in self.word_list[i]:
                bow.add(tok,)
        
        
        idf_d={}
       
        for t in bow:
            cnt=0
            for s in self.word_list:
                if t in s:
                    cnt+=1
            idf_d[t]=float(math.log(Dval/cnt))

        return idf_d        


if __name__ == "__main__":

    es_host="127.0.0.1"
    es_port="9200"
    
    url = "http://cassandra.apache.org/" # 찾고자 하는 url

    instance = TF_IDF(url, es_host, es_port)
    top10=instance.GetTop10()

    for tup in top10:
        print("word: %10s\ttf-idf: %.10f" %(tup[0], tup[1]))

    #es.indices.delete(index='urls', ignore=[400,404])
