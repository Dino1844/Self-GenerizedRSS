#crawler.py and tokenizer

#kit.self.pachong() api

import requests
from bs4 import BeautifulSoup
import re
import jieba
# for test
# import feedparser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
def article(url):
    w = requests.get(url = url,headers = headers)
    soup = BeautifulSoup(w.text, 'html.parser')

    pattern = re.compile(r'[\u4e00-\u9fa5]') 
    chinese_text = soup.find_all(text=pattern)
    for text in chinese_text:
        if len(re.findall(r'[\u4e00-\u9fa5]', text)) > 4:
            print(text)



def tokenizer(text):
    return list(jieba.cut(text,HMM=True))