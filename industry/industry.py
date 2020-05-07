import traceback
import sys
import os

from selenium.common.exceptions import TimeoutException

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from dbmysql.MySqlConn import MyPymysqlPool
from utils.selenium_uitls import SeleniumUtil
from multiprocessing import Process

"""
采集上市公司的信息
股票代码、股票名称、公司全称、上市时间（遗漏，需要补充）
"""


class IndustryHelper:
    def __init__(self, category_id, org_code, stock_type, category_url, done=False, com_url_list=None):
        """
        对应 表 industry_com_url
        :param category_id: 类别id,对应 industry_category 表中的 id
        :param org_code: 类别代码,对应 industry_category 表中的 org_code
        :param stock_type: 股票代码,对应 industry_category 表中的 stock_type
        :param category_url: 类别 url,对应 industry_category 表中的 category_url
        :param done: 是否已完成
        :param com_url_list: 公司地址列表
        """
        self.category_id = category_id
        self.org_code = org_code
        self.stock_type = stock_type
        self.category_url = category_url
        self.done = done
        self.com_url_list = com_url_list


global selenium_util
global mysql


def init_industry_mysql():
    """
    初始化 mysql 对象
    :return:
    """
    global mysql
    mysql = MyPymysqlPool("../dbmysql/industry_mysql.ini", 'mysql_config')


def init_selenium_util():
    """
    初始化 selenium_util
    :return:
    """
    global selenium_util
    selenium_util = SeleniumUtil(True)
    # selenium_util.set_waiting_time(10)
    selenium_util.set_window_size(1920, 1080)


