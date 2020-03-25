import os

import requests
import re
from lxml import etree
import pymysql
import time

# conn = pymysql.connect(host='localhost', user='root', passwd='02100426lhz', db='mydb',
#                        port=3306, charset='utf8')
# cursor = conn.cursor()

headers = {
    'Content-Type': 'text/html; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}


def get_movie_url(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    movie_hrefs = selector.xpath('//div[@class="hd"]/a/@href')
    for movie_href in movie_hrefs:
        print(movie_href)
        get_movie_info(movie_href)


def get_movie_info(url):
    html = requests.get(url, headers=headers)
    text = html.text
    # text = text.replace(' ', '').replace('\n', '')
    print(text)
    script = re.findall("(?<=<!-- dae-web-movie--).*?(?=lk9lp-->)", text)
    # result = etree.tostring(h2).decode('utf-8')
    # selector = etree.HTML(result)
    # print(text)
    # print(result)
    # print(type(selector))
    file_name = "douban.html"
    f = open(file_name, "w")
    f.write(new_text)
    f.close()
    # print("url = " + url)
    selector = etree.HTML(new_text)
    # selector = etree.parse(file_name)
    try:
        # xpath_name = '//*[@id="content"]/h1/span/text()'
        # /html/body/div[3]/div[1]/h1/span[1]
        xpath_name = u"//div"
        name_list = selector.xpath(xpath_name)
        name = name_list[0]
        director = selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0]
        actors = selector.xpath('//*[@id="info"]/span[3]/span[2]')[0]
        actor = selector.xpath('string(.)')
        style = re.findall('<span property="v:genre">(.*?)</span>', html.text, re.S)[0]
        country = re.findall('<span class="p1">制片国家/地区:</span>(.*?)<br/>', html.text, re.S)[0]
        release_time = re.findall('上映日期:</span>.*?>(.*?)</span>', html.text, re.S)[0]
        time = re.findall('片长:</span>.*?>(.*?)</span>', html.text, re.S)[0]
        score = selector.xpath('//*[@id="interest_sectl"/div[1]/div[2]/strong/text()')[0]
        # cursor.execute(
        #     "insert into doubanmovie (name,director,actor,style,country,release_time,time,socre) values(%s,%s,%s,%s,%s,%s,%s,%s)",
        #     (str(name), str(director), str(actor), str(style), str(country), str(release_time), str(time), str(score))
        # )
    except IndexError:
        pass


if __name__ == '__main__':
    urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    for url in urls:
        print(url)
        get_movie_url(url)
        time.sleep(1)
    # conn.commit()
