#IMPORTING THE LIBRARIES TO BE USED IN SCRAPPING
import os
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

from datetime import datetime, timedelta
import re
import time


#DEFINING THE FUNCTIONS TO BE USED IN SCRAPPING


def base_url_builder(tag):
    url = "https://medium.com/tag/" + tag +"/archive/"
    return url


def get_start_date(year, month, day):
    #CONVERTS TO DATETIME OBJECT
    try:
        start_date = datetime(year, month, day)
    except:
        raise Exception("Start date is in the wrong format or is invalid.")
    return start_date


def get_end_date(year, month, day):
    #CONVERTS TO DATETIME OBJECT
    try:
        end_date = datetime(year, month, day)
    except:
        raise Exception("End date is in the wrong format or is invalid.")
    return end_date


def open_chrome():
    #OPENS A CHROME DRIVER
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    return driver


def url_masher(base_url, year, month, day):
    #MAKES A NEW URL FRON GIVEN DATE
    #THE FORMAT OF THE URL IS YYYY/MM/DD WE MUST MATCH IT
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    #MASH THE STRINGS TOGETHER TO MAKE A PASSABLE URL
    url = base_url + year + "/" + month + "/" + day
    return url



def find_post_cards(soup):
    #PULLS EACH CARD FROM THE FEED. EACH CARD IS A STORY OR COMMENT
    cards = soup.find_all("div", class_="streamItem streamItem--postPreview js-streamItem")
    return cards



def get_titles_from_cards(cards):
    #PULLS TITLE DATA FROM EACH CARD IN CARDS, RETURNS A LIST OF TITLES
    def title_cleaner(title):
        #REMOVE MEDIUMS ENCODING SYMBOLS AND EMOJIS FROM TITLES
        title = title.replace("\xa0"," ")
        title = title.replace("\u200a","")
        title = title.replace("\ufe0f","")
        title = re.sub(r'[^\x00-\x7F]+','', title)
        return title

    titles=[]
    for card in cards:
        #3 DIFF CLASSES
        variant1 = card.find("h3", class_="graf graf--h3 graf-after--figure graf--title")
        variant2 = card.find("h3", class_="graf graf--h3 graf-after--figure graf--trailing graf--title")
        variant3 = card.find("h4", class_="graf graf--h4 graf--leading")
        variant4 = card.find("h3", class_="graf graf--h3 graf--leading graf--title")
        variant5 = card.find("p", class_="graf graf--p graf--leading")
        variant6 = card.find("h3", class_="graf graf--h3 graf--startsWithDoubleQuote graf--leading graf--title")
        variant7= card.find("h3", class_="graf graf--h3 graf--startsWithDoubleQuote graf-after--figure graf--trailing graf--title")
       
        variants = [variant1, variant2, variant3, variant4, variant5, variant6, variant7]
        saved = False
       
        for variant in variants:
            if ((variant is not None) and (not saved)):
                title = variant.text
                title = title_cleaner(title)
                titles.append(title)
                saved = True
        if not saved:
            titles.append("NaN")
    return titles




def get_subtitles_from_cards(cards):
    #A LIST OF TITLES
    def subtitle_cleaner(subtitle):
        #REMOVE MEDIUMS ENCODING SYMBOLS AND EMOJIS FROM TITLES
        subtitle = subtitle.replace("\xa0"," ")
        subtitle = subtitle.replace("\u200a","")
        subtitle = subtitle.replace("\ufe0f","")
        subtitle = re.sub(r'[^\x00-\x7F]+','', subtitle)
        return subtitle

    subtitles=[]
    for card in cards:
        #3 DIFF CLASSES
        variant1 = card.find("h4", class_="graf graf--h4 graf-after--h3 graf--subtitle")
        variant2 = card.find("h4", class_="graf graf--h4 graf-after--h3 graf--trailing graf--subtitle")
        variant3 = card.find("strong", class_="markup--strong markup--p-strong")
        variant4 = card.find("h4", class_="graf graf--p graf-after--h3 graf--trailing")
        variant5= card.find("p", class_="graf graf--p graf-after--h3 graf--trailing")
        variant6= card.find("blockquote", class_="graf graf--pullquote graf-after--figure graf--trailing")
        variant7 = card.find("p", class_="graf graf--p graf-after--figure")
        variant8 = card.find("blockquote", class_="graf graf--blockquote graf-after--h3 graf--trailing")
        variant9 = card.find("p", class_="graf graf--p graf-after--figure graf--trailing")
        variant10 = card.find("em", class_="markup--em markup--p-em")
        variant11=card.find("p", class_="graf graf--p graf-after--p graf--trailing")
       
        variants = [variant1, variant2, variant3, variant4, variant5, variant6, variant7, variant8, variant9, variant10, variant11]
        saved = False
        for variant in variants:
            if ((variant is not None) and (not saved)):
                subtitle = variant.text
                subtitle = subtitle_cleaner(subtitle)
                subtitles.append(subtitle)
                saved = True
        if not saved:
            subtitles.append("NaN")
    return subtitles





