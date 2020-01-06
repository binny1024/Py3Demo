import requests
from bs4 import BeautifulSoup
import time
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

f = open('C:/Users/97967/Desktop/doupo.doc','a+')

def get_info(url):
    res = requests.get(url,headers=headers)
    if res.status_code == 200:
        contents = re.findall('<p>(.*?)</p>',res.content.decode('utf-8'),re.S)
        for content in contents:
            f.write(content+'\n')
    else:
        pass

if __name__ == '__main__':
    urls = ['http://www.doupoxs.com/doupocangqiong/{}.html'.format(str(i)) for i in range(1,2)]
    for url in urls:
        get_info(url)
        time.sleep(1)
f.close()