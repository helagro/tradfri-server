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



//ANCHOR listeners

let wasOn = true
function toggleOnOff(){
    let payload = wasOn ? 0 : 1
    wasOn = !wasOn

    performAction("setState", deviceJson, payload)
}


function tOn(){
    performAction("tOn", deviceJson, null)
}


main()