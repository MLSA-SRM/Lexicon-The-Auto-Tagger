from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import pandas as pd

import json
import sys

app = Flask(__name__)
CORS(app, support_credentials=True)

#-----------------Routes----------------------

# default api endpoint [TEST]
@app.route('/', methods=['GET'])
def hello_world():
    response = jsonify({'data': 'Default API Endpoint'})
    return response

# return article data sent from ext [TEST]
@app.route('/scrapeDataMaster', methods=['POST'])
def return_article_post_test():
    df = pd.DataFrame(columns=['Links'])

    print('called /RetPost')
    req = json.loads(request.data)
    print(len(req['link']))
    df['Links'] = req['link']
    df.to_csv('link_list.csv', mode='a', header=False)
    

    res = jsonify({"message": "OK", "status":200})
    return res
