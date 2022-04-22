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
    
    var url = "http://localhost:8000";   // The URL and the port number must match server-side
    var endpoint = "/tick";            // Endpoint must match server endpoint

    var http = new XMLHttpRequest();

    ticker = document.getElementById("ticker").value;

    var payloadObj = { "ticker" : ticker };
    var payloadJSON = JSON.stringify(payloadObj);


    // prepare POST request
    http.open("POST", url+endpoint, true);
    http.setRequestHeader("Content-Type", "application/json");

    http.onreadystatechange = function() {
        var DONE = 4;       // 4 means the request is done.
        var OK = 200;       // 200 means a successful return.
        if (http.readyState == DONE && http.status == OK && http.responseText) {

            // JSON string
            var replyString = http.responseText;

            // convert JSON string into JavaScript object
            var obj = JSON.parse(replyString);

            document.getElementById("accuracy").innerHTML = obj["ticker"];

        }
    };

    // Send request
    http.send(payloadJSON);

    runPrediction();

    // testing local host updates 
}
