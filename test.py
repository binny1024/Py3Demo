# # -*- coding: utf-8 -*-
# # @Time : 2020/1/8 19:02
# # @Author : xubinbin
# import json
# import os
# import re
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
# def log(s, p, res):
#     print('|=========================================')
#     print('| 原始字符串: ' + s)
#     print('| 模式: ' + p)
#     print('|-----------')
#     print('| 结果: name = ' + str(type(res)))
#     print('|=========================================')
#
#
# if __name__ == '__main__':
#     s = 'my name is binny'
#     p = '(?<=my name is ).*(?=y)'
#     name = re.findall(p, s)
#     log(s, p, name)
#     p = '(?:my name is ).*(?:y)'
#     name = re.findall(p, s)
#     log(s, p, name)
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox

path = "test.pdf"

# 用文件对象来创建一个pdf文档分析器
praser = PDFParser(open(path, 'w+'))
# 创建一个PDF文档
doc = PDFDocument(praser)
# 连接分析器 与文档对象
praser.set_document(doc)
doc.set_parser(praser)

# 提供初始化密码
# 如果没有密码 就创建一个空的字符串
doc.initialize()

# 检测文档是否提供txt转换，不提供就忽略
if not doc.is_extractable:
    raise PDFTextExtractionNotAllowed
else:
    # 创建PDf 资源管理器 来管理共享资源
    rsrcmgr = PDFResourceManager()
    # 创建一个PDF设备对象
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解释器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # 循环遍历列表，每次处理一个page的内容
    for page in doc.get_pages():
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout = device.get_result()
        # 这里layout是一个LTPage对象，里面存放着这个 page 解析出的各种对象
        # 包括 LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等
        for x in layout:
            if isinstance(x, LTTextBox):
                print(x.get_text().strip())
