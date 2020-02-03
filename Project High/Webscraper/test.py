import pandas as pd
import numpy as np
import time
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Misc Functions
def common_member(a, b):  
    c = [value for value in a if value in b]
    if c != []:
        return c
    else:
        return 'None'

def text_processor(text):
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(text)

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    return filtered_sentence

# Getting Pages
medium_tags_df = pd.read_csv('C:/Users/Powerhouse/Desktop/Project High/Data/medium-tag-list-dataset/medium_tag_1000.csv')
tag_list = list(medium_tags_df['Tags'])

url = 'https://towardsdatascience.com/web-scraping-is-now-legal-6bf0e5730a78'
driver = webdriver.PhantomJS("C:/Users/Powerhouse/Desktop/Project High/Webscraper/dependency/phantomjs-2.1.1-windows/bin/phantomjs.exe")

driver.get(url)
res = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()

# Parse Page
soup = BeautifulSoup(res, 'lxml')

# Name
name = soup.find('h1').getText()
print(name)

# Tags
li = soup.find('ul')
li = li.find_all('li')

tags = []
for l in li:
    x = str(l.find('a').getText())
    if x in tag_list:
        tags.append(x)

print(tags)

# Text
para = soup.findAll('p')
text = ''
for p in para:
    text = text + ' ' + p.getText()
print(text_processor(text))