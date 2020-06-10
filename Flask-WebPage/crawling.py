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


words = []
frequencies = []
word_d = {}


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


		
def word_processsing(url_list):
	idvalue = 1	
	result = []
	for url in url_list:
		start = process_timer()		
		#urladdress = 'u'+'\''+url.strip()+'\''		
		urladdress = url.strip()
		ress = requests.get(urladdress)	#에러가 발생하지 않으면 f2에 url쓰기
		
		"""
		if urladdress not in url_cur_list:			
			if urladdress not in urllist:		
				f2.write(url)
				url_cur_list.append(urladdress)
			else:
				print("중복된 url")
				continue
				
		else:
			print("중복된 url")
			continue
		"""
			

		html = BeautifulSoup(ress.content, "html.parser")
		#content = html.select('body')
		content = html.findAll(text = True)
		#print(content)
		#print("-------------------------------------------")
		list1 = del_symbols(content)
		#print(list1)
		list1 = del_stopwords(list1)
			
		#print( "stopwords를 제거한 단어 list",list1)	
		add_word(list1)	
		end = process_timer()
		ptime = end - start #처리시간 check
		words = list(word_d.keys())			#dict.keys() -> words list
		frequencies = list(word_d.values())		#dict.values() -> frequency list
		

		dic = dict(url=urladdress, words = words, frequencies = frequencies, wordcnt = 		len(words),processing_time = ptime)
		dic2 = dict(url=urladdress, wordcnt = len(words),processing_time = round(ptime,5))
		result.append(dic2)
		e = json.dumps(dic)
		es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
		res = es.index(index='urls', doc_type='url',id=idvalue, body=e)
		print(res)
		
		words.clear()
		frequencies.clear()
		word_d.clear()
		idvalue = idvalue + 1
	return result
	
		
#if __name__ == '__main__':
def main(url_list):

	result = word_processsing(url_list)
	return result

		
	


	
	



	
	
