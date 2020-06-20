$("#csvDownBtn").click(function (event){
    $.ajax({
          type : 'GET',
          url : "/down/csv",
          dataType : "json",
          error : function(){
             // alert("통신실패!!!!");
          },
          success : function(data){
              var element = document.createElement('a'); 
              element.href =  '../static/csv/db.csv'
              element.download = "data.csv"
              document.body.appendChild(element)
              element.click()
              document.body.removeChild(element)
              console.log(data)
              
          }
      });
  });
  $("#submitBtn").click(function (event) {
    var crawlingContainer = document.getElementById("crawlingContainer")
    crawlingContainer.hidden = false;//감춰놧던걸 다시 보이기
    var crawlingList = document.getElementById("crawlingList")
    var crawlingBody = document.getElementById("crawling-body")
    crawlingList.innerHTML = ""//이미 있던 결과 날리기
    crawlingBody.innerHTML = ""//이미 있던 결과 날리기
    event.preventDefault();//submit 없애 버리고
    // DELETE
    $.ajax({//전부다 지우기 엘라스틱 안에 있는거
      url : "http://localhost:9200/*",
      type : 'DELETE',
      async : false,
      success : function(){
        console.log("success")
      },
      error : function(e){
        console.log(e)
      },
    })
    var form = $('#urlForm')[0];
    // Create an FormData object 
    var data = new FormData(form);
    var file = data.getAll("file");
    document.getElementById('csvDownBtn').disabled = false;
    if(file[0].name != ""){
      var reader = new FileReader()
      var results;
      reader.addEventListener("loadend", function() {
        results = reader.result;//파일 내용 읽기 끝!
        var result = results.split("\n")
        for(var i = 0 ; i < result.length; ++i){
          result[i] = result[i].trim()
        }
        console.log(result)
        var id = 1;
        var check = true
        for(var i = 0; i < result.length; ++i){
          check = true
          crawlingList.innerHTML += "<tr><th scope='row' class = 'text-center align-middle'>"+(i+1)+"</th><td class = 'text-center align-middle'>"+result[i]+"</td><td id = 'crawlingResult"+(i + 1)+"'"+" class = 'text-center align-middle'><div class='spinner-grow' style='width: 3rem; height: 3rem;' role='status'><span class='sr-only'>Loading...</span></div></td></tr> ";
          for(var j = 0; j < i; ++j){
            if(result[i] == result[j]){//url 중복 검사
              var resultRow = document.getElementById("crawlingResult"+(i+1))
              resultRow.innerHTML = ""
              resultRow.innerHTML = "<button type='button' class='btn btn-warning btn-circle btn-md' disabled>중복</button>"
              check = false
              
            }
          }
          if(!check)
            continue
          var bodyRow = "<tr> \
              <th scope='row' class = 'text-center align-middle'>"+id+"</th>\
              <td class = 'text-center align-middle'>"+result[i]+"</td>\
              <td id = 'wordcnt"+(id)+"' class = 'text-center align-middle'></td>\
              <td id = 'processtime"+(id)+"' class = 'text-center align-middle'></td>\
              <td class = 'text-center align-middle'>\
                <button type='button' class='btn btn-outline-success analysisBtn' data-toggle='modal' data-target='#tfidfModal' name="+result[i]+">단어 분석</button>&nbsp;&nbsp;&nbsp;\
                <button type='button' class='btn btn-outline-primary similarityBtn' data-toggle='modal' data-target='#similarityModal' name="+result[i]+">유사도</button>&nbsp;&nbsp;&nbsp;\
                <button type='button' class='btn btn-outline-info wordCloudBtn' data-toggle='modal' data-target='#wordCloudModal' name="+result[i]+">워드 클라우드</button>\
              </td>\
            </tr> "
          crawlingBody.innerHTML += bodyRow;
          getCrawlingInfo(result[i],id,i+1)
          id += 1
        }
        var elements = $('.analysisBtn')//이벤트 리스너 달기
        for(var i = 0; i < elements.length; i++){
          elements[i].addEventListener("click", function(){
            getTfidfInfo(this.name)
          });
        }
        elements = $('.similarityBtn')
        for(var i = 0; i < elements.length; i++){
          elements[i].addEventListener("click", function(){
            cosineSimilarityInfo(this.name)
          });
        }
        elements = $('.wordCloudBtn')
        for(var i = 0; i < elements.length; i++){
          elements[i].addEventListener("click", function(){
            wordCloudInfo(this.name)
          });
        }
      });
      reader.readAsText(file[0])
    }
    else{
      var singlueURL = data.getAll("url");
      crawlingList.innerHTML += "<tr><th scope='row' class = 'text-center align-middle'>"+1+"</th><td class = 'text-center align-middle'>"+singlueURL+"</td><td id = 'crawlingResult"+1+"'"+" class = 'text-center align-middle'><div class='spinner-grow' style='width: 3rem; height: 3rem;' role='status'><span class='sr-only'>Loading...</span></div></td></tr> ";
      var bodyRow = "<tr> \
            <th scope='row' class = 'text-center align-middle'>"+1+"</th>\
            <td class = 'text-center align-middle'>"+singlueURL+"</td>\
            <td id = 'wordcnt"+1+"' class = 'text-center align-middle'></td>\
            <td id = 'processtime"+1+"' class = 'text-center align-middle'></td>\
            <td class = 'text-center align-middle'>\
            <span class='d-inline-block' tabindex='0' data-toggle='tooltip' title='1개의 결과로 TF-IDF를 분석할 수 없습니다'>\
              <button type='button' class='btn btn-success' style='pointer-events: none;' disabled>단어 분석</button>&nbsp;&nbsp;&nbsp;\
            </span>\
            <span class='d-inline-block' tabindex='0' data-toggle='tooltip' title='1개의 결과로 Cosine-Similarity 를 분석할 수 없습니다'>\
              <button type='button' class='btn btn-primary' style='pointer-events: none;' disabled}>유사도</button>&nbsp;&nbsp;&nbsp;\
            </span>\
            <button type='button' class='btn btn-outline-info wordCloudBtn' data-toggle='modal' data-target='#wordCloudModal' name="+singlueURL+">워드 클라우드</button>\
          </td>\
        </tr> "
      crawlingBody.innerHTML += bodyRow;
      getCrawlingInfo(singlueURL,1,1)
      elements = $('.wordCloudBtn')
      for(var i = 0; i < elements.length; i++){
        elements[i].addEventListener("click", function(){
          wordCloudInfo(this.name)
        });
      }
    }

  });
  function getCrawlingInfo(url, id, i){
    $.ajax({
          type : 'GET',
          url : "/upload/File?url="+url+"&&id="+id,
          dataType : "json",
          error : function(){
            var resultRow = document.getElementById("crawlingResult"+i)
            resultRow.innerHTML = ""
            resultRow.innerHTML = "<button type='button' class='btn btn-danger btn-circle btn-md' disabled>실패</button>"
          },
          success : function(data){
            var resultRow = document.getElementById("crawlingResult"+i)
            resultRow.innerHTML = ""
            resultRow.innerHTML = "<button type='button' class='btn btn-success btn-circle btn-md' disabled>성공</button>"
            var analysisWordCntRow = document.getElementById("wordcnt"+data["id"])
            var analysisProcessRow = document.getElementById("processtime"+data["id"])
            analysisWordCntRow.innerHTML = data["wordcnt"]
            analysisProcessRow.innerHTML = data["processing_time"]
            console.log(data)
          }
      });
  }
  function getTfidfInfo(url){
    $.ajax({
          type : 'GET',
          url : "/analysis/tfidf?url="+url,
          dataType : "json",
          error : function(){
             // alert("통신실패!!!!");
          },
          success : function(data){
              console.log(data)
              tfIDFchart.data = [
                {
                  "word": data["word"][0],
                  "tfidf": data["percent"][0]
                },
                {
                  "word": data["word"][1],
                  "tfidf": data["percent"][1]
                },
                {
                  "word": data["word"][2],
                  "tfidf": data["percent"][2]
                },
                {
                  "word": data["word"][3],
                  "tfidf": data["percent"][3]
                },
                {
                  "word": data["word"][4],
                  "tfidf": data["percent"][4]
                },
                {
                  "word": data["word"][5],
                  "tfidf": data["percent"][5]
                },
                {
                  "word": data["word"][6],
                  "tfidf": data["percent"][6]
                },
                {
                  "word": data["word"][7],
                  "tfidf": data["percent"][7]
                },
                {
                  "word": data["word"][8],
                  "tfidf": data["percent"][8]
                },
                {
                  "word": data["word"][9],
                  "tfidf": data["percent"][9]
                }
              ]
              for(var i = 1; i <= 10; ++i){
                  var topword = document.getElementById("topWord"+i);
                  topword.innerHTML = data["word"][i - 1]
              }
          }
      });
  }

  function cosineSimilarityInfo(url){
    $.ajax({
          type : 'GET',
          url : "/analysis/cosineSimilarity?url="+url,
          dataType : "json",
          error : function(){
             //alert("통신실패!!!!");
          },
          success : function(data){
              similarityChart.data = [
                {
                  "url": data["url"][0],
                  "similiarity": data["percent"][0]*100
                },
                {
                  "url": data["url"][1],
                  "similiarity": data["percent"][1]*100
                },
                {
                  "url": data["url"][2],
                  "similiarity": data["percent"][2]*100
                }
              ]
              for(var i = 1; i <= 3; ++i){
                  var topURL = document.getElementById("cosineURL"+i)
                  topURL.innerHTML = data["url"][i - 1]
              }
              console.log(data)
          }
      });
  }
  function wordCloudInfo(url){
    var spinner = document.getElementById("imgSpinner")
    var img = document.getElementById("wordcloudImage")
    img.hidden = true;
    spinner.hidden = false;
    $.ajax({
          type : 'GET',
          url : "/make/wordcloud?url="+url,
          dataType : "json",
          error : function(){
             // alert("통신실패!!!!");
          },
          success : function(data){
              console.log(data)
              spinner.hidden = true
              img.hidden = false
              img.src = "../static/image/"+data["fname"]
          }
      });
  }
