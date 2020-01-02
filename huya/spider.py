import requests
import json
from bs4 import BeautifulSoup
import re


class Spider:
    def __init__(self):
        self.url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page={}'
        self.items = []

    def parse(self, url):

        response = requests.get(url)
        response.encoding = 'utf-8'
        assert response.status_code == 200  # 断言一下状态码是200
        print(response.text)
        json_dict = json.loads(response.text)  # 把响应的json数据转换成python的字典
        infos = json_dict['data']['datas']  # 每一页的直播间数据全在这里面，一共120个
        for info in infos:
            item = {}
            item['game_name'] = info['gameFullName']  # 游戏类型
            item['nick'] = info['nick']  # 昵称
            item['roomName'] = info['roomName']  # 房间的名字
            item['avatar'] = info['avatar180']  # 主播头像
            item['screenshot'] = info['screenshot']  # 封面
            item['url'] = 'https://www.huya.com/' + info['profileRoom']  # 房间号
            # print(item)
            self.items.append(item)

    # 程序入口
    def run(self):
        print("请稍后……")
        for page in range(1, 31):
            self.parse(spider.url.format(page))

        count = len(self.items)
        print("count = " + str(count))
        for i in range(0, count):
            item = self.items[i]
            url = item["url"]
            # print(url)
            response = requests.get(url)
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')  # 解析网页
            scripts = soup.find_all('script', {'data-fixed': "true"})  # 提取指定的脚本
            # print(str(scripts))

            for script in scripts:
                # print(script)
                js = script.string.replace(" ", "").replace("\n", "")  # 格式化 去空格和换行
                # print(js + "\n")
                gameStreamInfoList = re.findall(r'(?<="gameStreamInfoList":).+?(?=}],)', js)  # 正则匹配字符串

                if len(gameStreamInfoList):
                    # print("gameStreamInfoList = " + str(len(gameStreamInfoList)))
                    streamStr = gameStreamInfoList[0]
                    # print("streamStr = " + str(streamStr))
                    # print("streamStr = " + str(streamStr.split(',')))
                    stream = json.loads(streamStr)
                    for info in stream:
                        # print("sCdnType = " + str(info['sCdnType'])+"; sFlvUrl = "
                        #       +str(info['sFlvUrl'])+'/'
                        #       +str(info['sStreamName'])+'.'
                        #       +str(info['sFlvUrlSuffix'])
                        #       )
                        if str(info['sCdnType']) == 'AL' or str(info['sCdnType']) == 'al':
                            print(
                                "sCdnType = " + str(info['sCdnType']) + '\n'
                                + "直播地址 = "
                                + str(info['sHlsUrl']) + '/'
                                + str(info['sStreamName']) + '.'
                                + str(info['sHlsUrlSuffix']) + '\n'
                                + "主播的名字：" + item['nick'] + '\n'
                                + "主播头像：" + item['avatar'] + '\n'
                                + "游戏名字：" + item['game_name'] + '\n'
                                + "房间名字：" + item['roomName'] + '\n'
                                + "房间地址：" + item['url'] + '\n'
                                + "房间预览图：" + item['screenshot'] + '\n' + '\n'

                            )

                        # print("sCdnType = " + str(info['sCdnType'])+"; sP2pUrl = "
                        #       +str(info['sFlvUrl'])+'/'
                        #       +str(info['sStreamName'])+'.'
                        #       +str(info['sP2pUrlSuffix'])
                        #       )


if __name__ == '__main__':
    spider = Spider()
    spider.run()