def company_detail(url):
    """
    解析公司简介页面
    :param url: 公司简介页面地址
    :return: field_name_in_industry_company_profile_map
    """
    keys_map = {
        '公司名称：': 'name_cn',
        '英文名称：': 'name_en',
        '曾 用 名：': 'name_old',
        '所属地域：': 'area',
        '所属行业：': 'catg_desc',
        '公司网址：': 'com_url',
        '主营业务：': 'main_business',
        '产品名称：': 'product_name',
        '控股股东：': 'controller_stock',
        '实际控制人：': 'controller_actual',
        '最终控制人：': 'controller_ultimate',
        '董 事 长：': 'president',
        '董　　秘：': 'president_secretary',
        '法人代表：': 'representative_legal',
        '总 经 理：': 'general_manager',
        '注册资金：': 'registered_capital',
        '员工人数：': 'employees_number',
        '电　　话：': 'telephone',
        '传　　真：': 'fax',
        '邮　　编：': 'postcode',
        '办公地址：': 'company_address',
        '公司简介：': 'company_profile',
        '董事会主席：': 'president_chairman',
        '证券事务代表：': 'representative_securities_affairs',
        '年结日：': 'balance_sheet_date',
        '注册地址：': 'registered_address',
        '公司总部：': 'corporate_headquarters',
        '电邮：': 'e_mail',
        '核数师：': 'auditor',
        '法律顾问：': 'legal_adviser',
        'stock_type': '',
        'org_code': "",
        '电话：': 'telephone',
        '传真：': 'fax',
        '网址：': 'com_url',
    }
    field_name_in_industry_company_profile_map = {
        'name_cn': '',
        'name_en': '',
        'name_old': '',
        'area': '',
        'catg_desc': '',
        'com_url': '',
        'main_business': '',
        'product_name': '',
        'controller_stock': '',
        'controller_actual': '',
        'controller_ultimate': '',
        'president': '',
        'president_secretary': '',
        'representative_legal': '',
        'general_manager': '',
        'registered_capital': '',
        'employees_number': '',
        'telephone': '',
        'fax': '',
        'postcode': '',
        'company_address': '',
        'company_profile': '',
        'president_chairman': '',
        'representative_securities_affairs': '',
        'balance_sheet_date': '',
        'registered_address': '',
        'corporate_headquarters': '',
        'auditor': '',
        'legal_adviser': '',
        'stock_name': '',
        'stock_code': '',
        'e_mail': '',
    }
    selenium_util.get(url)
    # /html/body/div[2]/div[3]/div[1]/h1
    # xpath_stock_name_with_code = '/html/body/div[2]/div[3]/div[1]/h1'
    # results = selenium_util.find_one_element_by_xpath(xpath_stock_name_with_code)
    # stock_name_with_code_text = results.text
    # p = r'\d+'
    # ss = re.search(p, stock_name_with_code_text)
    # stock_code = ss.group()
    # print("股票代码:" + stock_code)
    # p = "[^（" + stock_code + "）]+"
    # ss = re.search(p, stock_name_with_code_text)
    # stock_name = ss.group()
    # print("股票名字:" + stock_name)
    xpath_tbody_trs = '/html/body/div[2]/div[3]/div[2]/div[2]/table/tbody/tr'
    tr_list = selenium_util.find_all_elements_by_xpath(xpath_tbody_trs)
    # print("tr 的个数" + str(len(tr_list)))

    # 遍历简介item
    for tr in tr_list:
        # /html/body/div[2]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[2]
        # 公司名称：	平安银行股份有限公司
        td_key = selenium_util.find_one_child_element_by_xpath(tr, './/td[1]')
        td_value = selenium_util.find_one_child_element_by_xpath(tr, './/td[2]')

        td_key_text = td_key.text
        if td_key_text in keys_map.keys():
            # print(td_key.text)
            td_value_text = td_value.text
            if td_key_text == '所属行业：':
                """
                1，当 键值对为   所属行业：	银行-银行 时，需要特殊处理，里面含有两个链接
                
                2，一个特殊的地址：https://s.askci.com/stock/summary/HK8613/ 
                
                """
                tds = selenium_util.find_all_child_elements_by_tag(td_value, 'a')
                td_value_text = ""
                for td in tds:
                    td_value_text = td_value_text + td.text
                print(url + " " + td_key_text + td_value_text)
                if keys_map[td_key_text] in field_name_in_industry_company_profile_map:
                    field_name_in_industry_company_profile_map[keys_map[td_key_text]] = td_value_text
                    # print(td_key_text + td_value_text)
                continue
            if keys_map[td_key_text] in field_name_in_industry_company_profile_map:
                field_name_in_industry_company_profile_map[keys_map[td_key_text]] = td_value_text
                # print(td_key_text + td_value_text)

    # field_name_in_industry_company_profile_map['stock_code'] = stock_code
    # field_name_in_industry_company_profile_map['stock_name'] = stock_name

    for key in field_name_in_industry_company_profile_map.keys():
        if field_name_in_industry_company_profile_map[key] == '':
            continue
        # print(key + ':' + field_name_in_industry_company_profile_map[key])
    return field_name_in_industry_company_profile_map


def update_industry_catg_url():
    """
    从 industry_catg表中获取碎片信息,拼接出上市公司的列表页面的完整地址,并回更新到数据库
    :return:
    """
    url_base = 'https://s.askci.com/stock/'

    sql_all_item = 'select id,stock_type,org_code from industry_category;'
    result = mysql.getAll(sql_all_item)
    industry_company_helper_objs = []
    for res in result:
        # print(res)
        whole_url = url_base + res['stocktype'] + '-' + res['orgcode'] + '-0/1/'
        industry_company_helper = IndustryHelper(res['id'], res['orgcode'], res['stocktype'], whole_url)
        # print(whole_url)
        industry_company_helper_objs.append(industry_company_helper)

    sql = 'UPDATE industry_category SET category_url=%s where org_code=%s'

    for helper_obj in industry_company_helper_objs:
        # print(company_url)
        # parse_company_list_page(company_url)
        id_ = mysql.update(sql, (helper_obj.category_url,
                                 helper_obj.org_code))
        print(id_)


