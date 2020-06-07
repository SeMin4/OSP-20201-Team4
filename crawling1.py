#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
from nltk import word_tokenize
from nltk.corpus import stopwords

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

	lines_list =[]
	for lines in my_lines:
		line = lines.text
		lines_list.append(line)

	for i in range(len(lines_list)):
		for mark in marks:
			lines_list[i] = lines_list[i].replace(mark,' ')
	
	return lines_list

def del_stopwords(lines_list):
	
	bef_str = str(lines_list[0])
	print("list 를 string으로 바꾼 문자열 ",bef_str)
	swlist = []	#stopwords list
	for sw in stopwords.words("english"):
		swlist.append(sw)
	tokenized = word_tokenize(bef_str)
	
	result = []	
	for w in tokenized:
		if w not in swlist:
			result.append(w)
	
	

	return result	#stop words 제거한 word lists

def process_timer():
	return time.time()
	

def add_word(wlist):

	

	"""for w in wlist:		# word list, freq list 분리
				
		if w not in words:
			words.append(w)
			frequencies.append(1)
		else:
			f_index = words.index(w)
			frequencies[f_index] = frequencies[f_index] + 1"""
	
	for w in wlist:		# word_d 딕셔너리에 단어, 빈도 수 추가
		if w not in word_d.keys():
			word_d[w] = 0
		word_d[w] +=1


def compute_tf(s):
	bow = set()
	wordcount_d = {}
	
	tokenized = word_tokenize(s)
	for tok in tokenized:
		if tok not in wordcount_d.keys():
			wordcount_d[tok]=0
		wordcount_d[tok]+=1
		bow.add(tok)
	tf_d = {}
	for word,count in wordcount_d.items():
		tf_d[word] = count/float(len(bow))
	
	return tf_d

def compute_idf():
	Dval = len(sent_list)
	
	bow = set()
	
	for i in range(0,len(sent_list)):
		tokenized = word_tokenize(sent_list[i])
		for tok in tokenized:
			bow.add(tok)
	idf_d={}
	for t in bow:
		cnt=0
		for s in sent_list:
			if t in word_tokenize(s):
				cnt += 1
		idf_d[t] = math.log(Dval/float(cnt))	#pdf랑다름


	return idf_d
	
#def compute_tfidf():
			
		
if __name__ == '__main__':

	idvalue=0
	f1 = open('test_input.txt','r')
	f2 = open('test_output.txt','a')
	#여기서부터 밑의 주석까지 반복문처리 
	for url in f1:
		idvalue = idvalue+1
		start = process_timer()		
		#urladdress = 'u'+'\''+url.strip()+'\''		
		urladdress = url.strip()
		ress = requests.get(urladdress)	#에러가 발생하지 않으면 f2에 url쓰기
		f2.write(url)
		html = BeautifulSoup(ress.content, "html.parser")
		content = html.select('body')
		list1 = del_symbols(content)
		list1 = del_stopwords(list1)
		#print( "stopwords를 제거한 단어 list",list1)	
		add_word(list1)	
		end = process_timer()
		ptime = end - start #처리시간 check
		words = list(word_d.keys())			#dict.keys() -> words list
		frequencies = list(word_d.values())		#dict.values() -> frequency list
		

		dic = dict(url=url.strip(), words = words, frequencies = frequencies, wordcnt = 		len(words),processing_time = ptime)
		e = json.dumps(dic)
		es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
		res = es.index(index='urls', doc_type='url',id=idvalue, body=e)
		print(res)
		
		words.clear()
		frequencies.clear()
		word_d.clear()

		###
	
	f1.close()
	f2.close()
	

	
	
