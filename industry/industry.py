from dbmysql.MySqlConn import MyPymysqlPool
from utils.selenium_uitls import SeleniumUtil
import re


class IndustryCompanyUrl:
    def __init__(self, catg_id, org_code, stock_type, url, done=False):
        """
        对应 表 industry_com_url
        :param catg_id:
        :param org_code:
        :param stock_type:
        :param url:
        :param done:
        """
        self.catg_id = catg_id
        self.org_code = org_code
        self.stock_type = stock_type
        self.url = url
        self.done = done


def company_detail(url, companies):
    print(url)
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
        '公司名称：': 'name_cn',
        '英文名称：': 'name_en',
        '曾 用 名：': 'name_old',
        '所属地域：': 'area',
        '所属行业：': 'catg_desc',
        '公司网址：': 'com_url',
        '主营业务：': 'main_business',
        '产品名称：': 'product_name',
        '控股股东：': 'controller_share',
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
        'share_type': '',
        'org_code': "",
        '电话：': 'telephone',
        '传真：': 'fax',
        '网址：': 'com_url',
    }
    value_in_mysql = {
        'catg_id': '',
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
        'auditor': '',
        'legal_adviser': '',
        'share_type': '',
        'share_name': '',
        'share_code': '',
        'e_mail': '',
        'org_code': ""
    }

    for tr in tr_list:
        # /html/body/div[2]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[2]
        td_key = selenium_util.find_child_element_by_xpath(tr, './/td[1]')
        td_value = selenium_util.find_child_element_by_xpath(tr, './/td[2]')
        td_key_text = td_key.text
        if td_key_text in keys.keys():
            # print(td_key.text)
            td_value_text = td_value.text
            if td_key_text == '所属行业：':
                tds = selenium_util.find_child_elements_by_tag(td_value, 'a')
                # print(tds[0].text)
                td_value_text = tds[0].text + tds[1].text
                print(td_key_text + td_value_text)
                if keys[td_key_text] in value_in_mysql:
                    value_in_mysql[keys[td_key_text]] = td_value_text
                    print(td_key_text + td_value_text)
                continue

            if keys[td_key_text] in value_in_mysql:
                value_in_mysql[keys[td_key_text]] = td_value_text
                print(td_key_text + td_value_text)

    value_in_mysql['catg_id'] = companies.catg_id
    value_in_mysql['share_code'] = 'todo'
    value_in_mysql['share_name'] = 'todo'
    value_in_mysql['share_type'] = companies.stock_type
    value_in_mysql['org_code'] = companies.org_code

    for key in value_in_mysql.keys():
        if value_in_mysql[key] == '':
            continue
        print(key + ':' + value_in_mysql[key])
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


def update_industry_catg_url():
    """
    获取上市公司的列表页面的完成地址 并更新到数据库
    :return:
    """
    mysql = get_industry_mysql()
    url_base = 'https://s.askci.com/stock/'

    sql_all_item = 'select id,stocktype,orgcode from industry_catg;'
    result = mysql.getAll(sql_all_item)
    com_url_objs = []
    for res in result:
        # print(res)
        whole_url = url_base + res['stocktype'] + '-' + res['orgcode'] + '-0/1/'
        com_url = IndustryCompanyUrl(res['id'], res['orgcode'], res['stocktype'], whole_url)
        # print(whole_url)
        com_url_objs.append(com_url)

    sql = 'UPDATE industry_catg SET catg_url=%s where orgcode=%s'

    for com_url_obj in com_url_objs:
        # print(company_url)
        # parse_company_list_page(company_url)
        id_ = mysql.update(sql, (com_url_obj.url,
                                 com_url_obj.org_code))
        print(id_)
    mysql.dispose()


def get_industry_mysql():
    """
    获取 mysql 对象
    :return:
    """
    mysql = MyPymysqlPool("../dbmysql/industry_mysql.ini", 'mysql_config')
    return mysql


def parse_company_url_list_page(industry_catg_obj):
    """
     解析上市公司列表页,查看是否有数据
    :param industry_catg_obj:
    :return:
    """
    url = industry_catg_obj.url
    selenium_util.driver.get(url)
    tr_list = selenium_util.find_elements_by_xpath('//*[@id="ResultUl"]/tr')
    if (len(tr_list) == 1) and (tr_list[0].text == '暂无数据'):
        print("此页没有公司列表 " + url)
        return
    print('正在解析')
    a_href_list = parse_current_company_list(tr_list)
    next_page = selenium_util.find_element_by_link_text('下一页')
    clickable = next_page.is_enabled()
    print('解析下一页')
    xpath_total_page_num = '//*[@id="kkpager"]/div[1]/span[2]/span/span[3]'
    total_page_num = selenium_util.find_element_by_xpath(xpath_total_page_num).text
    xpath_current_page_num = '//*[@id="kkpager"]/div[1]/span[2]/span/span[1]'
    while clickable:
        print('clickable = ' + str(clickable))
        next_page.click()
        results = selenium_util.find_elements_by_xpath('//*[@id="ResultUl"]/tr')
        a_href_list = a_href_list + parse_current_company_list(results)
        selenium_util.scroll_window_to_down()
        current_page_num = selenium_util.find_element_by_xpath(xpath_current_page_num).text
        print('current_page_num = ' + current_page_num + ' total_page_num = ' + total_page_num)
        if current_page_num == total_page_num:
            print('没有下一页了')
            break
        next_page = selenium_util.find_element_by_link_text('下一页')
        clickable = next_page.is_enabled()

    for href in a_href_list:
        print(href)

        # company_detail(href, companies)
    return a_href_list


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
    # update_industry_catg_url()

    mysql = get_industry_mysql()
    sql_all = 'select id,catg_url, orgcode, stocktype from industry_catg;'
    industry_catg_list = mysql.getAll(sql_all)
    industry_catg_objs = []
    for industry_catg in industry_catg_list:
        industry_catg_objs.append(IndustryCompanyUrl(
            industry_catg['id'],
            industry_catg['orgcode'],
            industry_catg['stocktype'],
            industry_catg['catg_url']
        ))

    print(len(industry_catg_objs))

    selenium_util = SeleniumUtil()
    selenium_util.set_waiting_time(10)
    selenium_util.set_window_size(1920, 1080)

    company_url_list = parse_company_url_list_page(industry_catg_objs[0])
    # todo : 将 获取的公司地址保存到数据库中

    # for industry_catg in industry_catg_list:
    #     parse_company_list_page(industry_catg)

    # parse_company_list_page('https://s.askci.com/stock/xsb-ci0000000205-0/1/')
    # company_detail('https://s.askci.com/stock/summary/000001/')
    # company_detail('https://s.askci.com/stock/summary/HK0001/')
    # parse_company_list_page(industry_catg_objs[0])
    # for company_url in company_url_list:
    #     print(company_url['com_url'])
    #     company_detail(company_url['com_url'])
    # industry(url)
    # selenium_util.close()
