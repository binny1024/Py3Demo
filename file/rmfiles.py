import os

path = '/Users/binny/PowerDesigner/2 PowerDesigner视频教程'
# files = os.listdir(path)
# for accessory in files:
#     print(os.path.join(path, accessory))

"""
删除指定目录下下重复的文件
"""
for root, dirs, files in os.walk(path):
    for file in files:
        f = os.path.join(root, file)
        if '(1)' in f:
            print(f)
            # os.remove(f)