def parse_company_list_page_auto_next(url):
    """
    解析上市公司列表页,自动点击下一页
    查看是否有数据
    :param url:
    :return: company_profile_url_list or []  公司的 简介列表
    """
    selenium_util.get(url)
    tr_list = selenium_util.find_all_elements_by_xpath('//*[@id="ResultUl"]/tr')
    if (len(tr_list) == 1) and (tr_list[0].text == '暂无数据'):
        # print("此页没有公司列表 " + url)
        return []
    xpath_total_page_num = '//*[@id="kkpager"]/div[1]/span[2]/span/span[3]'
    total_page_num = selenium_util.find_one_element_by_xpath(xpath_total_page_num).text
    xpath_current_page_num = '//*[@id="kkpager"]/div[1]/span[2]/span/span[1]'
    # print('正在解析')
    company_profile_url_list = parse_current_company_profile_url_list(tr_list)
    if total_page_num == "1":
        # 如果只有一页,解析完直接返回解析结果
        return company_profile_url_list
    next_page = selenium_util.find_one_element_by_link_text('下一页')

    clickable = next_page.is_enabled()
    # print('解析下一页')

    while clickable:
        # print('clickable = ' + str(clickable))
        next_page.click()
        results = selenium_util.find_all_elements_by_xpath('//*[@id="ResultUl"]/tr')
        company_profile_url_list = company_profile_url_list + parse_current_company_profile_url_list(results)
        selenium_util.scroll_window_to_down()
        current_page_num = selenium_util.find_one_element_by_xpath(xpath_current_page_num).text
        # print('current_page_num = ' + current_page_num + ' total_page_num = ' + total_page_num)
        if current_page_num == total_page_num:
            # print('没有下一页了')
            break
        next_page = selenium_util.find_one_element_by_link_text('下一页')
        if next_page is None:
            break
        clickable = next_page.is_enabled()

    # for href in catg_list:
    #     print(href)

    # company_detail(href, companies)
    return company_profile_url_list


def parse_company_list_page_single(url):
    """
    解析上市公司列表页,一页一页的解析
    查看是否有数据
    :param url:
    :return: company_profile_url_list or []  公司的 简介列表
    """
    selenium_util.get(url)
    tr_list = selenium_util.find_all_elements_by_xpath('//*[@id="ResultUl"]/tr')
    company_profile_url_list = parse_current_company_profile_url_list(tr_list)
    return company_profile_url_list


def parse_current_company_profile_url_list(tr_list):
    # 遍历上市公司列表
    a_href_list = []
    for tr in tr_list:
        # print(tr.text)
        # /html/body/div[3]/div[2]/div[1]/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/a
        # 获取子元素
        a = selenium_util.find_one_child_element_by_xpath(tr, './/td[2]/a')
        # 获取跳转链接
        company_detail_url = a.get_attribute('href')
        # print(company_detail_url)
        a_href_list.append(company_detail_url)
    return a_href_list


def parse_company_item_list(url, tr_list):
    # 遍历上市公司列表
    company_item_list = []
    for tr in tr_list:
        try:
            item = {}
            # print(tr.text)
            # /html/body/div[3]/div[2]/div[1]/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/a
            # 获取子元素 //*[@id="ResultUl"]/tr[7]/td[5]
            td_stock_code = selenium_util.find_one_child_element_by_xpath(tr, './/td[2]')
            # 获取 stock_code
            stock_code = td_stock_code.text
            item['stock_code'] = stock_code

            # 获取 company_url
            a = selenium_util.find_one_child_element_by_xpath(tr, './/td[2]/a')
            company_url = a.get_attribute('href')
            item['company_url'] = company_url

            # 获取 stock_name
            td_stock_name = selenium_util.find_one_child_element_by_xpath(tr, './/td[3]')
            stock_name = td_stock_name.text
            item['stock_name'] = stock_name

            # 获取 company_name
            td_company_name = selenium_util.find_one_child_element_by_xpath(tr, './/td[4]')
            company_name = td_company_name.text
            item['company_name'] = company_name

            # 获取 datetime
            td_datetime = selenium_util.find_one_child_element_by_xpath(tr, './/td[5]')
            datetime = td_datetime.text
            item['datetime'] = datetime

            td_company_type = selenium_util.find_one_child_element_by_xpath(tr, './/td[8]')
            # 获取 行业分类
            company_type = td_company_type.text
            item['company_type'] = company_type

            td_main_bussiness = selenium_util.find_one_child_element_by_xpath(tr, './/td[9]')
            # 获取 主营业务
            main_bussiness = td_main_bussiness.text
            item['main_business'] = main_bussiness
            company_item_list.append(item)
        except TimeoutException or Exception as e:
            sql = 'INSERT INTO collect_url_error (url) VALUES(%s)'
            id_ = mysql.insert(sql, url)
            print('error：' + url)
            return None
    return company_item_list


