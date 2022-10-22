const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
let deviceJson

function main(){
    deviceJson = urlParams.get('device')
    device = JSON.parse(deviceJson)

    performAction(urlParams.get("action"), deviceJson, urlParams.get("payload"))
    fillElements(device)
}


function performAction(action, deviceJson, payload){
    if(action !== null){
        getJSON(`deviceControlJson?device=${deviceJson}&action=${action}&payload=${payload}`, actionListener)
    } else{
        console.log("action is not specified")
    }
}

function actionListener(status, json){
    console.log(json)

    if(json != null){
        alert("color: " + json.color)
    }
}


function fillElements(device){
    document.getElementById("deviceName").innerText = device.name
    document.getElementById("deviceId").innerText = device.id
}


function replaceQueryParam(param, newval, search) {
    var regex = new RegExp("([?;&])" + param + "[^&;]*[;&]?");
    var query = search.replace(regex, "$1").replace(/&$/, '');

    return (query.length > 2 ? query + "&" : "?") + (newval ? param + "=" + newval : '');
}


//========== LISTENERS ==========

function toggleOnOff(){
    performAction("setState", deviceJson, "toggle")
}

function tOn(){
    performAction("tOn", deviceJson, null)
}

function sendControlFormula(){
    let actionSelect = document.getElementById("actionSelect")
    let payloadInput = document.getElementById("payloadInput")
    performAction(actionSelect.value, deviceJson, payloadInput.value)
}


main()