const FORM = document.getElementById("mainForm")
const GENERATED_ITEMS_DIV = document.getElementById("generatedItems")


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
    createInputsForEveryItem(json, 1, GENERATED_ITEMS_DIV)
}

function createInputsForEveryItem(json, depth, parent){
    for(var [key, value] of Object.entries(json)){
        console.log(key, value);
        if(value !== null && (typeof value === 'object' || Array.isArray(value))) {
            const div = createInputDiv(key, depth, parent)
            createInputsForEveryItem(value, depth + 1, div)
        } else{
            createInputForItem(key, value, parent)
        }
    }
}

function createInputDiv(key, depth, parent){
    const div = document.createElement("div")
    div.style.marginLeft = `${depth*2}em`
    div.className = "inputLayerDiv"

    const p = document.createElement("p")
    p.innerText = key
    p.style.fontWeight = "bold"
    div.appendChild(p)

    const button = document.createElement("button")
    button.innerText = "+"
    button.type = "button"
    button.className = "inputElementAdd"
    button.addEventListener("click", function(){
        createInputForItem("", "", div)
    })
    div.appendChild(button)

    GENERATED_ITEMS_DIV.appendChild(div)
    return div
}   


function createInputForItem(key, item, parent){
    console.log("item", item)

    const div = document.createElement("div")
    div.className = "inputElementDiv"

    const label = document.createElement("input")
    label.className = "inputLabel"
    label.value=key
    label.name = key
    
    div.appendChild(label)

    const input = document.createElement("input")
    input.className = "input"
    input.value = item
    input.name = item
    div.appendChild(input)

    parent.appendChild(div)
    
}


function submittBtn(){
    
}


main()