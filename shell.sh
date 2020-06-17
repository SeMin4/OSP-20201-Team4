#!/bin/bash

#cp -r Flask-WebPage ~/
#cp -r elasticsearch.yml ~/
cp -r etcRequirement.py ~/
cd ~
#mkdir osp-team4
#cp -r Flask-WebPage elasticsearch.yml osp-team4/
cp -r etcRequirement.py osp-team4/
cd osp-team4

#wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-linux-x86_64.tar.gz
#tar xvzf elasticsearch-7.6.2-linux-x86_64.tar.gz

#cp elasticsearch.yml elasticsearch-7.6.2/config/ # we have to modify cp command

./elasticsearch-7.6.2/bin/elasticsearch -d

python etcRequirement.py

cd Flask-WebPage


echo "flask directory archiecture done"


echo "Installing flask..."
#pip install flask


echo "Installing Werkzeug..."
#pip install -U Werkzeug

echo "Installing beautifulsoup4..."
#pip install beautifulsoup4

echo "Installing nltk..."
#pip install nltk

echo "Installing wordcloud"
#pip install wordcloud

echo "Installing matplotlib"
#pip install matplotlib

echo "Installing elasticsearch"
#pip install elasticsearch

echo "Installing requests"
#pip install requests

echo "Installing pandas"
#pip install pandas


flask run
