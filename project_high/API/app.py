from flask import Flask
from flask import request, jsonify

## Import Article DB
import pandas as import pd 
art_df = pd.read_csv()


app = Flask(__name__)

# routes
@app.route('/', methods=['GET'])
def hello_world():
    return 'Default API Endpoint'

@app.route('/Ret', methods=['GET'])
def return_article_raw():
    
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'API_REQ_ERR:no-id'
    
    return str(id)




    