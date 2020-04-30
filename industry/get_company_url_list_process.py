import sys
import os

import industry

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

"""
获取上市公司的简介连接
"""
if __name__ == '__main__':
    industry.get_company_url_list_process()
