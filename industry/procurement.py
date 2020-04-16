from selenium.common.exceptions import NoSuchElementException

from dbmysql.MySqlConn import MyPymysqlPool
from utils.selenium_uitls import SeleniumUtil
from multiprocessing import Process

global selenium_util
global mysql

"""
中国政府采购网
"""


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
    user_agent = 'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; ' + \
                 'CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
    proxy_host = '222.95.144.204'
    proxy_port = '3000'
    proxy_ip = proxy_host + proxy_port
    selenium_util = SeleniumUtil(True, proxy=None,
                                 download_path='/Users/binny/PycharmProjects/Py3Utils/industry/industry')
    # selenium_util.set_waiting_time(10)
    selenium_util.set_window_size(1920, 1080)


# noinspection PyShadowingNames
def gather_gov_ccgp_url(title_name, inp_cus_start_time='2019-04-16', inp_us_end_time='2020-04-16'):
    """
    采集 采购公告信息列表，放到数据库中
    :param title_name:
    :param inp_cus_start_time:
    :param inp_us_end_time:
    :return:
    """
    sql = "INSERT INTO gov_main_info_url_list" \
          " (url,type_name) " \
          "VALUES (%s,%s)"
    url = 'http://search.ccgp.gov.cn/bxsearch?'
    init_selenium_util()
    init_industry_mysql()
    selenium_util.get(url)
    title = selenium_util.find_one_element_by_id("kw")
    SeleniumUtil.send_text(title, title_name)
    #     cusTime
    selenium_util.click_by_id('cusTime')
    selenium_util.set_element_value_by_id("inpCusStartTime", inp_cus_start_time)
    selenium_util.set_element_value_by_id("inpCusEndTime", inp_us_end_time)
    selenium_util.find_one_element_by_class_name('dose').click()
    ul = selenium_util.find_one_element_by_class_name('vT-srch-result-list-bid')
    # 取第一页
    lis = selenium_util.find_all_child_elements_by_tag(ul, 'li')
    for li in lis:
        a = selenium_util.find_one_child_element_by_tag(li, 'a')
        href = a.get_attribute('href')
        # print(href)
        select = 'select * from gov_main_info_url_list where url = %s'
        exist = mysql.getOne(select, href)
        if exist:
            print("已存在")
            continue
        id_ = mysql.insert(sql, (href, title_name))
        print(str(id_) + ' ' + href)
    # 获取 分页模块的标签
    """
    <p class="pager">
    <script language="javascript">Pager({
        size: 4,
        current: 0,
        prefix: 'data2',
        suffix: '.jsp&'
    });</script>
    <span class="prev">上一页</span>
    <span class="current">1</span>
    <a href="javascript:void(0)" onclick="gopage(2)">2</a>
    <a href="javascript:void(0)" onclick="gopage(3)">3</a>
    <a href="javascript:void(0)" onclick="gopage(4)">4</a>
    <a href="javascript:void(0)" onclick="gopage(2)" class="next">下一页</a>
    </p>
     """
    pager = selenium_util.find_one_element_by_class_name('pager')
    a_tag_list = selenium_util.find_all_child_elements_by_tag(pager, 'a')
    total_page = len(a_tag_list)
    # print(total_page)
    selenium_util.find_one_element_by_link_text('下一页')
    current = selenium_util.find_one_element_by_class_name('current')
    current_num = current.text
    # print(current_num)

    while True:
        print("current_num " + str(current_num) + 'total_page = ' + str(total_page))
        if current_num == total_page:
            break
        next_page = selenium_util.find_one_element_by_link_text('下一页')
        next_page.click()
        SeleniumUtil.sleep(5)
        ul = selenium_util.find_one_element_by_class_name('vT-srch-result-list-bid')
        lis = selenium_util.find_all_child_elements_by_tag(ul, 'li')
        for li in lis:
            a = selenium_util.find_one_child_element_by_tag(li, 'a')
            href = a.get_attribute('href')
            select = 'select * from gov_main_info_url_list where url = %s'
            exist = mysql.getOne(select, href)
            if exist:
                print("已存在")
                continue
            id_ = mysql.insert(sql, (href, title_name))
            print(str(id_) + ' ' + href)
        current = selenium_util.find_one_element_by_class_name('current')
        current_num = current.text
        print(title_name + "  current_num =  " + current_num)
    selenium_util.colse()


