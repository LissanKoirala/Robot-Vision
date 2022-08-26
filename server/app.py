from urllib import request
from flask import Flask, request, send_from_directory

app = Flask(__name__)


@app.route("/image", methods=["GET", "POST"])
def hello_world():
    
    # file = request.files['file']
    print(request.data)
    
    # do some processing here
    
    return "motor coordinates"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)