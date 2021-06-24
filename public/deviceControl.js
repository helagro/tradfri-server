const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

function main(){

    performActionFromQueries()
    const device = getDevice()
    fillElements(device)
}


function performActionFromQueries(){
    if(urlParams.has("action")){
        getJSON(`deviceControlJson?device=${urlParams.get("device")}&action=${urlParams.get("action")}`, actionListener)
    }
}

function actionListener(status, json){
    console.log(json)
}


function getDevice(){
    const deviceStr = urlParams.get('device')
    const device = JSON.parse(deviceStr)
    return device
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




main()