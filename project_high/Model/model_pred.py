import model_init as mod_i
import model_pickle_files as mod_pic
import corpora_machine as corps

from nltk.stem import PorterStemmer

# model first train
#import model_train

# corpora machine
text_idf = corps.corpora_train()

# model predict and generate tag list
ml_features, ml_features_models = mod_i.load_tag_machines()

## --TAG1/TAG2/TAG3--
def text_return_tags(text, title):
    # clean text
    cleaned_text = corps.clean_text(text)

    # new text to features
    text_ft = text_idf.transform([cleaned_text])

    # predict tags
    tag_list = []
    ps = PorterStemmer()
    _t = ""
    for t in title.split():
        _t += ps.stem(t) + " "
    title = _t
    for model_index in range(0, len(ml_features_models)):
        if ml_features[model_index] in title:
            if ml_features[model_index] in title or ps.stem(ml_features[model_index]) in title:
                continue
            else:
                tag_list.append(ml_features[model_index])
        else:
            y_pred = ml_features_models[model_index].predict(text_ft)
            if y_pred == 1:
                tag_list.append(ml_features[model_index])

    # suggest extra
    #   --option for extra tags available
    #   --multiprocessing

    tag_send = ''
    for t in tag_list:
        tag_send += t + '/'

    # return tags
    return tag_send

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

    try:
            name = soup.find('h1').getText()
    except:
        name = 'None'

    return text, name


def pred_machine(id):
    #find article id in article-data.csv

    #predict tags for article

    #send back string of tags
    


# local testing
# text, title = test_webscraper_function('https://uxdesign.cc/make-sense-of-rounded-corners-on-buttons-dfc8e13ea7f7')
# print(text_return_tags(text, title))