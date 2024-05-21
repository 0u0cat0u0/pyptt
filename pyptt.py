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

        if re.search('\s*\[發錢\]\s*',article_title) or re.search('\s*\[推投\]\s*',article_title):
            return

        article_title = re.sub('\s*\[.*?\]\s*', '', article_title)
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
    #url = 'https://www.pttweb.cc/hot/not-news/today'
    url = 'https://www.pttweb.cc/hot/comic/today'

    ptt_data = ptt_url(url,30,300)

    with open('ptt_data2.json', 'w', encoding='utf-8') as f:
        json.dump(ptt_data, f, indent=4, ensure_ascii=False)



to_JSON()



""" 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time

# 初始化ChromeDriver
options = Options()
options.headless = True  # 设置为True可以在后台运行Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 打开网页
url = "https://www.pttweb.cc/bbs/C_Chat/M.1716253900.A.195"
driver.get(url)

# 循环点击“載入全部”按钮，直到按钮不存在
while True:
    try:
        # 查找包含“載入全部”文本的div元素，然后获取其父级button元素
        load_more_button = driver.find_element(By.XPATH, '//div[text()="載入全部"]/parent::button')
        load_more_button.click()
        time.sleep(2)  # 等待页面加载
        break
    except Exception as e:
        print(f"Exception occurred: {e}")
        # 按钮不存在时跳出循环
        break

# 获取加载后的页面内容
soup = BeautifulSoup(driver.page_source, "html.parser")


# 关闭WebDriver
driver.quit()
max_comment = 10
# 输出加载后的页面内容
article_title = soup.select_one('div' ,class_='yellow--text text--darken-2 e7-recommend-message').text
print(article_title)
 """