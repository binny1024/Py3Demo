# -*- coding:utf-8 -*-
import json
import os
import re
import time

import itchat
import matplotlib.pyplot as plt
import pygame
from PIL import ImageFont, Image
from wordcloud import WordCloud

# noinspection PyGlobalUndefined
global account

global imgPath


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("--文件夹已创建---")
    else:
        print("---文件夹已存在!---")


# 获取头像
def get_head_image():
    mkImgFile()  # 获取头像
    print("正在获取头像……………………")
    friends = itchat.get_friends(update=True)
    # itchat.get_head_img() 获取到头像二进制，并写入文件，保存每张头像
    print("您的好友总数为：" + str(len(friends)))

    for count, f in enumerate(friends):
        folder = os.path.exists(imgPath + "/" + str(count) + ".png")

        if folder:
            print("文件存在 " + str(count))
            continue
        print("正在创建第" + str(count) + "头像")
        # 根据userName获取头像
        img = itchat.get_head_img(userName=f["UserName"])
        imgFile = open(imgPath + "/" + str(count) + ".png", "wb")
        imgFile.write(img)
        imgFile.close()
        print("文件创建完成！")


def sortFile(l):
    print('Before:')
    print(l)
    for i in range(len(l)):
        l[i] = l[i].split('.')
        l[i][0] = int(l[i][0])
    print('After:')

    print(l)
    l.sort()
    print('Sorted:')

    print(l)

    for i in range(len(l)):
        l[i][0] = str(l[i][0])
        l[i] = l[i][0] + '.' + l[i][1]
    print('Recover:')
    print(l)
    return l


# 创建头像拼图的文件夹
def mkImgFile():
    global imgPath
    imgPath = "img/" + account
    mkdir(imgPath)
    print("头像拼图的文件夹 ：" + imgPath)


# 头像拼接图
def createImg(dotPx, img_name):
    """
    :param img_name: 要保存的文件名
    :param dotPx:  每张小图片的像素点数，越大越清晰
    :return: 无

    根据输入的像素值，和计算出来的 图片总数,来获取大图分辨率
    """
    mkImgFile()  # 获取头像
    x = 0
    y = 0
    imgs = os.listdir(imgPath)
    # random.shuffle(imgs)
    # imgs = sortFile(imgs)
    count = len(imgs)
    print("图片总数 = " + str(count))  # 1000

    # 每张图片的像素数
    # 每行图片数
    numLine = int(pygame.math.sqrt(count)) + 1
    print("每行图片数 = " + str(numLine))
    # # 图片宽度
    # widthTotalLengthPx = numLine * dotPx
    # # 列数
    # numColumn = int(count / numLine) + 1
    # # 图片的高度
    # heightTotalLengthPx = dotPx * numColumn
    #
    # # 最终的宽高
    # size = math.sqrt(math.pow(widthTotalLengthPx, 2) + math.pow(heightTotalLengthPx, 2))
    width = dotPx
    print("小图片宽度 = " + str(width))
    resolutionX = numLine * dotPx
    # Image.new('颜色模式', (宽, 高),(背景色))
    # newImg = Image.new('RGBA', (resolution, resolution), (0, 255, 0))
    newImg = Image.new('RGBA', (resolutionX, resolutionX))
    print("大图分辨率 = " + str(resolutionX) + "*" + str(resolutionX))
    mkImgFile()  # 头像拼接图
    for count, i in enumerate(imgs):
        path = imgPath + "/" + i
        try:
            if os.path.getsize(path) == 0:  # 获取文件大小
                os.remove(path)
                continue
            img = Image.open(path)
            # 缩小图片
            img = img.resize((width, width), Image.ANTIALIAS)
            # 拼接图片，一行排满，换行拼接
            newImg.paste(img, (x * width, y * width))
            print(path + "  " + str(count))
            x += 1
            if x >= numLine:
                x = 0
                y += 1
        except IOError as e:
            print(repr(e))
            # continue
    folder = os.path.exists(imgPath + "_all")

    if not folder:
        mkdir(imgPath + "_all")
    newImg.save(imgPath + "_all" + "/" + img_name + ".png")
    print("img保存完成！文件名为---" + img_name)


# 性别统计
def getSex():
    friends = itchat.get_friends(update=True)
    sex = dict()
    for f in friends:
        if f["Sex"] == 1:  # 男
            sex["man"] = sex.get("man", 0) + 1
        elif f["Sex"] == 2:  # 女
            sex["women"] = sex.get("women", 0) + 1
        else:  # 未知
            sex["unknown"] = sex.get("unknown", 0) + 1
    # 柱状图展示
    for i, key in enumerate(sex):
        plt.bar(key, sex[key])
    plt.savefig("getsex.png")  # 保存图片
    plt.ion()
    plt.pause(5)
    plt.close()  # 图片显示5s，之后关闭
    # plt.show() #不建议用show，show是堵塞式


