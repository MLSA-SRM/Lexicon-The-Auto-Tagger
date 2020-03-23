from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import json
import sys

#----------------Pre-Run----------------------
# train tfidf corpora
# load ml models into program memory
sys.path.insert(1, 'C:/Users/Powerhouse/Documents/GitHub/Project-High/project_high/Model/')
import model_pred 

app = Flask(__name__)
CORS(app, support_credentials=True)

#-----------------Routes----------------------

# default api endpoint [TEST]
@app.route('/', methods=['GET'])
def hello_world():
    response = jsonify({'data': 'Default API Endpoint'})
    return response

# return article data sent from ext [TEST]
@app.route('/RetPost', methods=['POST'])
def return_article_post_test():
    print('called /RetPost')
    req = json.loads(request.data)
    print(req)

    res = jsonify({"message": "OK", "status":200})
    return res

# return article data sent from ext [FUNCTION]
@app.route('/extToModel', methods=['POST'])
def returnTagsForArticleSent():
    print('called /extToModel')

    # recv data as json dict
    req = json.loads(request.data)
    _title = req['title']
    _article = req['article']
    #print(_title, _article)
    
    # return_text_tags
    tags = model_pred.text_return_tags(_article, _title)
    print(tags)

    # respond with status 200 OK | tags as JSON
    response = jsonify({"message":"OK", "status":200, "tags":tags})
    return response