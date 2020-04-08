from dbmysql.MySqlConn import MyPymysqlPool
from utils.selenium_uitls import SeleniumUtil
import re


def company_detail(url):
    selenium_util.driver.get(url)
    # /html/body/div[2]/div[3]/div[1]/h1
    xpath_share_name_with_code = '/html/body/div[2]/div[3]/div[1]/h1'
    results = selenium_util.find_element_by_xpath(xpath_share_name_with_code)
    share_name_with_code_text = results.text
    # 需要处理一下 *************************
    share_name_with_code_text = share_name_with_code_text.replace("  ", "")
    reg = '(?<=\().*(?=\))'
    share_name = re.findall(reg, share_name_with_code_text)
    # share_code = share_name_with_code_text.split(" ")[1]
    print(share_name)
    # 需要处理一下 *************************

    xpath_tbody = '/html/body/div[2]/div[3]/div[2]/div[2]/table/tbody/tr'
    tr_list = selenium_util.find_elements_by_xpath(xpath_tbody)
    print(len(tr_list))
    keys = {
        '公司名称：': '',
        '英文名称：': '',
        '曾 用 名：': '',
        '所属地域：': '',
        '所属行业：': '',
        '公司网址：': '',
        '主营业务：': '',
        '产品名称：': '',
        '控股股东：': '',
        '实际控制人：': '',
        '最终控制人：': '',
        '董 事 长：': '',
        '董　　秘：': '',
        '法人代表：': '',
        '总 经 理：': '',
        '注册资金：': '',
        '员工人数：': '',
        '电　　话：': '',
        '传　　真：': '',
        '邮　　编：': '',
        '办公地址：': '',
        '公司简介：': '',
        '董事会主席：': '',
        '证券事务代表：': '',
        '年结日：': '',
        '注册地址：': '',
        '公司总部：': '',
        '电邮：': '',
        '核数师：': '',
        '法律顾问：': '',
        'share_type': '',
        'orgcode': "",
        '电话：': '',
        '传真：': '',
        '网址：': '',
    }
    value = {
        'name_cn': '',
        'name_en': '',
        'name_old': '',
        'area': '',
        'catg_desc': '',
        'com_url': '',
        'main_business': '',
        'product_name': '',
        'controller_share': '',
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
        'com_url': '',
        'auditor': '',
        'legal_adviser': '',
        'share_type': '',
        'orgcode': ""
    }

    for tr in tr_list:
        # /html/body/div[2]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[2]
        td_key = selenium_util.find_child_element_by_xpath(tr, './/td[1]')
        td_value = selenium_util.find_child_element_by_xpath(tr, './/td[2]')
        if td_key.text in keys.keys():
            # print(td_key.text)
            if td_key.text == '所属行业：':
                tds = selenium_util.find_child_elements_by_tag(td_value, 'a')
                print(tds[0].text)
                print(tds[1].text)
                continue
            print(td_key.text + td_value.text)

    # print(share_code)
    # for tr in results:
    #     print(tr.text)
    #
    # next_page = selenium_util.find_element_by_link_text('下一页')
    # clickable = next_page.is_enabled()
    # print('clickable = ' + str(clickable))
    #
    # if clickable:
    #     next_page.click()
    #     results = selenium_util.find_elements_by_xpath('//*[@id="ResultUl"]/tr')
    #     for tr in results:
    #         print(tr.text)

    # clickable = selenium_util.element_to_be_clickable('下一页')


def get_company_list():
    """
    获取上市公司的列表页面的完成地址
    :return:  完整的,带有股票类型和行业的完整的地址
    """
    mysql = get_industry_mysql()
    url_base = 'https://s.askci.com/stock/'

    sql_all_item = 'select id,stocktype,orgcode from indstry_catg;'
    result = mysql.getAll(sql_all_item)
    whole_url_list = []
    for res in result:
        # print(res)
        whole_url = url_base + res['stocktype'] + '-' + res['orgcode'] + '-0/1/'
        # print(whole_url)
        whole_url_list.append(whole_url)

    sql = "INSERT INTO `industry_com_url` (com_url, done) VALUES ( %s,%s)"

    for company_url in whole_url_list:
        # print(company_url)
        # parse_company_list_page(company_url)
        id_ = mysql.insert(sql, (company_url, False))
        print(id_)
    mysql.dispose()
    return whole_url_list


def get_industry_mysql():
    mysql = MyPymysqlPool("../dbmysql/industry_mysql.ini", 'mysql_config')
    return mysql


def parse_company_list_page(url):
    """
     解析上市公司列表页,查看是否有数据
    :param url:
    :return:
    """
    selenium_util.driver.get(url)

    tr_list = selenium_util.find_elements_by_xpath('//*[@id="ResultUl"]/tr')
    if (len(tr_list) == 1) and (tr_list[0].text == '暂无数据'):
        print("此页没有公司列表 " + url)
        return
    a_href_list = parse_current_company_list(tr_list)
    next_page = selenium_util.find_element_by_link_text('下一页')
    clickable = next_page.is_enabled()
    while clickable:
        print('clickable = ' + str(clickable))
        next_page.click()
        results = selenium_util.find_elements_by_xpath('//*[@id="ResultUl"]/tr')
        a_href_list = a_href_list + parse_current_company_list(results)
        selenium_util.scroll_window_to_down()
        next_page = selenium_util.find_element_by_link_text('下一页')
        if next_page is None:
            break
        clickable = next_page.is_enabled()

    for href in a_href_list:
        print(href)
        # company_detail(href)


def parse_current_company_list(tr_list):
    # 遍历上市公司列表
    a_href_list = []
    for tr in tr_list:
        # print(tr.text)
        # /html/body/div[3]/div[2]/div[1]/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/a

        # 获取子元素
        a = selenium_util.find_child_element_by_xpath(tr, './/td[2]/a')
        # 获取跳转链接
        company_detail_url = a.get_attribute('href')
        # print(company_detail_url)
        a_href_list.append(company_detail_url)
    return a_href_list


if __name__ == "__main__":
    # get_company_list()
    # mysql = get_industry_mysql()
    # sql_all = 'select com_url from industry_com_url;'
    # company_url_list = mysql.getAll(sql_all)

    selenium_util = SeleniumUtil()
    selenium_util.set_waiting_time(5)
    selenium_util.set_window_size(1920, 1080)

    # parse_company_list_page('https://s.askci.com/stock/xsb-ci0000000205-0/1/')
    # company_detail('https://s.askci.com/stock/summary/000001/')
    company_detail('https://s.askci.com/stock/summary/HK0001/')
    # for company_url in company_url_list:
    #     print(company_url['com_url'])
    #     company_detail(company_url['com_url'])
# industry(url)
# selenium_util.close()
