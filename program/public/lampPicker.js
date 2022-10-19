const deviceContainer = document.getElementById("devicesContainer")

function main(){
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
    const a = document.createElement("a")
    a.className = "itemContainer"
    a.href = `deviceControl.html?jsonUrl=itemContainerJson&device=${JSON.stringify(device)}`

    const name = document.createElement("p")
    name.innerText = device.name
    a.appendChild(name)

    const id = document.createElement("p")
    id.innerText = device.id
    a.appendChild(id)

    deviceContainer.appendChild(a)
}

main()