const FORM = document.getElementById("mainForm")
const jsonArea = document.getElementById("jsonArea")


function main(){
    getJSONObjectFromUrlParams(jsonRequestCallback)
}

function jsonRequestCallback(status, response){
    if(status === null){
        console.log("res", response)
        processJsonDocument(response)
    }
}

function processJsonDocument(json){
    let jsonString = JSON.stringify(json) 
    let tabI = 0
    
    for(let i = 0; i<jsonString.length; i++){
        let letter = jsonString[i]
        let insertTextLeng
        const tabs = generateTabs(tabI)
        let insertStr = `\n${tabs}`;
        switch (letter){
            case "[":
            case "{": 
                insertStr += "   "
                tabI ++
            case ",": 
                [insertTextLeng, jsonString] = insert(insertStr, jsonString, i)
                i += insertTextLeng
                break
            case "]":
            case "}":
                tabI --
                [insertTextLeng, jsonString] = insert(insertStr, jsonString, i-1)
                i += insertTextLeng
                
        }
    }

    jsonArea.value = jsonString
}

function insert(insertText, jsonString, i){
    const insertTextLeng = insertText.length
    const insertI = i+1
    const newText = jsonString.slice(0, insertI) + insertText + jsonString.slice(insertI);
    return [insertTextLeng, newText]
}

function generateTabs(tabI){
    const TAB = "   "
    var newString = ""
    for (let i = 0; i<= tabI; i++){
        newString += TAB
    }
    return newString
}


main()