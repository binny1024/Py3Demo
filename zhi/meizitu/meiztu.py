import os
import ssl

import lxml.html
# import xlwt
import requests
# import time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/79.0.3945.88 Safari/537.36'}

# def url_open(url):
#     req = urllib.request.Request(url)
#     req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                          'Chrome/79.0.3945.88 Safari/537.36')
#     response = urllib.request.urlopen(req)
#     html = response.read()
#     return html


download_links = []
path = './photo/'
urls = ['https://www.mzitu.com/xinggan/']
for url in urls:
    res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.text, 'html.parser')
imgs = soup.select('li > a > img')

ssl._create_default_https_context = ssl._create_unverified_context
for img in imgs:
    print(img.get('data-original'))
    download_links.append(img.get('data-original'))
if not os.path.exists(path):
    os.mkdir(path)
for item in download_links:
    print('1')
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/79.0.3945.88 Safari/537.36')]
    urllib.request.install_opener(opener)
    urlretrieve(item, path + item[-10:])

#         all_info_list.append(info_list)
#     time.sleep(1)
#
# if __name__ == '__main__':
#     for url in urls:
#         get_info(url)
#     header = ['title','author','stytle','complete','introduce','word']
#
#     book = xlwt.Workbook(encoding='utf-8')
#     sheet = book.add_sheet('Sheet1')
#     for h in range(len(header)):
#         sheet.write(0,h,header[h])
#     i = 1
#     for list in all_info_list:
#         j = 0
#         for data in list:
#             sheet.write(i,j,data)
#             j +=1
#         i +=1
#
# book.save('xioashuo.xls')


# for url in urls:
#     html = requests.get(url,headers=headers)
#     selector = etree.HTML(html.text)
#     infos = selector.xpath('//tr[@class="item"]')
#     for info in infos:
#         name = info.xpath('td/div/a/@title')[0]
#         url = info.xpath('td/div/a/@href')[0]
#         book_infos = info.xpath('td/p/text()')[0]
#         author = book_infos.split('/')[0]
#         publisher = book_infos.split('/')[-3]
#         date = book_infos.split('/')[-2]
#         price = book_infos.split('/')[-1]
#         rate = info.xpath('td/div/span[2]/text()')[0]
#         comments = info.xpath('td/p/span/text()')
#         comment = comments[0] if len(comments) !=0 else "空"
#         writer.writerow((name,url,author,publisher,date,price,rate,comment))
#
# fp.close()
#
#
# //*[@id="content"]/div/div[1]/div/table[1]/tbody/tr/td[2]/div[1]
# //*[@id="content"]/div/div[1]/div/table[1]/tbody/tr/td[2]/div[1]/a
# /html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/h4/a
# /html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/h4/a
# /html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[1]
# /html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[1]/a[1]
# /html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[1]/a[2]
# /html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[1]/a[3]
# /html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[1]/span
# /html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[2]/text()
# /html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[3]/span/text()
