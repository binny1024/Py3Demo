# # -*- coding: utf-8 -*-
# # @Time : 2020/1/8 19:02
# # @Author : xubinbin
# import json
# import os
import re


#
# # video_url = "https://hongkongossofwhbalzac.oss-cn-hongkong.aliyuncs.com/WallpaperEngine/Videos/4_154884890032031.mp4"
# #
# # # 切割地址
# # # res = re.findall("(?<=/)\\d\\w*", video_url)
# # # print(res[0])
# #
# #
# # video_list = []
# # load_list = {}
# # # json文件路径
# # json_path = './json/video_bizhi.json'
# #
# # # 打开json文件
# # with open(json_path, 'r') as load_f:
# #     # 解析为 list
# #     load_list = json.load(load_f)
# #
# # print(str(load_list))
# # res = re.findall("'video_path': '(.*?)'", str(load_list))
# # print(str(res))
#
# # path = './tttttt/'
# # if not os.path.exists(path):
# #     os.mkdir(path)
# from pprint import pprint
#
#
def log(s, p, res):
    print('|=========================================')
    print('| 原始字符串: ' + s)
    print('| 模式: ' + p)
    print('|-----------')
    print('| 结果: name = ' + str(type(res)))
    print('|=========================================')


if __name__ == '__main__':
    s = '平安银行（000001）'
    p = r'.*(\(.*\))'
    r = re.search(p, s)

    log(s, p, r)
