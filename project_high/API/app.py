from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, support_credentials=True)

# routes
@app.route('/', methods=['GET'])
def hello_world():
    response = jsonify({'data': 'Default API Endpoint'})
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/Ret', methods=['GET'])
def return_article_raw():
    
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'API_REQ_ERR:no-id'
    
    response = jsonify({'data': id})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/RetPost', methods=['POST'])
def return_article_id_post():

    req = json.loads(request.data)
    print(req)

    res = jsonify({"message": "OK", "status":200})
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res




    