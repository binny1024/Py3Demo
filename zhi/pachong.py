import requests

from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
res = requests.get('http://bj.xiaozhu.com', headers=headers)
# text = res.text
# print(text)
soup = BeautifulSoup(res.text, 'html.parser')
prices = soup.select(
    '#page_list > ul > li > div.result_btm_con.lodgeunitname > div > span.result_price > i')

for price in prices:
    print(price.text)
