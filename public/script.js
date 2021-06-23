function getJSONObjectFromUrlParams(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const jsonUrl = urlParams.get('jsonUrl')

    getJSON(jsonUrl, jsonRequestCallback)
    console.log(queryString, urlParams, jsonUrl)
}

var getJSON = function(url, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};