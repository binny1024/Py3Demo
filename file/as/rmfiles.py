import os
import shutil


def rm_as_project_build():
    path = '/Users/binny/AndroidStudioProjects'
    # files = os.listdir(path)
    # for accessory in files:
    #     print(os.path.join(path, accessory))

    """
    删除指定目录下下重复的文件
    """
    for root, dirs, files in os.walk(path):
        # for file in files:
        #     f = os.path.join(root, file)
        #     print(f)
        #     # os.remove(f)

        # 删除 build 文件
        # for d in dirs:
        #     if d.startswith('.gradle') or d.startswith('build'):
        #         d = os.path.join(root, d)
        #         print(d)
        #         shutil.rmtree(d)

        #     删除 zip 文件
        for d in files:
            # print(d)
            if d.endswith('.jar'):
                d = os.path.join(root, d)
                print(d)
                # shutil.rmtree(d)
                os.remove(d)


if __name__ == '__main__':
    rm_as_project_build()
