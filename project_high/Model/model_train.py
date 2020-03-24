import numpy as np
import pandas as pd 
import time
import nltk
import string
import re
import os
import joblib
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

_debug = True

def debug(text):
    if _debug:
        print(text)

debug('Importing Parent Database..')
art_df = pd.read_csv('article-database.csv')
model_db = art_df.drop([art_df.columns[0], art_df.columns[2], art_df.columns[5]], axis=1)
model_db_clean = model_db.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False).reset_index(drop=True)

# from ast import literal_eval
def func(raw_tags):
    raw_split = raw_tags[1:-1].split(',')
    num_tags = len(raw_split)
    tags_clean = []
    tags_clean.append(raw_split[0][1:-1])
    for i in range(1, num_tags):
       tags_clean.append(raw_split[i][2:-1])
    return tags_clean

debug('Cleaning Parent Data..')
model_db_clean['Tags_clean'] = model_db_clean['Tags'].apply(lambda x: func(x))

multi_label_transform = MultiLabelBinarizer()
multi_label_transform.fit(model_db_clean['Tags_clean'])
y = multi_label_transform.transform(model_db_clean['Tags_clean'])

cols = []
for i in list(multi_label_transform.classes_):     
    cols.append(i)
cols.append('Text')

prepd_db = pd.DataFrame()

prepd_db.loc[:, 'Text'] = model_db_clean.loc[:, 'Text']
for i in range(0, y.shape[1]):
        prepd_db.loc[:, i+1] = y[:, i]

debug('Cleaning Parent Database Text..')
ps = PorterStemmer()
def clean_text(text):
    text = re.sub("\'", "", text) 
    text = re.sub("[^a-zA-Z]"," ",text) 
    text = ' '.join(text.split()) 
    text = text.lower()
    _t = ""
    for t in text.split():
        _t += ps.stem(t) + " "
    text = _t

    return text

prepd_db['Text_clean'] = prepd_db['Text'].apply(lambda x: clean_text(x))
prepd_db.drop(['Text'], axis=1, inplace=True)

prepd_db.columns = cols
prepd_db.drop([''], axis=1, inplace=True)

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

prepd_db['Text'] = prepd_db['Text'].apply(lambda x: remove_stopwords(x))

y = []
for i in range(0, prepd_db.shape[1]):
    x = prepd_db.iloc[:, i].value_counts()
    if x[1] > 500:
        y.append(x.name)

debug('Creating Corpus Database..')  
model_final_data = prepd_db[y]
model_final_data['Text'] = prepd_db['Text']
model_final_data['ID'] = range(0, model_final_data.shape[0])

article_id_db = model_final_data[['Text', 'ID']]

model_final_data.to_csv('model-data.csv')
article_id_db.to_csv('article-data.csv')

debug('Training Corpora Transform..')
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=1000)
train_tfidf = tfidf_vectorizer.fit_transform(model_final_data['Text'])

debug('Training Model [.pkl]..')
for x in range(0, len(model_final_data.columns)-2):

    lr = LogisticRegression(tol=0.75)
    lr.fit(train_tfidf, model_final_data.iloc[:, x])

    joblib.dump(lr, 'model_pickle_files/' + str(model_final_data.columns[x]) + '.pkl')

debug('Birth Database and Model Train Complete..')
time.sleep(5)