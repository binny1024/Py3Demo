# -*- coding: utf-8 -*-
# @Time : 2020/1/6 17:21
# @Author : xubinbin
import os
from time import sleep, time

from QZone.QQZoneLogin import login_qzone
import traceback
from utils.selenium_uitls import SeleniumUtil

selenium_util = SeleniumUtil()

if __name__ == "__main__":
    try:
        path = './shuoshuo'
        if not os.path.exists(path):
            os.mkdir(path)
        # selenium_util.set_chrome_forbidden_image()
        selenium_util.init()
        selenium_util.set_waiting_time(50)

        # 浏览器窗口最大化
        selenium_util.set_window_size_max()
        # 浏览器地址定向为qq登陆页面
        selenium_util.driver.get('https://i.qq.com/')
        # 定位输入信息frame
        selenium_util.find_element_by_id('login_frame')
        selenium_util.driver.switch_to.frame("login_frame")

        # 快捷登录 二维码
        face = selenium_util.find_elements_by_class_name('face')
        selenium_util.sleep(2)
        face[0].click()
        selenium_util.sleep(2)
        # driver.switch_to.default_content()
        qq = '1021600743'  # 马卫军
        qq = '1270976774'  # 孙月
        qq = '596928539'  # 自己
        shuoshuo = open(path + os.sep + qq + '.txt', 'a+')
        selenium_util.driver.get('https://user.qzone.qq.com/' + qq)
        try:
            """
            刚进空间,如果会跳出一个 '我知道了' 按钮,则点击一下该按钮
            不点击是否可以执行后面逻辑
            """
            selenium_util.driver.find_element_by_link_text("我知道了").click()
            selenium_util.sleep(1)
            print("我知道了")
        except Exception as e:
            print("没有发现 --我知道了-- 弹窗")

        # 账号密码登录
        # selenium_util.driver.find_element_by_id("switcher_plogin").click()
        # # 账号输入框输入已知qq账号
        # selenium_util.driver.find_element_by_id("u").send_keys("596928539")
        # # 密码框输入已知密码
        # selenium_util.driver.find_element_by_id("p").send_keys("lx1228xbb")
        # # 自动点击登陆按钮
        # selenium_util.driver.find_element_by_id("login_button").click()
        # sleep(15)
        # driver.switch_to.default_content()

        selenium_util.wait_presence_by_link_text('说说')
        selenium_util.driver.find_element_by_link_text('说说').click()
        selenium_util.find_element_by_id('app_canvas_frame')
        selenium_util.switch_to_frame('app_canvas_frame')
        print("进入 iframe")
        selenium_util.scroll_window_to_bottom()
        # 获取 最大页数
        page_num_str = selenium_util.find_element_by_id('pager_last_0').text
        print('page_num = ' + page_num_str)
        page_num = int(page_num_str) + 1
        print('page_num = ' + str(page_num))
        for i in range(0, page_num):
            selenium_util.sleep(5)
            # selenium_util.scroll_window_to_top()
            # 获取说说内容
            content_list = selenium_util.find_elements_by_class_name('content')
            # 获取发表说说的时间
            date_list = selenium_util.find_elements_by_class_name('c_tx.c_tx3.goDetail')
            # 当前页说说的个数
            count = len(content_list)
            for j in range(0, count):
                print(date_list[j].text + " : " + content_list[j].text)
                shuoshuo.write(date_list[j].text + " : " + content_list[j].text + "\n\n\t")
            if i == page_num:
                print('爬完最后一页...')
                break
            print("爬第  " + str(i + 1) + "  页数据")
            while True:
                print('是否出现页面索引....')
                try:

                    if selenium_util.driver.find_element_by_link_text(
                            '下一页'):
                        print('可以跳转......')
                        selenium_util.sleep(5)
                        selenium_util.driver.find_element_by_link_text('下一页').click()
                        break
                except Exception as e:
                    if i == page_num:
                        print('爬完最后一页...')
                        break
                    else:
                        print('继续等待.....')
                selenium_util.scroll_window_to_bottom()

            # selenium_util.switch_to_frame('app_canvas_frame')
            # selenium_util.refresh()
            # selenium_util.scroll_window_to_bottom()
            # selenium_util.find_element_by_id('pager_go_0').send_keys(str(i))
            # selenium_util.sleep(5)
            # selenium_util.find_element_by_id('pager_gobtn_0').click()
            # selenium_util.scroll_window_to_top()
            # selenium_util.sleep(3)

            # selenium_util.scroll_window_to_bottom()

        shuoshuo.close()

        # 点击 下一页
        # selenium_util.find_element_by_id('pager_next_0').click()

        # next page
        # selenium_util.wait_presence_by_id('pager_next_0')
        # selenium_util.driver.find_element_by_id('pager_next_0').click()

    except Exception as e:
        print(traceback.format_exc())
        selenium_util.driver.close()
