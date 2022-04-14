import standardizedData
# import Flask
from flask import Flask, send_from_directory, request, json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


# Send index.html
@app.route('/', methods=["GET"])
@app.route('/index.html', methods=["GET"])
def get_index():
    #return contents of index.html
    return send_from_directory('', 'index.html', mimetype='text/html')

# Send main.js
@app.route('/main.js', methods=["GET"])
def get_main():
     #return contents of main.js
    return send_from_directory('', 'main.js', mimetype='text/javascript')

# Run the server
if __name__ == '__main__':
        
    # start the server
    app.run(port = 8000)


# Send the result from machine learning
# Endpoint is "result"
@app.route('/result', methods=["GET"])
def result():

    # call the prediction function in ml.py
    result = standardizedData.prediction()

    # convert dictionary to JSON string
    resultString = json.dumps(result)

    return resultString

# Endpoint tick
@app.route('/tick', methods=["POST"])
def set_ticker():
    
    # get the payload as dictionary from client
    receivedDict = request.get_json()
    
    # From the dictionary get the value
    ticker = receivedDict["ticker"]
    standardizedData.setTicker(ticker)

    # make a dictionary from the result
    # in this example, the server always replies whatever the client sent + 1
    resultDict = { "ticker": ticker }
    
    # convert dictionary to JSON string
    resultString = json.dumps(resultDict)

    return resultString


# Run the server
if __name__ == '__main__':
    
    # train the model
    test =standardizedData.train()
    print(test)
    
    # start the server
    app.run(port = 8000)