def make_get_list_items_process():
    """
    获取列表
    :return:
    """
    title_name = "区块链"
    #
    # inpCusStartTime = '2019-04-16'
    # inpCusEndTime = '2020-04-16'

    block_chain = Process(target=gather_gov_ccgp_url, name='block_chain', args=(title_name,))  # 必须加,号
    block_chain.start()
    title_name = "营商环境"
    environment_business = Process(target=gather_gov_ccgp_url, name='environment_business', args=(title_name,))  # 必须加,号
    environment_business.start()


def get_announcement_profile_page_info(url_list):
    """
    获取简介信息
    :param url_list:
    :return:
    """
    keys = {
        '采购类型': 'procurement_type',
        '此采购信息的地址': 'info_url',
        '采购项目名称': 'project_name',
        '品目': 'items',
        '采购单位': 'procurement_unit',
        '行政区域': 'administrative_region',
        '公告时间': 'notice_time',
        '获取招标的时间': 'tender_get_time',
        '招标文件售价': 'tender_documents_selling_price',
        '获取招标文件的地点': 'tender_documents_address',
        '开标时间': 'bidding_opening_time',
        '开标地点': 'bidding_opening_address',
        '预算金额': 'budget_amount',
        '项目联系人': 'project_contacts',
        '项目联系电话': 'project_phone',
        '采购单位地址': 'procurement_unit_address',
        '采购单位联系方式': 'procurement_unit_phone',
        '代理机构名称': 'agency_name',
        '代理机构地址': 'agency_place',
        '代理机构联系方式': 'agency_phone',
        '公告正文': 'main_body',
        '获取谈判文件的地点': 'negotiation_doc_get_address',
        '获取谈判文件的时间': 'negotiation_doc_get_date',
        '附件地址': 'attachment_address',
        '提交文件截止时间': 'submission_deadline',
        '资格审查日期': 'qualification_date',
        '本项目招标公告日期': 'project_tender_notice_date',
        '成交日期': 'bidding_get_date',
        '评审专家名单': 'professor_name_list',
        '总中标金额': 'bidding_get_total_amount',
        '首次公告日期': 'first_time_notice_date',
        '更正日期': 'modify_date',
        '获取磋商文件时间': 'consultation_document_get_time',
        '获取磋商文件地点': 'consultation_document_get_address',
        '响应文件递交时间': 'response_file_delivery_time',
        '响应文件递交地点': 'response_file_delivery_address',
        '响应文件开启时间': 'response_file_opening_time',
        '响应文件开启地点': 'response_file_opening_address',
        '谈判小组、询价小组成员、磋商小组成员名单及单一来源采购人员名单': 'person_names',
        '总成交金额': 'total_transaction_amount'
    }
    values = {
        'title': '',
        'procurement_type': '',
        'info_url': '',
        'project_name': '',
        'items': '',
        'procurement_unit': '',
        'administrative_region': '',
        'notice_time': '',
        'tender_get_time': '',
        'tender_documents_selling_price': '',
        'tender_documents_address': '',
        'bidding_opening_time': '',
        'bidding_opening_address': '',
        'budget_amount': '',
        'project_contacts': '',
        'project_phone': '',
        'procurement_unit_address': '',
        'procurement_unit_phone': '',
        'agency_name': '',
        'agency_place': '',
        'agency_phone': '',
        'main_body': '',
        'negotiation_doc_get_address': '',
        'negotiation_doc_get_date': '',
        'attachment_address': '',
        'submission_deadline': '',
        'qualification_date': '',
        'project_tender_notice_date': '',
        'bidding_get_date': '',
        'professor_name_list': '',
        'bidding_get_total_amount': '',
        'first_time_notice_date': '',
        'modify_date': '',
        'consultation_document_get_time': '',
        'consultation_document_get_address': '',
        'response_file_delivery_time': '',
        'response_file_delivery_address': '',
        'response_file_opening_time': '',
        'response_file_opening_address': '',
        'person_names': '',
        'total_transaction_amount': ''
    }
    init_selenium_util()
    init_industry_mysql()
    for url_obj in url_list:
        SeleniumUtil.sleep(5)
        # url = 'http://www.ccgp.gov.cn/cggg/zygg/zbgg/201906/t20190605_12210374.htm'
        url = url_obj['url']
        values['info_url'] = url
        # selenium_util.get(url)
        selenium_util.get(url)
        """
        获取公告类型
        //*[@id="detail"]/div[2]/div/div[1]/p
        
        //*[@id="detail"]/div[2]/div/div[1]/p/a[2]
        """
        procurement_type = selenium_util.find_one_element_by_xpath(
            '//*[@id="detail"]/div[2]/div/div[1]/p/a[2]').get_attribute('title')
        procurement_type = procurement_type + '-' + selenium_util.find_one_element_by_xpath(
            '//*[@id="detail"]/div[2]/div/div[1]/p/a[3]').get_attribute('title')
        procurement_type = procurement_type + '-' + selenium_util.find_one_element_by_xpath(
            '//*[@id="detail"]/div[2]/div/div[1]/p/a[4]').get_attribute('title')
        print(procurement_type)
        values['procurement_type'] = procurement_type
        """
        获取title
        """
        element_title = selenium_util.find_one_element_by_class_name('tc')
        title = element_title.text
        print(title)
        values['title'] = title
        """
        正文
        vF_detail_content_container
        """
        element_body = selenium_util.find_one_element_by_class_name('vF_detail_content_container')
        main_body = element_body.get_attribute("outerHTML")
        print(main_body)
        values['main_body'] = main_body

        """
        处理表格信息
        tbody ：这个标签有两个，取第一个
        """
        # selenium_util.close()
        tbody = selenium_util.find_one_element_by_tag('tbody')
        tr_list = selenium_util.find_all_child_elements_by_tag(tbody, 'tr')
        for tr in tr_list:
            # print(tr)
            tds = selenium_util.find_all_child_elements_by_tag(tr, 'td')
            if len(tds) <= 1:
                # 没有信息
                continue
            if len(tds) == 2:
                """
               第一个作为键，第二个作为值
               这里面包含附件的信息
               """
                if '附件' in tds[0].text:
                    for td in tds:
                        # print(td.text)
                        try:
                            # 如果有 a 标签，则是附件信息，保存下载链接，后续去下载
                            a = selenium_util.find_one_child_element_by_tag(td, 'a')
                            if a:
                                a_href = a.get_attribute('href')
                                a_text = a.text
                                # a_href.click()
                                print(a_text + '  ' + a_href)
                                # 保存附件信息 todo 正式采集时开启
                                # sql_accessory_insert = 'INSERT INTO gov_accessory_info ' \
                                #                        '(owner,download_url,file_name) VALUES (%s,%s,%s)'
                                # mysql.insert(sql_accessory_insert, (title, a_href, a_text))
                        except NoSuchElementException as e:
                            # print(e.msg)
                            continue
                    continue
                # print("key = " + tds[0].text + ' value = ' + tds[1].text)
                values[keys[tds[0].text]] = tds[1].text

            elif len(tds) == 4:
                # print("key = " + tds[0].text + ' value = ' + tds[1].text)
                # print("key = " + tds[2].text + ' value = ' + tds[3].text)
                values[keys[tds[0].text]] = tds[1].text
                values[keys[tds[2].text]] = tds[3].text
        for key in values:
            print(key + ':' + values[key])


def get_announcement_profile_url_list():
    """
    从数据中获取页面链接地址
    :return:
    """
    init_industry_mysql()
    #     从 url 数据库中读取 url
    query_url = 'select id,url from gov_main_info_url_list'
    query_res_list = mysql.getAll(query_url)
    # for query_res in query_res_list:
    #     print(query_res)
    return query_res_list


def make_get_announcement_profile_process():
    query_res_list = get_announcement_profile_url_list()
    p1 = Process(target=get_announcement_profile_page_info, name='p1', args=(query_res_list[0:20],))  # 必须加,号
    p1.start()


if __name__ == '__main__':
    # 中国政府采购网搜索界面
    # make_get_list_items_process()
    make_get_announcement_profile_process()
