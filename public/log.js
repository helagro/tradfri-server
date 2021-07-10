const logArea = document.getElementById("logArea")

function main(){
    getJSON("logJson", jsonCallback)
}

function jsonCallback(status, json){
    console.log("fese", json, status)
    if(status === null)
        createItemElements(json)
}

function createItemElements(entries){
    for (const entry of entries){
        createItemElement(entry)
    }
}

function createItemElement(entry){
    const p = document.createElement("p")
    p.innerText = entry

    logArea.appendChild(p)
}

main()