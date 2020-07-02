import string
import os
import re

import pandas as pd 

from decimal import *
from heapq import nlargest
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

lemmatizer = WordNetLemmatizer()
def clean_text(text):
    text = re.sub("\'", "", text) 
    text = re.sub("[^a-zA-Z]"," ",text) 
    text = ' '.join(text.split()) 
    text = text.lower()
    _t = ""
    for t in text.split():
        _t += lemmatizer.lemmatize(t, pos='a') + " "
    text = _t
    text = remove_stopwords(text)

    return text

def corpora_train():
    # corpus load as model_data.csv
    corpora_data = pd.read_csv('model-data.csv')

    # tfidf vectorizer on corpus
    tfidf_vect = TfidfVectorizer(max_df=0.8, max_features=1000)
    tfidf_vect.fit_transform(corpora_data['text'])

    return tfidf_vect

# return list of (N% of text)-most frequent words in a text
def freq_dist(text):

    wordlist = list(word_tokenize(text))
    freq_dict = dict(Counter(wordlist)) 
    list_keywords = nlargest(round(0.10*len(wordlist)), freq_dict, key = freq_dict.get)
    
    
    scr_list_keywords = []
    scale = len(list_keywords)
    for i in range(0, scale):
        getcontext().prec = 2
        scr_list_keywords.append(round((scale-i)/scale, 2))

    return list_keywords, scr_list_keywords