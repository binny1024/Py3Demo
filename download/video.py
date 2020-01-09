# -*- coding: utf-8 -*-
# @Time : 2020/1/8 19:02
# @Author : xubinbin
import json
import os
import re
import requests
from multiprocessing import Pool


def download_video(url):
    r = requests.get(url, stream=True)
    # 使用正则取出文件名
    res = re.findall("(?<=/)\\d\\w*", url)[0]
    path = '/Users/binny/Movies/wall_video/' + res + '.mp4'
    if os.path.exists(path):
        print('文件已存在....')
    else:
        with open(str(path), "wb") as mp4:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    mp4.write(chunk)


if __name__ == "__main__":
    # 指定json文件所在路径
    json_path = '../json/video_bizhi.json'

    # 打开json文件
    with open(json_path, 'r') as load_f:
        # 解析为 list
        load_list = json.load(load_f)

    # 使用正则取出 所有的url
    video_list = re.findall("(?<='video_path': ').*?(?=',)", str(load_list))
    print("视频个数: "+ str(len(video_list)))
    path = '/Users/binny/Movies/wall_video/'
    if not os.path.exists(path):
        os.mkdir(path)
        print('文件夹: ' + path + '   已创建')
    else:
        print('文件夹: ' + path + '   已存在')
    pool = Pool(processes=10)
    pool.map(download_video, video_list)
