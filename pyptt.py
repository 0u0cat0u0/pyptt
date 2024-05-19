import requests
import re
import json
from bs4 import BeautifulSoup



headers = {
        'cookie':'over18=1;'
}



def ptt_url(url, max_articles, max_comment):
    try:
        ptt_data = []

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for articles_found in soup.find_all('div', class_='e7-right-top-container e7-no-outline-all-descendants', limit=max_articles):
            article_url = 'https://www.ptt.cc' + articles_found.find('a').get('href') + '.html'
            #print(article_url)
            
            article_data = ptt_article(article_url, max_comment)
            ptt_data.append(article_data)
    
        return ptt_data

    except Exception as e:
        print(f'Error: {str(e)}')



def ptt_article(article_url, max_comment):
    try:
        article_data = []

        response = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        article_title = soup.select_one('#main-content .article-metaline:nth-child(3) .article-meta-value').text
        article_title = re.sub(r'\s*\[.*?\]\s*', '', article_title)
        #print(article_title)

        if re.search('.*?\(發錢\).*?',article_title) or re.search('.*?（發錢）.*?',article_title):
            return
        
        for article in soup.find_all('div', class_='push', limit = max_comment):
            article_comment = article.find('span', class_='f3 push-content').text

            article_comment = re.sub('^:? ', '', article_comment)

            if not re.match('.*://.*',article_comment):
                #print(article_comment)
                article_data.append({
                "instruction": article_title,
                "input": "",
                "output": article_comment
                })
        
        return article_data
    except:
            return



def to_JSON():
    #url = 'https://www.pttweb.cc/hot/all/today'
    url = 'https://www.pttweb.cc/hot/not-news/today'

    ptt_data = ptt_url(url,30,300)

    with open('ptt_data1.json', 'w', encoding='utf-8') as f:
        json.dump(ptt_data, f, indent=4, ensure_ascii=False)



to_JSON()