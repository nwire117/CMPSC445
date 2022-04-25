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

            document.getElementById("accuracy").innerHTML = obj["ticker"].toUpperCase() + " Prediction Graph";
           console.log(obj);

        }
    };

    // Send request
    http.send(payloadJSON);


    
}

document.addEventListener("DOMContentLoaded", function(event) {
    document.querySelectorAll('img').forEach(function(img){
       img.onerror = function(){this.style.display='none';};
    })
 });

 // Get the input field
var input = document.getElementById("ticker");

// Execute a function when the user releases a key on the keyboard
document.addEventListener("keyup", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("button").click();
  }
});

function showGraph(){
    let image = document.getElementById("graph");
    image.src  = "static/graph.png"
    document.getElementById("btnID").style.display = "none";

}
