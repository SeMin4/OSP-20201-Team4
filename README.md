# Opensource Programming Team Project
## Team4 - Web Data Similarity Analysis

### What we do?
현재 웹상에 있는 데이터들을 HTTP REQUEST METHOD(GET, POST..) 등을 통해서 웹상의 데이터들을 모으고 이것을 자연어 처리 라이브러리를 통해서 데이터를 분석합니다. 웹페이지의 메인 페이지의 화면은 아래와 같습니다.

![mainpage](https://user-images.githubusercontent.com/45915619/85197796-6306c400-b31e-11ea-8cf1-36bbb2ac8d92.png)


### Why?
현재 웹상에서 데이터들이 무수히 많습니다. 이것을 자연어 처리와 크롤링을 활용하여 웹상의 데이터 들을 분석하고 한눈에 알아 보기 쉽게 만들도록 합니다. 현재 수업시간에 배우는 flask, BeautifulSoup, Elastic Search의 활용에 익숙해 지기 위함이며 이것을 통해 다른 프로젝트 진행시 이것을 잘 활용할 수 있도록 팀프로젝트 실습을 통해 배우도록 합니다.

### How?
-- Web
- Flask 를 활용하여 웹페이지를 구성하고 사용자가 좀 더 결과물을 한눈에 파악하기 쉽도록 결과물을 구성하도록 합니다.

-- Crawling
- Reuqests 를 활용하여 크롤링을 진행하고 BeautifulSoup4 를 이용하여 html을 parsing후 데이터 분석을 진행하여야 하는 정보를 모을수 있도록 합니다.

-- Database
- ElasticSearch 의 NonSQL 기반의 데이터베이스를 활용하여 데이터 베이스를 구축하고 이것을 통해 HTTP REQUEST를 활용하여 저장한 데이터들을 받아오도록 합니다. 이것을 활용하여 여러 웹사이트에 대한 정보를 한사이트에서 한꺼번에 정리후 보여주도록 합니다.


### So?
수업시간에 배운 여러가지 파이썬 패키지등의 활용법을 정확히 숙지하고 다른 프로젝트 진행시 이것을 응용하여 활용할 수 있도록 합니다. 다른 수업시간에 배우지 않는 NonSQL기반의 데이터 베이스의 활용법, flask, BeuatifulSoup 을 정확히 숙지해 다른 프로젝트 진행시 활용할 수 있도록 합니다. 

### Web Page Analysis Procedure
웹 페이지 분석 프로젝트를 실행시키기 위한 쉘 파일이 있습니다.

![파일이동](https://user-images.githubusercontent.com/45915619/85198731-ff809480-b325-11ea-9928-ea32b2828b47.png)

Flask-WebPage 디렉토리 등 필요한 파일들을 osp_team4 디렉토리로 이동시킵니다.
그리고 웹상의 데이터들을 분석하기 위한 라이브러리들을 다운받고 프로젝트 환경을 구축합니다.

![라이브러리다운](https://user-images.githubusercontent.com/45915619/85198733-014a5800-b326-11ea-9945-994fe5465317.png)

이로써 웹 페이지 분석 프로젝트를 실행하기 위한 환경을 다 구축하였고, app.py 파일이 있는 Flask-WebPage 디렉토리로 이동하여 flask를 실행시킵니다.

![플라스크런](https://user-images.githubusercontent.com/45915619/85198734-027b8500-b326-11ea-90aa-d0579824f7a9.png)

### 크롤링 상태표
URL 입력창에서는  single url 과 files 중에 무엇을 입력할지 선택한 후 URL을 입력받고 'Enter' 버튼을 누르면 크롤링 상태표가 나타납니다. 크롤링 상태표에서는 입력받은 URL들의 주소와 크롤링 상태를 보여줍니다.  URL들이 처리되는 과정을 보여주기 위해 비동기적으로 각각의 URL들의 상태가 나타납니다.  각각의 URL들의 크롤링이 성공하면 성공, 비정상적인 주소를 입력받았거나 프로그램상의 이유로 크롤링이 실패하면 실패, 파일에서 중복된 URL이 있는경우 중복으로 상태가 나타납니다.

### 오픈소스 프로젝트 분석리스트

![mainpage2](https://user-images.githubusercontent.com/45915619/85197799-6601b480-b31e-11ea-8d74-0aacabf2ea72.png)

이 리스트는 오픈소스 프로젝트 web page URL들을 파일에 넣어 입력한 후  크롤링을 한 결과를 보여줍니다.  크롤링 상태표에서 실패하거나 중복된 URL들을 제거한 분석에 성공한 URL들의 결과가 나타납니다.  

-- URL
- 각 URL의 주소

-- 전체 단어수
- 분석된 웹 페이지의 전체 단어수

-- 처리시간
- 크롤링 및 단어 빈도 수 측정 처리시간입니다.  단어 빈도 수 측정에서는 공백, 숫자, 기호, stopwords를 제거한 단어만이 단어로 취급됩니다.

-- 처리
- 단어 빈도 수가 측정된 URL들에 대한 결과는 엘라스틱서치에 저장되어 TF-IDF, Cosine Similarity, Word Cloud 등 다양한 데이터 분석을 하는데 자료로 쓰여집니다.






### 단어분석 버튼
단어분석 버튼을 누르면 해당 URL의 TF-IDF 기반 상위 10개의 단어 리스트를 보여줍니다. TF-IDF(Term Frequency - Inverse Document Frequency)는 여러 문서로 이루어진 문서군이 있을 때 어떤 단어가 특정 문서에서 얼마나 중요한 것인지를 나타내는 수치입니다. 특정한 단어가 문서 내에 얼마나 자주 등장하는 지를 나타내는 TF 값과 특정 단어가 모든 문서 전체에서 얼마나 공통적인지를 나타내는 IDF 값을 곱하여 TF-IDF값을 구합니다. 한 문서 내에서 TF-IDF 수치가 높은 단어는 모든 문서와 비교했을 때 현재 문서에서 두드러지게 나타나는 단어입니다. 파일을 입력하였을 때에 단어분석 버튼을 누르면 파일에 있는 모든 URL들의 TF-IDF값을 구하여 해당 문서에서 높은 TF-IDF값을 가지는 상위 10개의 단어를 보여줍니다. 단일 URL을 입력하면 문서가 하나 밖에 없어 비교할 문서가 없기 때문에 결과가 나타나지 않습니다.

![tf-idf](https://user-images.githubusercontent.com/45915619/85199167-774fbe80-b328-11ea-8605-9c350dc99945.png)

### 유사도분석 버튼
유사도 분석 버튼을 누르면 해당 URL과 코사인 유사도가 높은 상위 3개의 URL 리스트를 보여줍니다. 코사인 유사도는 두 벡터 간 코사인 각도를 이용하여 구할 수 있는 두 벡터의 유사도를 의미합니다. 코사인 유사도는 -1이상 1이하의 값을 가지며 1에 가까울 수록 두 벡터의 유사도가 높다고 판단할 수 있습니다. 유사도 분석 버튼을 누르면 해당 url과 데이터베이스 내에 저장된 다른 모든 url간의 각 코사인 유사도를 구하여 코사인 유사도가 높은 상위 3개의 url을 보여줍니다. 

![cosinesimilarity](https://user-images.githubusercontent.com/45915619/85200980-b553df00-b336-11ea-896f-4de03066690c.png)

### 워드클라우드 버튼
워드클라우드 버튼을 누르면 해당 URL의 워드 클라우드를 보여줍니다. 워드클라우드에서 보여주는 단어의 중요도의 기준은 단어의 빈도 수 입니다. 빈도 수가 높은 단어일수록 워드 클라우드에서 큰 크기를 차지합니다. 

![word_cloud](https://user-images.githubusercontent.com/45915619/85199242-fcd36e80-b328-11ea-867b-172f8c802035.png)

### ToCsv 버튼
ToCsv 버튼을 누르면 입력한 파일 혹은 단일 URL의 크롤링 결과 전체를 엑셀로 저장합니다. 크롤링 시 결과를 저장하는 데이터베이스 안에는 url 명, stopword를 제외한 전체 단어, 각 단어의 빈도 수, 전체 단어 수, 처리 시간 이 저장되어있습니다. 따라서 엑셀 파일에는 위의 5개 행에 부합하는 내용이 저장됩니다. 

![csv파일](https://user-images.githubusercontent.com/45915619/85199243-fe049b80-b328-11ea-8f28-b963b6d51cc9.png)