def get_industry_helper_objs(sql):
    """
    读取 industry.industry_category_in_table 表中,  items_count IS NULL 的所有记录
    保存到 industry_helper_obj_list 列表中
    :return: industry_helper_obj_list
    """
    industry_category_list = mysql.getAll(sql)
    industry_helper_obj_list = []
    for industry_category_in_table in industry_category_list:
        industry_helper_obj_list.append(IndustryHelper(
            industry_category_in_table['id'],
            industry_category_in_table['org_code'],
            industry_category_in_table['stock_type'],
            industry_category_in_table['category_url']
        ))

    print("从 行业类别数据库中取出 类别地址个数 " + str(len(industry_helper_obj_list)) + "\n")
    return industry_helper_obj_list


def worker_insert_com_url(index1, index2):
    init_industry_mysql()
    init_selenium_util()
    """
    从 industry_category 表中查询出每一个类别 的 url
    :param index1: id 的起始位置,包括
    :param index2: id 的终止位置,包括
    :return:
    """
    sql = "select id,category_url, org_code, stock_type from industry_category where id BETWEEN " + str(
        index1) + " and " + str(index2) + ";"
    # print(sql)
    industry_helper_objs = get_industry_helper_objs(sql)
    for industry_catg_obj in industry_helper_objs:
        # print(str(industry_catg_obj.catg_id) + '\n')
        company_profile_url_list = parse_company_list_page_auto_next(industry_catg_obj.category_url)
        #
        # # 更新 行业列表表中 类别表中的 item_count
        # # sql = 'UPDATE industry_category SET company_counts=%s where org_code=%s'
        # # id_ = mysql.update(sql, (len(company_profile_url_list), industry_catg_obj.org_code))
        # # print(id_)
        #
        # # 更新 公司简介链接表
        sql2 = "INSERT INTO industry_category_whole_companies_info" \
               " (com_url, category_id, org_code, stock_type) " \
               "VALUES (%s, %s,%s, %s)"
        for company_profile_url in company_profile_url_list:
            print(company_profile_url)
            # company_detail(company_profile_url, industry_catg_obj)
            id_ = mysql.update(sql2, (company_profile_url,
                                      industry_catg_obj.category_id,
                                      industry_catg_obj.org_code,
                                      industry_catg_obj.stock_type))
            print(id_)
    # print("done")
    selenium_util.quit()


def process_get_categories_contains_all_com_url():
    """
    获取所有类别下的所有公司的简介地址,保存到数据库中
    :return:
    """
    p1 = Process(target=worker_insert_com_url, name='p1', args=(398, 600,))  # 必须加,号
    p1.start()
    p2 = Process(target=worker_insert_com_url, name='p2', args=(601, 800,))
    p2.start()
    p3 = Process(target=worker_insert_com_url, name='p3', args=(801, 1000,))
    p3.start()
    p4 = Process(target=worker_insert_com_url, name='p4', args=(1001, 1200,))
    p4.start()
    p5 = Process(target=worker_insert_com_url, name='p5', args=(1201, 1400,))
    p5.start()
    p6 = Process(target=worker_insert_com_url, name='p6', args=(1401, 1600,))
    p6.start()
    p7 = Process(target=worker_insert_com_url, name='p7', args=(1601, 1800,))
    p7.start()
    p8 = Process(target=worker_insert_com_url, name='p8', args=(1801, 2000,))
    p8.start()
    p9 = Process(target=worker_insert_com_url, name='p9', args=(2001, 2200,))
    p9.start()
    p10 = Process(target=worker_insert_com_url, name='p10', args=(2201, 2527,))
    p10.start()


