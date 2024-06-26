import requests
import re
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



headers = {
        'cookie':'over18=1;'
}



def ptt_url(url, max_articles, max_comment):
    try:
        ptt_data = []

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for articles_found in soup.find_all('div', class_='e7-right-top-container e7-no-outline-all-descendants', limit=max_articles):
            article_title = articles_found.find('span', class_='e7-show-if-device-is-not-xs')
            
            try:
                article_title = article_title.text
                #print(article_title)

                if not (re.search('\s*\[發錢\]\s*',article_title) or re.search('\s*\[推投\]\s*',article_title) or re.search('.*?\(發錢\).*?',article_title) or re.search('.*?（發錢）.*?',article_title) or re.search('.*?直播單.*?',article_title)):
                    article_url = 'https://www.pttweb.cc' + articles_found.find('a').get('href')
                    #print(article_url)
                    
                    article_data = ptt_article(article_url, max_comment)
                    ptt_data += article_data
            except:
                print('無標題')

        return ptt_data

    except Exception as e:
        print(f'Error: {str(e)}')



def ptt_article(article_url, max_comment):
    article_data = []

    options = Options()
    options.headless = True # 设置为True可以在后台运行Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(article_url)

    try:
        load_all_button = driver.find_element(By.XPATH, '//div[text()="載入全部"]/parent::button')
        load_all_button.click()
    except:
        print('留言過少')

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    article_title = soup.find('h1', 'title mt-2').text.strip()
    article_title = re.sub('\s*Re:\s*', '', article_title)
    article_title = re.sub('\s*\[.*?\]\s*', '', article_title)
    print(article_title)
    
    for article in soup.find_all('div', class_='yellow--text text--darken-2 e7-recommend-message', limit = max_comment):
        article_comment = article.find('span')

        try:
            article_comment = article_comment.text

            if (not re.match('.*://.*',article_comment)):
                print(article_comment)

                article_data.append({
                "instruction": article_title,
                "input": "",
                "output": article_comment
                })
        except:
            print('無內文')
    
    return article_data



def to_JSON():
    #url = 'https://www.pttweb.cc/hot/all/today'
    url = 'https://www.pttweb.cc/hot/not-news/today'
    # url = 'https://www.pttweb.cc/hot/comic/today'

    ptt_data = ptt_url(url,5,5)

    with open('data/ptt_data2.json', 'w', encoding='utf-8') as f:
        json.dump(ptt_data, f, indent=4, ensure_ascii=False)

to_JSON()




# def test():
#     art_data = []    
#     art_data += ptt_article('https://www.pttweb.cc/bbs/C_Chat/M.1716257370.A.D36', 500)

#     with open('data/ptt_data2.json', 'w', encoding='utf-8') as f:
#         json.dump(art_data, f, indent=4, ensure_ascii=False)

# test()