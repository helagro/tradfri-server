const backgroundElem = document.getElementById("backgroundElem")
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
let deviceJson

function main(){
    deviceJson = urlParams.get('device')
    device = JSON.parse(deviceJson)

    const action = urlParams.get("action")
    if(action !== null){
        performAction(action, deviceJson, urlParams.get("payload")) 
    }

    fillElements(device)
    getDeviceProperties()
}


function performAction(action, deviceJson, payload){
    if(action !== null){
        getJSON(`deviceControlJson?device=${deviceJson}&action=${action}&payload=${payload}`, actionListener)
    } else{
        console.log("action is not specified")
    }
}

function actionListener(status, jsonObj){
    console.log(jsonObj)

    if(jsonObj == null) return

    if("color" in jsonObj){
        const color = jsonObj["color"]
        backgroundElem.style.backgroundColor = "#" + color
        document.getElementById("deviceColor").innerHTML = color
    }

    if("brightness" in jsonObj){
        const brightness = jsonObj["brightness"]
        document.getElementById("deviceBrightness").innerHTML = brightness
    }
}

function getDeviceProperties(){
    performAction("getColor", deviceJson, null)
    performAction("getBrightness", deviceJson, null)
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