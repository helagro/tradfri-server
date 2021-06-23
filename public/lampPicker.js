const deviceContainer = document.getElementById("devicesContainer")

function main(){
    console.log("everywhere")
    getJSON("lampPickerJson", jsonCallback)
}

function jsonCallback(status, json){
    if(status === null)
        createItemElements(json.devices)
}

function createItemElements(devices){
    for (const device of devices){
        createItemElement(device)
    }
}

function createItemElement(device){
    const div = document.createElement("div")
    div.className = "itemContainer"

    const name = document.createElement("p")
    name.innerText = device.name
    div.appendChild(name)

    const id = document.createElement("p")
    id.innerText = device.id
    div.appendChild(id)

    deviceContainer.appendChild(div)
}

main()