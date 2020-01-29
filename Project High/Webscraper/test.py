import urllib.request
import requests
import bs4
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#medium_story_df = pd.read_csv('C:/Users/Powerhouse/Desktop/Project High/Data/medium-story-dataset/Medium_Clean.csv')

url = 'https://medium.com/@RecastAI/how-to-make-your-chatbot-a-huge-success-two-dimensions-and-a-tip-3da221bdf731'
driver = webdriver.Chrome("C:/Users/Powerhouse/Desktop/Project High/Webscraper/chromedriver.exe")

driver.get(url)
res = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()

soup = BeautifulSoup(res, 'lxml')
li = soup.find('ul')
li = li.find_all('li')

for l in li:
    print(l.find('a').getText())