def update_whole_companies_info_stock_code(index1, index2):
    """
    更新股票号
    :param index1:
    :param index2:
    :return:
    """
    init_industry_mysql()
    sql = "select id,com_url from industry_category_whole_companies_info where id BETWEEN " + str(
        index1) + " and " + str(index2) + ";"
    results = mysql.getAll(sql)
    for result in results:
        # https://s.askci.com/stock/summary/600537/
        base_url = 'https://s.askci.com/stock/summary/'
        com_url = result['com_url']
        stock_code = com_url[len(base_url):len(com_url) - 1]
        print(stock_code)
        sql_update_stock_code = "UPDATE industry_category_whole_companies_info SET stock_code=%s where id=%s"
        mysql.update(sql_update_stock_code, (stock_code, result['id']))


def get_company_profile_url_list_worker(start_page_num, end_page_num):
    """
    获取公司简介的URL的任务，并插入到数据库中
    :param start_page_num:
    :param end_page_num:
    :return:
    """
    init_selenium_util()
    init_industry_mysql()
    while True:
        url = "https://s.askci.com/stock/0-0-0/" + str(start_page_num) + "/"
        # print(url)
        selenium_util.get(url)
        tr_list = selenium_util.find_all_elements_by_xpath('//*[@id="ResultUl"]/tr')
        # print('解析 列表')
        items = parse_company_item_list(url, tr_list)
        if items is None:
            continue
        # print(items)
        for item in items:
            # print(item)
            sql = 'INSERT INTO industry_company_profile_simple (company_url, stock_code, stock_name, company_name, company_type,' \
                  ' main_business, datetime) VALUES(%s,%s,%s,%s,%s,%s,%s)'
            id_ = mysql.insert(sql, (item['company_url'], item['stock_code'], item['stock_name'], item['company_name'],
                                     item['company_type'],
                                     item['main_business'],
                                     item['datetime']
                                     ))
            if id_ != 1:
                print('error：' + url)
            else:
                print('right：' + url)
        if start_page_num == end_page_num:
            break
        start_page_num = start_page_num + 1
    print("done")
    selenium_util.quit()


def get_company_url_list_process():
    """
    开启十个进程,抓取全部的公司简介地址
    :return:
    """
    delt = 574 // 10 + 1
    for i in range(0, 10):
        start = delt * i + 1
        end = delt * (i + 1)
        print((start, end))
        p = Process(target=get_company_profile_url_list_worker, args=(start, end,))
        p.start()


