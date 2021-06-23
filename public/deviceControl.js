
function main(){
    const device = getDevice()
    console.log("silent", device)
    fillElements(device)
}

function getDevice(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const deviceStr = urlParams.get('device')
    const device = JSON.parse(deviceStr)
    return device
}

function fillElements(device){
    document.getElementById("deviceName").innerText = device.name
    document.getElementById("deviceId").innerText = device.id
}






main()