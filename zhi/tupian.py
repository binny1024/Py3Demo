import os

from bs4 import BeautifulSoup
import requests
import json

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

url_path = 'https://www.pexels.com/search/'
word = input('请输入你要下载的图片：')
# js_data = json.loads(word)
# content = js_data['english']
url = url_path + word + '/'
print(url)
# https://www.pexels.com/search/book/
wb_data = requests.get(url, headers=headers)
soup = BeautifulSoup(wb_data.text, 'lxml')
imgs = soup.select(
    'article > a > img')  # body > div.page-wrap > div.search > div.search__grid > div.photos > div > div:nth-child(1) > article > a.js-photo-link.photo-item__link > img
list = []
for img in imgs:
    photo = img.get('src')
    list.append(photo)

path = './photo/'

if not os.path.exists(path):
    os.mkdir(path)
    print('path' + path)

for item in list:
    data = requests.get(item, headers=headers)
    fp = open(path + item.split('?')[0][-10:], 'wb')
    fp.write(data.content)
    fp.close()