def get_company_profile_detail(company_info_list):
    """

    :param company_info_list:
    :return:
    """
    for company_info in company_info_list:
        print(company_info)
        url = company_info['company_url']
        company_profile_map = company_detail(url)
        company_profile_map['collection_url'] = url
        company_profile_map['stock_code'] = company_info['stock_code']
        company_profile_map['stock_name'] = company_info['stock_name']
        company_profile_map['datetime'] = company_info['datetime']
        print(company_profile_map)
        sql_insert = "INSERT INTO industry_company_profile_detail ( datetime,collection_url,name_cn, name_en, name_old, area," \
                     " category_description, " \
                     "com_url, stock_name, main_business, product_name," \
                     " controller_stock, stock_code, controller_actual, " \
                     "controller_ultimate, president, president_secretary, " \
                     "representative_legal, general_manager, registered_capital," \
                     " employees_number, telephone, fax, postcode, company_address," \
                     " company_profile, president_chairman, " \
                     "representative_securities_affairs, balance_sheet_date," \
                     " registered_address, corporate_headquarters, auditor, " \
                     "legal_adviser, e_mail) " \
                     "VALUES (%s,%s,%s, %s,%s, %s,%s, " \
                     "%s,%s, %s,%s, %s,%s, %s,%s," \
                     " %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
        id_ = mysql.insert(sql_insert,
                           (
                               company_profile_map['datetime'],
                               company_profile_map['collection_url'],
                               company_profile_map['name_cn'],
                               company_profile_map['name_en'],
                               company_profile_map['name_old'],
                               company_profile_map['area'],
                               company_profile_map['catg_desc'],
                               company_profile_map['com_url'],
                               company_profile_map['stock_name'],
                               company_profile_map['main_business'],
                               company_profile_map['product_name'],
                               company_profile_map['controller_stock'],
                               company_profile_map['stock_code'],
                               company_profile_map['controller_actual'],
                               company_profile_map['controller_ultimate'],
                               company_profile_map['president'],
                               company_profile_map['president_secretary'],
                               company_profile_map['representative_legal'],
                               company_profile_map['general_manager'],
                               company_profile_map['registered_capital'],
                               company_profile_map['employees_number'],
                               company_profile_map['telephone'],
                               company_profile_map['fax'],
                               company_profile_map['postcode'],
                               company_profile_map['company_address'],
                               company_profile_map['company_profile'],
                               company_profile_map['president_chairman'],
                               company_profile_map['representative_securities_affairs'],
                               company_profile_map['balance_sheet_date'],
                               company_profile_map['registered_address'],
                               company_profile_map['corporate_headquarters'],
                               company_profile_map['auditor'],
                               company_profile_map['legal_adviser'],
                               company_profile_map['e_mail']
                           )
                           )
        if id_ == 1:
            print(id_)
            sql_update = 'UPDATE industry_company_profile_simple SET done=%s where company_url=%s '
            mysql.update(sql_update, (True, url))
    mysql.commit()


def get_company_profile_detail_work(index1, index2):
    """
    获取公司的详细信息
    :param index1: 起始 id
    :param index2: 终止 id
    :return:
    """
    init_industry_mysql()
    init_selenium_util()

    sql = "select id,company_url,stock_code,stock_name,datetime from industry_company_profile_simple where id BETWEEN " + str(
        index1) + " and " + str(index2) + ";"
    company_info_list = mysql.getAll(sql)
    get_company_profile_detail(company_info_list)
    selenium_util.quit()


def patch_company_profile_process(company_url_list):
    """
    补丁方法
    当使用 get_company_profile_detail_work 跑完之后，有一部分没有完成的，使用此方法
    :param company_url_list:
    :return:
    """
    for company_profile in company_url_list:
        print(company_profile)

    delt = len(company_url_list) // 10 + 1
    for i in range(0, 10):
        start = delt * i + 1
        end = delt * (i + 1)
        print((start, end))
        p = Process(target=patch_company_profile_work, args=(company_url_list[start:end],))
        p.start()
    # p = Process(target=patch_company_profile_work, args=(company_url_list,))
    # p.start()


def patch_company_profile_work(company_url_list):
    init_industry_mysql()
    init_selenium_util()
    get_company_profile_detail(company_url_list)


