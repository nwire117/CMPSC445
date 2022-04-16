import flask
from flask import Flask, send_from_directory, request, json
app = Flask(__name__)



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