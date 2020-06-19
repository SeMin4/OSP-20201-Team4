#!/usr/bin/python

import pandas as pd
from elasticsearch import Elasticsearch

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
        

if __name__=="__main__":
    es_host="127.0.0.1"
    es_port="9200"

    inst=ToCsv(es_host, es_port, "./static/csv/db.csv")
    df=inst.toCsv()
    print(df)




        