def patch_company_profile_worker(company_url_list):
    for company_url in company_url_list:
        # print(company_url['company_url'] + " id =" + str(company_url['id']))
        url = company_url['company_url']
        company_profile_map = company_detail(url)
        sql_insert = "INSERT INTO industry_company_profile" \
                     "_detail ( name_cn, name_en, name_old, area, category_description, " \
                     "com_url, stock_name, main_business, product_name," \
                     " controller_stock, stock_code, controller_actual, " \
                     "controller_ultimate, president, president_secretary, " \
                     "representative_legal, general_manager, registered_capital," \
                     " employees_number, telephone, fax, postcode, company_address," \
                     " company_profile, president_chairman, " \
                     "representative_securities_affairs, balance_sheet_date," \
                     " registered_address, corporate_headquarters, auditor, " \
                     "legal_adviser, e_mail) " \
                     "VALUES (%s, %s,%s, %s,%s, " \
                     "%s,%s, %s,%s, %s,%s, %s,%s," \
                     " %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
        try:
            id_ = mysql.insert(sql_insert,
                               (
                                   company_profile_map['name_cn'],
                                   company_profile_map['name_en'],
                                   company_profile_map['name_old'],
                                   company_profile_map['area'],
                                   company_profile_map['catg_desc'],
                                   company_profile_map['com_url'],
                                   company_profile_map['stock_name'],
                                   company_profile_map['main_business'],
                                   company_profile_map['product_name'],
                                   company_profile_map['controller_stock'],
                                   company_profile_map['stock_code'],
                                   company_profile_map['controller_actual'],
                                   company_profile_map['controller_ultimate'],
                                   company_profile_map['president'],
                                   company_profile_map['president_secretary'],
                                   company_profile_map['representative_legal'],
                                   company_profile_map['general_manager'],
                                   company_profile_map['registered_capital'],
                                   company_profile_map['employees_number'],
                                   company_profile_map['telephone'],
                                   company_profile_map['fax'],
                                   company_profile_map['postcode'],
                                   company_profile_map['company_address'],
                                   company_profile_map['company_profile'],
                                   company_profile_map['president_chairman'],
                                   company_profile_map['representative_securities_affairs'],
                                   company_profile_map['balance_sheet_date'],
                                   company_profile_map['registered_address'],
                                   company_profile_map['corporate_headquarters'],
                                   company_profile_map['auditor'],
                                   company_profile_map['legal_adviser'],
                                   company_profile_map['e_mail']
                               )
                               )
            if id_ == 1:
                print(id_)
                sql_update = 'UPDATE industry_company_profile_simple SET done=%s where company_url=%s '
                mysql.update(sql_update, (True, url))
        except Exception as e:
            print(traceback.format_exc())
            continue
    selenium_util.quit()


def patch_company_profile():
    """
    patch_company_profile_process
    打补丁，有些因为字符数过长导致没有成功插入到数据库
    :return:
    """
    init_industry_mysql()
    sql = "select id,company_url,stock_code,stock_name,datetime from industry_company_profile_simple where done = 0;"
    company_profile_url_list = mysql.getAll(sql)
    print(len(company_profile_url_list))
    patch_company_profile_process(company_profile_url_list)


def get_company_profile_info_process():
    """
    获取公司的简介信息,保存到数据库中
    :return:
    """
    delt = 1721
    for i in range(0, 10):
        start = delt * i + 1
        end = delt * (i + 1)
        print((start, end))
        p = Process(target=get_company_profile_detail_work, args=(start, end,))
        p.start()


def sync_stock_code():
    init_industry_mysql()
    sql = 'select id,stock_code,name_cn from industry_company_profile_detail where length(stock_code)<6'
    res_old = mysql.getAll(sql)
    print('len_old', str(len(res_old)))
    for item_old in res_old:
        print('item_old', item_old)
        sql = "select id,stock_code,company_name from industry_company_profile_simple  where company_name = %s"
        res_new = mysql.getAll(sql, item_old['name_cn'])
        print('res_new', res_new)
        sql = 'update industry_company_profile_detail set stock_code = %s where stock_name = %s'
        # mysql.update(sql, res_new['stock_code'], item_old['stock_name'])


if __name__ == "__main__":
    # init_industry_mysql()
    # init_selenium_util()
    # update_industry_catg_url()
    # get_industry_catg_objs()
    # process_get_categories_contains_all_com_url()
    # update_whole_companies_info_stock_code(1, 47005)
    get_company_url_list_process()
    # get_company_profile_info_process()
    # patch_company_profile()
    # sync_stock_code()