# 获取个性签名
def getSignature():
    friends = itchat.get_friends(update=True)
    print(friends)
    file = open('name_sign.txt', 'a', encoding='utf-8')
    text = ""
    for count, f in enumerate(friends):
        rec = re.compile("1f\d+\w*|[<>/=]")

        signature = f["Signature"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        signature = rec.sub("", signature)

        # remarks = f["RemarkName"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        # remarks = rec.sub("", remarks)

        nickname = f["NickName"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        nickname = rec.sub("", nickname)

        print("昵称：" + nickname)
        # print("备注：" + remarks)
        print("签名：" + signature)
        print("---------------------")
        strs = str(count) + " \n昵称：" + nickname + "\n" + "签名：" + signature + "\n"
        if not signature.strip():
            text = text + "签名：" + signature + "\n"
        file.write(strs + "\n")
    saveTxtToPNG(text)


# 保存本本信息
def saveText(file_name, text_save):
    print("保存联系人信息……")
    mkdir(file_name)
    file = open(file_name + "/" + account, 'a', encoding='utf-8')
    file.write(text_save + "\n")
    print("保存联系人信息……Done!")


# 生成词云图
def create_word_cloud(filename):
    # 读取文件内容
    text = open("{}.txt".format(filename), encoding='utf-8').read()

    # 注释部分采用结巴分词
    # wordlist = jieba.cut(text, cut_all=True)
    # wl = " ".join(wordlist)

    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置最大显示的词云数
        max_words=2000,
        # 这种字体都在电脑字体中，window在C:\Windows\Fonts\下，mac下可选/System/Library/Fonts/PingFang.ttc 字体
        font_path='C:\\Windows\\Fonts\\simfang.ttf',
        height=500,
        width=500,
        # 设置字体最大值
        max_font_size=60,
        # 设置有多少种随机生成状态，即有多少种配色方案
        random_state=30,
    )

    myword = wc.generate(text)  # 生成词云 如果用结巴分词的话，使用wl 取代 text， 生成词云图
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file('signature.png')  # 把词云保存下


def removeIpg():
    jpg = os.listdir("img")
    jpg.sort()
    for img in jpg:
        if img.endswith('.jpg'):
            print(img)
            os.remove("img/" + img)  # 要加完整路径


def saveTxtToPNG(text):
    print("将文本保存为图片")
    pygame.init()

    im = Image.new("RGB", (2000, 45000), (255, 255, 255))
    from PIL import ImageDraw
    dr = ImageDraw.Draw(im)
    font_size = 30
    font = ImageFont.truetype(os.path.join("fonts", "minishaoer.ttc"), font_size)

    dr.text((50, 5), text, font=font, fill="#000000")

    im.show()
    im.save("t.png")
    print("保存为图片--Done")


def getFriendsList():
    print("获取成员列……")
    fds = itchat.get_friends(update=True)
    fds = format_output(fds)  # 获取成员列表
    saveText(file_name="account", text_save=fds)
    print(fds)
    # fs = []
    # for count, f in enumerate(fds):
    #     nickname = f["NickName"].strip().replace("emoji", "").replace("span", "").replace("class", "")
    #     print(nickname)
    #     fs.append(nickname)
    # return fs


def sendGroupAssistant():
    exclude_name = """
    '妈'，
    '妈妈',
    '爸',
    '爸爸'
    """
    SINCERE_WISH = """
    值此2019年大年初一,
    许彬彬祝您和您家人在新的一年里：
    一帆风顺🌺，二龙起飞🌹，三羊开泰💐，四季平安🌷，五福临门🌺，六六大顺🎄，七星高照☘，八方来财🍀，九九同心✨，十全十美💫。
    
    您以为这是群发的？不,不,不……不信您看啊：
    您的昵称：%s 您的签名：%s 
    祝 %s 身体安康🍎，诸事如意🍌、阖家幸福🍊，年年有鱼🌽，顺缘增长🥕，六时吉祥！
    """
    friendList = itchat.get_friends(update=True)[0:]  # 排除登录者本人的微信
    print("开始群发消息")
    print("您总共有 " + str(len(friendList)) + " 个好友")

    for count, friend in enumerate(friendList):
        msg = SINCERE_WISH % (friend['NickName'] or '好吧，空？大神，您是怎么做到的😒',  friend['Signature'] or '好吧，您未设置个性签名,不设置一下吗？',friend['RemarkName'] or friend['NickName'] )
        # if count > 0:  # 只发给一个人
        #     return
        itchat.send(msg, toUserName=friend['UserName']) # 发送消息
        print(str(count) + " " + msg)
        # print("\n昵称："+friend['NickName']+"\n备注："+friend['RemarkName']+"\n签名："+friend['Signature'])
        # time.sleep(1)

    print("群发完成")


def login():
    print("扫码登陆……")
    itchat.auto_login(hotReload=True)
    print("登陆成功……获取微信联系人信息")
    getAccount()


def loginWithAutoReply():
    print("带自动回复的登录……")
    itchat.auto_login(hotReload=True)
    getAccount()
    itchat.run()


def getAccount():
    print("获取微信账号……")
    friends = itchat.get_friends(update=True)
    print("打印联系人信息……")
    print("登录账号为 ：" + friends[0]["PYQuanPin"])
    global account
    account = friends[0]["PYQuanPin"]


@itchat.msg_register(itchat.content.TEXT)  # msg.text 就是回复的文本信息内容
def text_reply(msg):
    format_output(msg)  # 文本信息回复
    return '微信自动回复 ：' + msg.text


@itchat.msg_register(itchat.content.PICTURE)
def pic_reply(msg):
    print(msg)


def format_output(json_str):
    print("格式化输出 json :")
    json_str = json.dumps(json_str, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    # print(json_str)
    return json_str


if __name__ == "__main__":
    login()
    # loginWithAutoReply()
    # getAccount()
    # print(itchat.search_friends())  # 获取自己的用户信息，返回自己的属性字典
    # print(itchat.search_friends(wechatAccount='qq18667155877'))  # 获取特定UserName的用户信息

    # itchat.send('Hello, filehelper', toUserName='filehelper')# 发送信息给文件助手

    # get_head_image()
    # createImg(dotPx=640, img_name=account)  # 合成图片
    # removeIpg()
    # getSignature()

    # getFriendsList()

    sendGroupAssistant()  # 群发微信消息
