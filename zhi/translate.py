# -*- coding: utf-8 -*-
import sys
import io

"""
Created on Sun Mar  3 12:22:49 2019

@author: Ben
"""

import importlib

importlib.reload(sys)

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# from PyPDF2.pdf import PdfFileReader, PdfFileWriter, ContentStream


import requests
import string
import time
import hashlib
import json

import fitz
##初始化

api_url = "http://api.fanyi.baidu.com/api/trans/product/index"
api_id = ""  ##申请的百度翻译接口的id
cyber = ""  ##申请的百度翻译接口的password

# pdffile = "out.pdf"  ##处理的pdf
# ENtextfile = "out.txt"  ##存储提取的txt
ENtextfile = "E运输型培养箱.txt"  ##存储提取的txt
pdffile = "运输型培养箱.pdf"  ##处理的pdf
CNtextfile = "C运输型培养箱.txt"  ##存储翻译的结果
isTranslate = False  ##是否将提取的英文翻译为中文


## 处理PDF
## 读取PDF的内容 filename是待处理的PDF的名字

###使用PDFminer读取
def getDataUsingPyPDF(filename):
    parser = PDFParser(open(pdffile, 'rb'))  # 以二进制打开文件 ,并创建一个pdf文档分析器
    doc = PDFDocument()  ##创建一个pdf文档
    # 将文档对象和连接分析器连接起来
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()

    # 使用正则表达式来查找图片
    checkXO = r"/Type(?= */XObject)"
    checkIM = r"/Subtype(?= */Image)"

    # 判断该pdf是否支持txt转换

    if doc.is_extractable:
        # 创建一个PDF设备对象
        rsrcmgr = PDFResourceManager()
        # 创建一个pdf设备对象
        laparamas = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparamas)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        contents = ""  # 保存读取的text

        # 依次读取每个page的内容

        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()  # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            # 在windows下，新文件的默认编码是gbk编码，所以我们在写入文件的时候需要设置一个编码格式，如下：
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text()
                    results = results.replace("\n", "")  # 去掉换行符 因为排版问题 有的换行导致句子中断
                    contents += (results)
        ##为了看着舒服，每一句为一行
        saveText(contents.replace(".", ".\n"), ENtextfile)
        return contents


## 将读取的content以txt格式存放到本地
def saveText(content, Textfile):
    with open(Textfile, "w", encoding='utf-8') as f:
        f.write(content)


## 翻译从pdf提取的content
def translate(content):
    salt = str(time.time())[:10]
    final_sign = str(api_id) + content + salt + cyber
    final_sign = hashlib.md5(final_sign.encode("utf-8")).hexdigest()
    # from to  代表翻译的语言
    paramas = {
        'q': content,
        'from': 'en',
        'to': 'zh',
        'appid': '%s' % api_id,
        'salt': '%s' % salt,
        'sign': '%s' % final_sign
    }
    my_url = api_url + '?appid=' + str(
        api_id) + '&q=' + content + '&from=' + 'zh' + '&to=' + 'en' + '&salt=' + salt + '&sign=' + final_sign
    response = requests.get(api_url, params=paramas).content
    content = str(response, encoding="utf-8")
    json_reads = json.loads(content)
    return json_reads['trans_result'][0]['dst'] + " "


###

content = getDataUsingPyPDF(pdffile)
print("读取pdf成功，将其保存为txt格式")

if (isTranslate):
    clist = content.split(".")  # split() 通过指定.将英文分成多个句子
    i = 0
    chinese = ""
    print("一共有" + str(clist.__len__()) + "行需要翻译")
    print("开始翻译...请耐心等待")

    while (i < clist.__len__()):
        chinese += (translate(clist[i]).replace("\n", "。"))
        # chinese += '\n'
        i += 1
        saveText(chinese, CNtextfile)
        print("翻译结束，ok")
