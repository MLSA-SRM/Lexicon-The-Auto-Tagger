import string
import os
import string
import re
import joblib

import pandas as pd 
import numpy as np

from scipy.sparse import csr_matrix
from nltk.corpus import stopwords
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

def test_webscraper_function(url):
    import selenium
    import bs4
    from bs4 import BeautifulSoup
    from selenium import webdriver

    # Getting Pages
    driver = webdriver.Chrome('project_high/Model/chromedriver.exe')
    driver.get(url)
    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    # Parse Page
    soup = BeautifulSoup(res, 'lxml')

    # Text
    para = soup.findAll('p')
    text = ''
    for p in para:
        text = text + ' ' + p.getText()
    # text = text_processor(text)

    return text

def clean_text(text):
    text = re.sub("\'", "", text) 
    text = re.sub("[^a-zA-Z]"," ",text) 
    text = ' '.join(text.split()) 
    text = text.lower() 
    
    stop_words = set(stopwords.words('english'))
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    clean_text = ' '.join(no_stopword_text)

    # return text
    return clean_text


def text_return_tags(text):
    # clean text
    cleaned_text = clean_text(text)

    # corpus load as model_data.csv
    corpora_data = pd.read_csv('project_high/Model/model-data.csv')

    # tfidf vectorizer on corpus
    tfidf_vect = TfidfVectorizer(max_df=0.8, max_features=1000)
    tfidf_global = tfidf_vect.fit_transform(corpora_data['Text'])
    
    # tfidf transform on new text
    text_ft = tfidf_vect.transform([cleaned_text])

    # load features
    ml_features = []
    ml_features_models = []
    for file in os.scandir(path='project_high/Model/model_pickle_files'):
        ml_features.append(file.name[:-4]) 
        ml_features_models.append(joblib.load('project_high/Model/model_pickle_files/' + file.name))

    # predict tags
    tag_list = []
    for model_index in range(0, len(ml_features_models)):
        y_pred = ml_features_models[model_index].predict(text_ft)
        if y_pred == 1:
            tag_list.append(ml_features[model_index])

    # suggest extra tags


    # return tags
    return tag_list

text = test_webscraper_function('https://medium.com/the-marketing-playbook/how-to-design-marketing-campaigns-the-importance-of-market-segmentation-71b11e1819c2')
print(text_return_tags(text))