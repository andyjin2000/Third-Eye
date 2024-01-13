## should be able to accept requests from the app 
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask Server!"

@app.route('/getdata', methods=['GET'])
def get_data():
    return jsonify({'data': 'Sample Data'})

@app.route('/postdata', methods=['POST'])
def post_data():
    data = request.json
    return jsonify({'message': 'Data received', 'received_data': data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)