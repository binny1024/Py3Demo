import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from industry.industry import get_company_url_list_process
"""
获取上市公司的简介连接
"""
if __name__ == '__main__':
    get_company_url_list_process()
