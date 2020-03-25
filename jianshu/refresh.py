import random
import socket
from time import sleep

import requests
from jianshu.proxy import download_page
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pool

# 定义User-Agent集合
agent_list = [
    # Win7:
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    # Win7:
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    # Win7:
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    # Win7:
    'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    # Win7+ie9：
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
    # Win7+ie8：
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
    # WinXP+ie8：
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
    # WinXP+ie7：
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    # WinXP+ie6：
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    # 傲游3.1.7在Win7+ie9,高速模式:
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
    # 傲游3.1.7在Win7+ie9,IE内核兼容模式:
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
    # 搜狗3.0在Win7+ie9,IE内核兼容模式:
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
    # 搜狗3.0在Win7+ie9,高速模式:
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
    # 360浏览器3.0在Win7+ie9:
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
    # QQ浏览器6.9(11079)在Win7+ie9,极速模式:
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
    # QQ浏览器6.9(11079)在Win7+ie9,IE内核兼容模式:
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
    # 阿云浏览器1.3.0.1724 Beta(编译日期2011-12-05)在Win7+ie9:
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
]


def to_refresh_page(urls):
    # browser = webdriver.Chrome("../driver/chromedriver_80")
    b = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    # chrome_options.add_argument('--headless')  # 增加无界面选项
    # chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
    # browser = webdriver.Chrome(options=chrome_options)
    # for i in range(100):
    for u in urls:
        # browser.get(url)
        # for url in url_list:
        for j in range(1000):
            # chromeOptions.add_argument("--proxy-server=http://" + random.choice(proxys))
            # browser = webdriver.Chrome(options=chromeOptions)
            print("j = " + str(j) + "  " + u)
            b.get(u)
            # browser.refresh()
    # browser.quit()
    b.close()


# def get_page_jianshu():
#     # html = download_page("https://www.jianshu.com/u/b8d32d868a2b")
#     html = download_page("https://www.jianshu.com/u/5f41e5b2d14c")
#     # print(html)
#     soup = BeautifulSoup(html, 'lxml')
#     list_a = soup.find_all('a', attrs={"class": "title"})
#     print("list_h2 = " + str(len(list_a)))
#     ls = []
#     for a in list_a:
#         url = "https://www.jianshu.com" + (a['href'])
#         # print(url)
#         ls.append(url)
#     return ls
#

if __name__ == '__main__':
    # to_refresh_page(get_page_url_blockchainbrother())
    # to_refresh_page(get_page_jianshu())
    browser = webdriver.Chrome()
    browser.get("https://www.jianshu.com/u/5f41e5b2d14c")
    sleep(5)
    # # 简书需要上拉才能获取更多文章
    # for i in range(10):
    #     browser.execute_script("window.scrollBy(0, 500);")  # execute_script是插入js代码的
    #     sleep(2)  # 加载需要时间，2秒比较合理
    while True:
        try:
            if browser.find_element_by_link_text('傅里叶变换、拉普拉斯变换和Z变换的简便算法'):
                break
        except Exception as e:
            browser.execute_script("window.scrollBy(0, 500);")  # execute_script是插入js代码的
            sleep(2)  # 加载需要时间，2秒比较合理

    titles = browser.find_elements_by_class_name("title")
    url_list = []
    for title in titles:
        url = title.get_attribute("href")
        if url is not None:
            url_list.append(str(url))
            print(url)
    browser.quit()
    # url_list.reverse()
    print(str(len(url_list)))
    # pool = Pool(processes=10)
    # pool.map_async(to_refresh_page, url_list)
    to_refresh_page(url_list)

    # print(f"browser text = {browser.page_source}")
