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

es_host="127.0.0.1"
es_port="9200"
es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)

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
		print(len(word_d))	

		dic = dict(url=urladdress, words = words, frequencies = frequencies, wordcnt = 		len(words),processing_time = ptime)
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
def main(url_list ,id) :
	input_urls.clear()
	input_urls_value.clear()
	result = word_processsing(url_list, id)
	return result

		
	


	
	



	
	
