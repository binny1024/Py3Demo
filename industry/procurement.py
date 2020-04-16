from dbmysql.MySqlConn import MyPymysqlPool
from utils.phantomjs_utils import PhantomJsUtil
from utils.selenium_uitls import SeleniumUtil

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
    selenium_util = SeleniumUtil(True)
    # selenium_util.set_waiting_time(10)
    selenium_util.set_window_size(1920, 1080)


if __name__ == '__main__':
    # 中国政府采购网搜索界面
    url = 'http://search.ccgp.gov.cn/bxsearch?'

    title_name = "区块链"
    inpCusStartTime = '2019-04-16'
    inpCusEndTime = '2020-04-16'



    init_selenium_util()
    selenium_util.get(url)
    title = selenium_util.find_one_element_by_id("kw")
    SeleniumUtil.send_text(title, title_name)
    #     cusTime
    cusTime = selenium_util.click_by_id('cusTime')
    selenium_util.set_element_value_by_id("inpCusStartTime", inpCusStartTime)
    selenium_util.set_element_value_by_id("inpCusEndTime", inpCusEndTime)
    selenium_util.find_one_element_by_class_name('dose').click()

    ul = selenium_util.find_one_element_by_class_name('vT-srch-result-list-bid')

    # 取第一页
    lis = selenium_util.find_all_child_elements_by_tag(ul, 'li')
    for li in lis:
        a = selenium_util.find_one_child_element_by_tag(li, 'a')
        href = a.get_attribute('href')
        print(href)
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
    print(total_page)
    next_page = selenium_util.find_one_element_by_link_text('下一页')
    current = selenium_util.find_one_element_by_class_name('current')
    current_num = current.text
    print(current_num)
    next_page_clickable = True
    while next_page_clickable:
        if current_num == total_page:
            next_page_clickable = False
        next_page = selenium_util.find_one_element_by_link_text('下一页')
        next_page.click()
        ul = selenium_util.find_one_element_by_class_name('vT-srch-result-list-bid')
        lis = selenium_util.find_all_child_elements_by_tag(ul, 'li')
        for li in lis:
            a = selenium_util.find_one_child_element_by_tag(li, 'a')
            href = a.get_attribute('href')
            print(href)
        current = selenium_util.find_one_element_by_class_name('current')
        current_num = current.text
        print(current_num)
