const FORM = document.getElementById("mainForm")
const jsonArea = document.getElementById("jsonArea")


function main(){
    getJSONObjectFromUrlParams()
}

function getJSONObjectFromUrlParams(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const jsonUrl = urlParams.get('jsonUrl')

    getJSON(jsonUrl, jsonRequestCallback)
    console.log(queryString, urlParams, jsonUrl)
}

var getJSON = function(url, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

function jsonRequestCallback(status, response){
    if(status === null){
        console.log("res", response)
        processJsonDocument(response)
    }
}

function processJsonDocument(json){
    let jsonString = JSON.stringify(json) 
    let tabI = 0
    
    for(let i = 0; i<jsonString.length; i++){
        let letter = jsonString[i]
        switch (letter){
            case "{": 
                tabI ++
            case ",": 
                const tabs = generateTabs(tabI)
                let insertStr = "\n" + tabs
                let insertTextLeng
                [insertTextLeng, jsonString] = insert(insertStr, jsonString, i)
                i += insertTextLeng
                break
            case "}":
                tabI --
                
        }
    }

    jsonArea.value = jsonString
}

function insert(insertText, jsonString, i){
    const insertTextLeng = insertText.length
    const insertI = i+1
    const newText = jsonString.slice(0, insertI) + insertText + jsonString.slice(insertI);
    return [insertTextLeng, newText]
}

function generateTabs(tabI){
    const TAB = "   "
    var newString = ""
    for (let i = 0; i<= tabI; i++){
        newString += TAB
    }
    return newString
}


main()