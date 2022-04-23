function runPrediction() {

    var url = "http://localhost:8000";  
    var endpoint = "/result";           
    
    var http = new XMLHttpRequest();
    // prepare GET request
    http.open("GET", url+endpoint, true);

http.onreadystatechange = function() {
    var DONE = 4;       // 4 means the request is done.
    var OK = 200;       // 200 means a successful return.
    if (http.readyState == DONE && http.status == OK && http.responseText) {

        // JSON string
        var replyString = http.responseText;

        var reply = JSON.parse(replyString);

        document.getElementById("trend").innerHTML = "JSON received: " + reply;
        // convert JSON string into JavaScript object and get the scores


    }
};

// Send request
http.send();
}


function setTicker(){
    document.getElementById("graph").innerHTML = ""
    var url = "http://localhost:8000";   // The URL and the port number must match server-side
    var endpoint = "/tick";            // Endpoint must match server endpoint

    var http = new XMLHttpRequest();

    ticker = document.getElementById("ticker").value;
    console.log(ticker);
    var payloadObj = { "ticker" : ticker };
    var payloadJSON = JSON.stringify(payloadObj);
    console.log(payloadJSON);


    // prepare POST request
    http.open("POST", url+endpoint, true);
    http.setRequestHeader("Content-Type", "application/json");

    http.onreadystatechange = function() {
        var DONE = 4;       // 4 means the request is done.
        var OK = 200;       // 200 means a successful return.
        if (http.readyState == DONE && http.status == OK && http.responseText) {

            // JSON string
            var replyString = http.responseText;
            console.log(replyString);

            // convert JSON string into JavaScript object
            var obj = JSON.parse(replyString);

            document.getElementById("accuracy").innerHTML = obj["ticker"];
           console.log(obj);

        }
    };

    // Send request 
    http.send(payloadJSON);

    runPrediction();

    const image = document.createElement('img')
    image.src  = 'main\graph.png'
    document.getElementById("graph").appendChild(image)

}

document.addEventListener("DOMContentLoaded", function(event) {
    document.querySelectorAll('img').forEach(function(img){
       img.onerror = function(){this.style.display='none';};
    })
 });