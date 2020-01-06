import lxml.html
import requests
import csv

etree = lxml.html.etree

fp = open('C://Users/97967/Desktop/doubanbook.csv','wt',newline='',encoding='utf-8')
writer = csv.writer(fp)
writer.writerow(('name','url','author','pulisher','data','price',
'rate','comment'))

urls = ['https://book.douban.com/top250?start={}'.format(str(i)) for
        i in range(0,250,25)]

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.3'
}

for url in urls:
    html = requests.get(url,headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//tr[@class="item"]')
    for info in infos:
        name = info.xpath('td/div/a/@title')[0]
        url = info.xpath('td/div/a/@href')[0]
        book_infos = info.xpath('td/p/text()')[0]
        author = book_infos.split('/')[0]
        publisher = book_infos.split('/')[-3]
        date = book_infos.split('/')[-2]
        price = book_infos.split('/')[-1]
        rate = info.xpath('td/div/span[2]/text()')[0]
        comments = info.xpath('td/p/span/text()')
        comment = comments[0] if len(comments) !=0 else "空"
        writer.writerow((name,url,author,publisher,date,price,rate,comment))

fp.close()

//*[@id="content"]/div/div[1]/div/table[1]/tbody/tr/td[2]/div[1]
//*[@id="content"]/div/div[1]/div/table[1]/tbody/tr/td[2]/div[1]/a
/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/h4/a
/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/h4/a
/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[1]
/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[1]/a[1]
/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[1]/a[2]
/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[1]/a[3]
/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[1]/span
/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[2]/text()
/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[3]/span/text()