def get_dates_and_tags(tag, year,month,day,cards):
    Year=[]
    Month=[]
    Day = []
    tags=[]
    for card in cards:
        tags.append(tag)
        Year.append(year)
        Month.append(month)
        Day.append(day)
    return Year, Month, Day, tags




def get_applause_from_cards(cards):
    #PULL CLAPS FROM CARDS
    applause=[]
    for card in cards:
        claps=card.find("button", class_="button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents")
        if claps is not None:
            applause.append(claps.text)
        else:
            applause.append("0")
    return applause




def get_urls_from_cards(cards):
    #GETS ARTICLE URLS FROM ALL
    urls = []
    for card in cards:
        url = card.find("a", class_="")
        if url is not None:
            urls.append(url['href'])
        else:
            raise Exception("couldnt find a url")
    return urls



def scrape_tag(tag, yearstart, monthstart, yearstop, monthstop):
   
    path = os.getcwd()
    path = path + "/TAG_SCRAPES/medium_"+tag+".csv"
    #3. TRY TO OPEN FILE PATH
    try:
        file = open(path, "w")
        file.close()
    except:
        raise Exception("Could not open file.")

    #START DATE <= STOP DATE
    current_date = get_start_date(int(yearstart), int(monthstart), 1)
    end_date = get_start_date(int(yearstop), int(monthstop), 1)
    if current_date > end_date:
        raise Exception("End date exceeds start date.")
    else:
        None
#
    #SCRAPING

    
    base_url = base_url_builder(tag)
    chrome_driver = open_chrome()
    
    firstPage=True
    counter=0

    #START ITERATION OVER DATES
    while(current_date <= end_date):
        #BUILD URL FROM CURRENT_DATE
        url = url_masher(base_url,
                        str(current_date.year),
                        str(current_date.month),
                        str(current_date.day))

        #PARSE WEB RESPONSE

        response = chrome_driver.get(url)


        soup = BeautifulSoup(chrome_driver.page_source, features='lxml')

        #FIND ALL STORY CARDS, EACH IS AN ARTICLE
        cards = find_post_cards(soup)


        #PULL DATA FROM CARDS
        titles = get_titles_from_cards(cards)
        subtitles = get_subtitles_from_cards(cards)
        year, month, day, tags = get_dates_and_tags(tag,
                                        current_date.year,
                                        current_date.month,
                                        current_date.day,
                                        cards)
       
       
       
        applause = get_applause_from_cards(cards)
        urls = get_urls_from_cards(cards)
        
        

        
        dict = {"Title":titles,"Subtitle":subtitles,"Image":images,"Author":authors, "Publication":pubs, "Year":year, "Month":month, "Day":day, "Tag":tags, "Reading_Time":readingTimes, "Claps":applause,"Comment":comment, "url":urls, "Author_url":auth_urls}

        #CHECK THAT DATA IN EACH CATEGORY IS THE SAME LENGTH
        vals = list(dict.values())
        for col in vals:
            if len(col)==len(cards):
                continue
            else:
                raise Exception("Data length does not match number of stories on page.")

       
        df = pd.DataFrame.from_dict(dict)

  
        # IF FIRSTPAGE-> ADD A HEADER
        if firstPage:
            with open(path, 'a') as f:
                df.to_csv(f, mode="a", header=True, index = False)
            firstPage=False
        #IF NOT FIRSTPAGE -> NO HEADER
        else:
            with open(path, 'a') as f:
                df.to_csv(f, mode="a", header=False, index=False)

        
       
    chrome_driver.close()
