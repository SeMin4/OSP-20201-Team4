#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
from nltk import word_tokenize
from nltk.corpus import stopwords
from werkzeug.utils import secure_filename
import sys
from elasticsearch import Elasticsearch
import json
import time



class Crawling() :
	def __init__(self, input_url,id,es_host,es_port):
		self.__input_url = input_url
		self.__id = id
		self.es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
		self.__words = []
		self.__frequencies = []
		self.__word_d = {}

	def process_timer(self):
		return time.time()	

	def del_symbols(self, my_lines):
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
	def efilter(self, s):
		lines_list =[]
		for i in s:
			text = re.sub('[^a-zA-Z ]','',i).strip()
			lines_list.append(text+' ')
		

		return lines_list
	def del_stopwords(self,lines_list):
		string=""
		for i in range(len(lines_list)):
			string = string + str(lines_list[i])
	
		swlist = []	#stopwords list
		for sw in stopwords.words("english"):
			swlist.append(sw)
			w = sw.capitalize()
			swlist.append(w)
			w = sw.upper()
			swlist.append(w)
	
	
		tokenized = word_tokenize(string)
	
		result = []	
		for w in tokenized:
			if w not in swlist:
				result.append(w)
	
		return result	#stop words 제거한 word lists
		
	def add_word(self, wlist,word_d):
	
		for w in wlist:		# word_d 딕셔너리에 단어, 빈도 수 추가
			if w not in word_d.keys():
				word_d[w] = 0
			word_d[w] +=1

    
	def word_processing(self):

		start = self.process_timer()		
		#urladdress = 'u'+'\''+url.strip()+'\''		
		urladdress = self.__input_url.strip()		
		ress = requests.get(urladdress)	
		html = BeautifulSoup(ress.content, "html.parser")
	
		content = html.findAll(text = True)

		list1 = self.del_symbols(content)
		list1 = self.efilter(list1)
		list1 = self.del_stopwords(list1)

		self.add_word(list1,self.__word_d)	
		end = self.process_timer()
		ptime = end - start #처리시간 check
	
		self.__words = list(self.__word_d.keys())			#dict.keys() -> words list
		self.__frequencies = list(self.__word_d.values())		#dict.values() -> frequency list
		print(len(self.__word_d))	

		dic = dict(url=urladdress, words = self.__words, frequencies = self.__frequencies, wordcnt = len(self.__words),processing_time = ptime)
		dic2 = dict(id= self.__id, url=urladdress, wordcnt = len(self.__words),processing_time = round(ptime,5))
	
		e = json.dumps(dic)
		res = self.es.index(index='urls', doc_type='url',id=self.__id, body=e)
	
		#words.clear()
		#frequencies.clear()
		#word_d.clear()
		print(res)
		return dic2
    

    




if __name__ == "__main__":
	
	es_host="127.0.0.1"
	es_port="9200"

	
	input_url="http://archiva.apache.org/"
	id = 1 
	crawling_url = Crawling(input_url,id, es_host, es_port)
	dic = crawling_url.word_processing()
	print(dic)
    