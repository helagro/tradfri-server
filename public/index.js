
function main(){
    getJSON("isTradfriSetup", jsonRequestCallback)
}

function jsonRequestCallback(status, response){
    if(status === null){
        if(response.isSetup){
            document.getElementById("needsRaspiSetup").style.display = "block"
        } else{
            console.log("Tradfri handler is not set up")
        }
    }
}


main()