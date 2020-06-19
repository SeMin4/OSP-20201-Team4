
function changeFormSingleURL(){
    var menu = document.getElementById("menu")
    var inputArea = document.getElementById("inputArea")
    var fileGroup = document.getElementById("fileGroup")
    var form = document.getElementById("urlForm")
    menu.innerHTML="Single URL"
    if(inputArea.hidden){
    form.reset()
    inputArea.hidden = false
    fileGroup.hidden = true
    
    }
    inputArea.setAttribute('placeholder', "Single URL을 입력해 주세요.")
}

function changeFormFile(){
    var menu = document.getElementById("menu")
    var inputArea = document.getElementById("inputArea")
    var fileGroup = document.getElementById("fileGroup")
    var form = document.getElementById("urlForm")
    menu.innerHTML = "Files"
    if(fileGroup.hidden){
    form.reset();
    inputArea.hidden = true;
    fileGroup.hidden = false;
    }
}
  
