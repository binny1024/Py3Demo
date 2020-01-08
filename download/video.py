# -*- coding: utf-8 -*-
# @Time : 2020/1/8 19:02
# @Author : xubinbin
import json
import os

import requests

video_list = []
load_dict = []
with open("../json/video_bizhi.json", 'r') as load_f:
    load_dict = json.load(load_f)

for video_url in load_dict:
    print(video_url['video_path'])
    name = video_url['video_path'].split('/')[-1:]
    print(name)
    print(str(name)[2:len(str(name)) - 2])
    print(str(video_url['video_path'].split('/')[-1:]).split('.')[0])
    video_list.append(video_url['video_path'])

for url in video_list:
    r = requests.get(url, stream=True)
    name_video_list = url.split('/')[-1:]
    name = str(name_video_list)[2:len(str(name_video_list)) - 2]
    print('下载----' + name)
    path = '/Users/binny/Movies/wall_video/'+ str(name)
    if os.path.exists(path):
        print('文件已存在....')
        continue
    with open(str(path), "wb") as mp4:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                mp4.write(chunk)
        # mp4.close()
print("下载结束")
