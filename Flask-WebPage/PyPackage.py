#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
from elasticsearch import Elasticsearch
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
from nltk import word_tokenize
from nltk.corpus import stopwords
import json
import time
import pandas as pd
import math
from werkzeug.utils import secure_filename

'''
crawling : main(url_list ,id, es_host, es_port)
tfidf : TF_IDF
Cosine Similarity : Url_Similarity
wordcloud : Word_Cloud
tocsv : ToCsv
'''
words = []
frequencies = []
word_d = {}

input_urls = []
input_urls_value = []

def del_symbols(my_lines):
    	marks = [',', '!',':','.','#','$','%','^','&','*','(',')','+','-','/','[',']','{','}','\\','\'',';','<','>','0','1','2','3','4','5','6','7','8','9','\n','"','’','_','~','?','|','@','©']
	h = 0
	lines_list =[]
	for text in my_lines:
		#line = lines.text
		lines_list.append(text)
		h = h+1

	for i in range(len(lines_list)):
		for mark in marks:
			lines_list[i] = lines_list[i].replace(mark,' ')
	
	return lines_list

def efilter(s):
	lines_list =[]
	for i in s:
		text = re.sub('[^a-zA-Z ]','',i).strip()
		lines_list.append(text+' ')
		

	return lines_list


def del_stopwords(lines_list):
	
	string=""
	for i in range(len(lines_list)):
		string = string + str(lines_list[i])
	

	#print("list 를 string으로 바꾼 문자열 ",string)
	swlist = []	#stopwords list
	for sw in stopwords.words("english"):
		swlist.append(sw)
	
	
	tokenized = word_tokenize(string)
	
	result = []	
	for w in tokenized:
		if w not in swlist:
			result.append(w)
	
	

	return result	#stop words 제거한 word lists

def process_timer():
	return time.time()
	

def add_word(wlist):
	
	for w in wlist:		# word_d 딕셔너리에 단어, 빈도 수 추가
		if w not in word_d.keys():
			word_d[w] = 0
		word_d[w] +=1


		
def word_processsing(url_list, id):
	idvalue = int(id) 
	result = []
	for url in url_list:
		start = process_timer()		
		#urladdress = 'u'+'\''+url.strip()+'\''		
		urladdress = url.strip()		
		
		if urladdress in input_urls:			
			input_urls.append(urladdress)			
			input_urls_value.append(3)			
			print("중복된 url")	#중복
			continue
		input_urls.append(urladdress)
			
		ress = requests.get(urladdress)	
		rval = ress.status_code
		if rval <200 | rval >= 300:
			input_urls_value.append(2)
			print("url 크롤링실패")	#실패
			continue

		
		html = BeautifulSoup(ress.content, "html.parser")
		#content = html.select('body')
		content = html.findAll(text = True)
		#print(content)
		#print("-------------------------------------------")
		list1 = del_symbols(content)
		list1 = efilter(list1)
		list1 = del_stopwords(list1)

		
		#print( "stopwords를 제거한 단어 list",list1)	
		add_word(list1)	
		end = process_timer()
		ptime = end - start #처리시간 check
		input_urls_value.append(1) 	#성공
	
		words = list(word_d.keys())			#dict.keys() -> words list
		frequencies = list(word_d.values())		#dict.values() -> frequency list
		#print(len(word_d))	

		dic = dict(url=urladdress, words = words, frequencies = frequencies, wordcnt = len(words),processing_time = ptime)
		dic2 = dict(id= id, url=urladdress, wordcnt = len(words),processing_time = round(ptime,5))
		# result.append(dic2)
		e = json.dumps(dic)
		res = es.index(index='urls', doc_type='url',id=idvalue, body=e)
		#print(res)
	
		
		words.clear()
		frequencies.clear()
		word_d.clear()

	return dic2
	
		
#if __name__ == '__main__':
def main(url_list ,id, es_host, es_port) :
    es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
	input_urls.clear()
	input_urls_value.clear()
	result = word_processsing(url_list, id)
	return result

######### TF-IDF ########
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

        for word,tfval in tf_d.items():
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

######### Cosine Similarity ########
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


######### WordCloud ########
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

    
######## 엑셀 파일 저장 ########
class ToCsv():
    
    def __init__(self, es_host, es_port, filename):
        self.es=Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
        self.url_list=[]
        self.word_list=[]
        self.freq_list=[]
        self.wordcnt_list=[]
        self.time_list=[]
        self.fname=filename
    
    def toDataFrame(self):
        query={"query":{"match_all":{}}}
        result=self.es.search(index="urls", body=query)
        cnt=result['hits']['total']['value']
        query={"query":{"match_all":{}}, "size":str(cnt)}
        result=self.es.search(index="urls", body=query)

        for res in result["hits"]["hits"]:
            self.url_list.append(res['_source']['url'])
            word=res['_source']['words']
            freq=res['_source']['frequencies']

            word, freq = self.SortDic(word, freq)

            self.word_list.append(str(str(word).strip('[]')))
            self.freq_list.append(str(str(freq).strip('[]')))
            self.wordcnt_list.append(res['_source']['wordcnt'])
            self.time_list.append(res['_source']['processing_time'])

        df=pd.DataFrame({"Url":self.url_list, "Words":self.word_list, "Frequency":self.freq_list, "WordCount":self.wordcnt_list, "Processing Time": self.time_list})

        return df 

    def toCsv(self):
        df=self.toDataFrame()
        df.to_csv(self.fname)
        return df

    def SortDic(self, key_list, val_list):
        wd_d={}
        for i in range(0, len(key_list)):
            wd_d[key_list[i]]=val_list[i]
        wd_d=sorted(wd_d.items(), reverse=True, key=lambda item: item[1])
        
        key_list=[]
        val_list=[]
        dic={}

        for tup in wd_d:
            dic[tup[0]]=tup[1]
        
        return list(dic.keys()), list(dic.values())