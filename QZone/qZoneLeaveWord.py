# -*- coding: utf-8 -*-
# @Time : 2020/1/2 11:46
# @Author : xubinbin

from time import sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import requests
import json
from selenium.webdriver import ActionChains  # 处理悬停
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import traceback

from QZone.QQZoneLogin import login_qzone


def set_message(name, qq):
    # qq = 270067992
    driver.get("https://user.qzone.qq.com/" + str(qq))
    waiting_for_page_finish(2)
    try:
        """
        刚进空间,如果会跳出一个 '我知道了' 按钮,则点击一下该按钮
        不点击是否可以执行后面逻辑
        """
        driver.find_element_by_link_text("我知道了").click()
        waiting_for_page_finish(1)
        print("我知道了")
    except Exception as e:
        print("没有发现 --我知道了-- 弹窗")

    # 查看是否有权限访问还有空间
    try:
        if driver.find_element_by_class_name("btn_v2"):
            print("您无权访问此 " + name + " 空间......")
            return
    except:
        print("查找 访问权限 异常...")

    # 查看好友是否开通了空间
    try:
        if driver.find_element_by_link_text("邀请开通"):
            print(name + "空间已关闭......")
            return
    except:
        print("查找 是否开通 异常...")

    # 找留言板
    print("未在主页的主界面发现--留言模块--")
    try:
        waiting_for_page_finish(1)
        """
        通过  悬停 我的主页 按钮  进入留言板主界面
        """
        leave_msg_ele = driver.find_element_by_class_name('nav-list-inner')
        ActionChains(driver).move_to_element(leave_msg_ele).perform()
        waiting_for_page_finish(2)
        driver.find_element_by_link_text('留言板').click()
        print("找留言编辑框")
        waiting_for_page_finish(3)  # 等待页面加载
        iframe = driver.find_element_by_id("tgb")
        driver.switch_to.frame(iframe)
        driver.switch_to.frame("veditor1_Iframe")
        # 这里通过前面的方式  无法写入数据,这里使用 小path
        print("写留言")

        driver.find_element_by_xpath("/html/body").send_keys(name + "元旦快乐!python 自动留言脚本测试 -- 请自行删除--抱歉")
        driver.switch_to.parent_frame()
        if leave_msg:
            driver.find_element_by_id("btnPostMsg").click()
        return
    except Exception as e:
        print("最终没有留言....")


"""等待页面加载"""


def waiting_for_page_finish(seconds):
    sleep(seconds)


if __name__ == "__main__":
    leave_msg = False
    # 创建Chrome浏览器的一个Options实例对象
    chrome_options = Options()
    # 设置Chrome浏览器禁用PDF和Flash插件,把图片也关掉了。
    profile = {"plugins.plugins_disabled": ['Chrome PDF Viewer'],
               "plugins.plugins_disabled": ['Adobe Flash Player']}

    # profile = {"plugins.plugins_disabled": ['Chrome PDF Viewer'],
    #            "plugins.plugins_disabled": ['Adobe Flash Player'],
    #            "profile.managed_default_content_settings.images": 2}

    # chrome_options.add_experimental_option("prefs", profile)
    # prefs = {"profile.managed_default_content_settings.images": 2}

    chrome_options.add_experimental_option("prefs", profile)
    # 向Options实例中添加禁用扩展插件的设置参数项
    chrome_options.add_argument("--disable-extensions")
    # 添加屏蔽--ignore-certificate-errors提示信息的设置参数项
    chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    # 添加浏览器最大化的设置参数项，启动同时最大化窗口
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Firefox()
    actionChains = ActionChains(driver)
    try:
        login_qzone(driver)
        print('查找说说....')
        WebDriverWait(driver, 20, 1).until(
            EC.presence_of_element_located((By.LINK_TEXT, '说说'))
        )
        print('找到了 说说 ,点击说说')
        driver.find_element_by_link_text('说说').click()

        WebDriverWait(driver, 10, 0.5).until(
            EC.presence_of_element_located((By.ID, 'app_canvas_frame'))
        )
        driver.switch_to.frame('app_canvas_frame')
        print('查找提到的人....')
        # WebDriverWait(driver, 10, 0.5).until(
        #     EC.presence_of_element_located((By.ID, 'QM_Mood_Poster_Container'))
        # )
        # print('1')
        # WebDriverWait(driver, 10, 0.5).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'qz-poster-ft'))
        # )
        # print('2')
        # WebDriverWait(driver, 10, 0.5).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'qz-poster-attach'))
        # )
        # print('3')
        """
        将 iframe中的地址复制出来,
        然后,在浏览区使用 xpath 定位
        然后,把 xpath复制过来查找
        """
        WebDriverWait(driver, 10, 0.5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/div[6]/div[1]/a[2]'))
        )
        # WebDriverWait(driver, 10, 0.5).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'at'))
        # )
        # ele = driver.find_element_by_class_name('at')
        print('找到了提到的人....')
        waiting_for_page_finish(2)
        driver.find_element_by_class_name('at').click()
        driver.find_element_by_class_name('at').click()
        waiting_for_page_finish(2)
        # 获取 好友的列表狂,使用列表,然后在使用 集合去重
        friend_qq = []
        friend_name = []

        for i in range(0, 13):
            print("i = " + str(i))
            top = 400 * (i + 1)
            js = 'document.getElementsByClassName("friend_list")[0].scrollTop=' + str(top)
            # 就是这么简单，修改这个元素的scrollTop就可以
            driver.execute_script(js)
            waiting_for_page_finish(2)
            ul = driver.find_element_by_class_name('fSelector_friendlist')
            lis = ul.find_elements_by_xpath('li')
            for li in lis:
                if li.get_attribute('data-uin') is not None:
                    print(li.text + "----   " + li.get_attribute('data-uin'))
                    friend_qq.append(li.get_attribute('data-uin'))
                    friend_name.append(li.text)
        qq_num = set(friend_qq)
        friend_counts  =  len(qq_num)
        for i in range(0,friend_counts):
            print(friend_name[i]+" "+friend_qq[i]+ " index = "+ str(i))
            set_message(friend_name[i], friend_qq[i])

    except Exception as e:
        print(traceback.format_exc())
        # driver.close()
