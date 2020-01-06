from bs4 import BeautifulSoup
import requests
import random
import time

from requests import HTTPError


def download_page(url):
    print(url)
    try:
        # User Agent中文名为用户代理，简称 UA，它是一个特殊字符串头，使得服务器能够识别客户使用的操作系统及版本、CPU 类型、浏览器及版本、
        # 浏览器渲染引擎、浏览器语言、浏览器插件等。
        header = {
            "User-Agent": "Mozilla/5.0 (windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36"
        }
        data = requests.get(url, headers=header).text
        # print(data)
    except HTTPError as err:
        print(err.__traceback__)
    except ConnectionError as err:
        print(err.__traceback__)
    except TimeoutError as err:
        print(err.__traceback__)
    return data


# 获取当前首页的内容
def parse_proxy_html(html):
    f = open("proxy.txt", "w")
    try:
        # 解析器html.parser lxml xml html5lib
        soup = BeautifulSoup(html, 'lxml')
        list_tr = soup.find_all('tr')
        print("list_tr.size = " + str(len(list_tr)))
        count = 0
        for tr in list_tr:
            list_td = tr.find_all('td')
            count = count + 1
            if len(list_td) == 0:
                continue
            ip_temp = list_td[1].contents[0] + ":" + list_td[2].contents[0]
            print(str(count) + " " + ip_temp)
            f.write(ip_temp + "\n")
        return ""
    except Exception as ex:
        print('抓取信息异常:' + ex)


# 首页数据抓取
HTTP = 'https://www.xicidaili.com'


def to_proxy_page():
    download_url = '/wt/1'
    num = 1
    # 获取页面信息
    html = download_page(HTTP + download_url)
    # 解析和保存
    download_url = parse_proxy_html(html)

    # while download_url != 'JAVAscript:;' and download_url != '':
    #     if num == 3:
    #         print('~~~~够用了~~不抓取了~~~')
    #         break
    #     print("第%d次请求地址:%s" % (num, download_url));
    #     # 随机停顿几秒
    #     i = random.randint(1, 3)
    #     time.sleep(i)
    #     # 获取页面信息
    #     html = download_page(HTTP + download_url)
    #     # 解析和保存
    #     download_url = parse_proxy_html(html)
    #     num = num + 1


if __name__ == '__main__':
    to_proxy_page()
