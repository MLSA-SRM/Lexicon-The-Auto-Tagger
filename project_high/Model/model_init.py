import string
import os
import re
import joblib

import pandas as pd 
import numpy as np

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

def load_tag_machines():
    # load features
    ml_features = []
    ml_features_models = []
    for file in os.scandir(path='project_high/Model/model_pickle_files'):
        ml_features.append(file.name[:-4]) 
        ml_features_models.append(joblib.load('project_high/Model/model_pickle_files/' + file.name))

    return ml_features, ml_features_models