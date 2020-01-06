import requests
from bs4 import BeautifulSoup
import time
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.3'}

f = open('C:/Users/97967/Desktop/baidu.doc','a+')

def get_info(url):
    res = requests.get(url,headers=headers)
    if res.status_code == 200:
        contents = re.findall('<p(.*?)</p>',res.content.decode('utf-8'),re.S)
        print(contents)
        # for content in contents:
        #     f.write(content+'\n')
    else:
        pass

if __name__ == '__main__':
    urls = ['https://wenku.baidu.com/view/bee47dcc4a35eefdc8d376eeaeaad1f34793114e']
    for url in urls:
        get_info(url)
        time.sleep(1)
f.close()