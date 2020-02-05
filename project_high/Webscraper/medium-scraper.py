import pandas as pd
import numpy as np
import time
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#-----GLOBAL-VARIABLES--------

# List of relevant tags
medium_tags_df = pd.read_csv('project_high/Data/medium-tag-list-dataset/medium_tag_1000.csv')
tag_list = list(medium_tags_df['Tags'])


#-----MISC-FUNCTIONS----------

# Finding common elements of two lists
# def common_member(a, b):  
#     c = [value for value in a if value in b]
#     if c != []:
#         return c
#     else:
#         return 'None'

# Processing text (nltk) for removing stopwords
def text_processor(text):
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(text)

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    return filtered_sentence

#----SCRAPER------------------

# Scraper function
def scrapeURL(url):
    # Getting Pages
    driver = webdriver.PhantomJS("C:/Users/Powerhouse/Documents/GitHub/Project-High/project_high/Webscraper/dependency/phantomjs-2.1.1-windows/bin/phantomjs.exe")
    driver.get(url)
    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    # Parse Page
    soup = BeautifulSoup(res, 'lxml')

    wok = True
    try:
        # Name
        name = soup.find('h1').getText()

        # Tags
        tags = []
        _li = soup.findAll('ul')
        li = []
        for _l in _li:
            for l in _l.findAll('li'):
                li.append(l.getText())
        for l in li:
            if l in tag_list:
                tags.append(l)

        # Text
        para = soup.findAll('p')
        text = ''
        for p in para:
            text = text + ' ' + p.getText()
        text = text_processor(text)
        
        # Return each row data
        eachDict = {'Name': name, 'Url': url, 'Text': text, 'Tags': tags}
    except:
        wok = False
    
    if wok:
        return eachDict
    else:
        return -1
    

#-----Iterative-MAIN----------------

# Can run multiple times | Saves after each scrape

# List of URLs to Scrape
tot_df = pd.read_csv('project_high/Data/medium-clean/Export-Medium-Data-950.csv')
url_list = list(tot_df['Url'])

# Check if file exists
try:
    done_df = pd.read_csv('article-database.csv')
    done_url_list = list(done_df.Url)
    isEx = True
except:
    isEx = False

# If file exists then check for done URLs
if(isEx):
    this_url_list = list(set(url_list)-set(done_url_list))
else:
    this_url_list = url_list

this_run = len(this_url_list)

# how many left
print(this_run)

if this_run >= 1:    
    for i in range(0, this_run):
        
        main_db = {'Name': [], 'Url': [], 'Text': [], 'Tags': []}

        dataIns = scrapeURL(this_url_list[i])

        if dataIns != -1:            
            main_db['Name'].append(dataIns['Name'])
            main_db['Url'].append(dataIns['Url'])
            main_db['Text'].append(dataIns['Text'])
            main_db['Tags'].append(dataIns['Tags'])

            if(isEx):
                pd.DataFrame(data=main_db).to_csv('article-database.csv', mode='a', header=False)
            else:
                pd.DataFrame(data=main_db).to_csv('article-database.csv')
                isEx = True

            print(main_db['Name'])
            print(i)
        else:
            continue
else:
    print('done')
    time.sleep(2)
