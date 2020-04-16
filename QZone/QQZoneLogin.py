# -*- coding: utf-8 -*-
# @Time : 2020/1/6 17:19
# @Author : xubinbin


"""
登录扣扣空间
"""
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC


def login_qzone(driver):
    # 浏览器窗口最大化
    driver.maximize_window()
    # 浏览器地址定向为qq登陆页面
    driver.get('https://h5.qzone.qq.com/mqzone/index ')
    # 定位输入信息frame
    driver.switch_to.frame("login_frame")

    # 快捷登录 二维码
    # WebDriverWait(driver, 10, 1).until(
    #     EC.presence_of_element_located(
    #         (By.CLASS_NAME, 'face')
    #     )
    # )
    # driver.find_element_by_class_name('face').click()
    # driver.switch_to.default_content()

    """
    扫码登录
    """

    """
    账号密码登录
    """
    # # 自动点击账号登陆方式
    driver.find_one_element_by_id("switcher_plogin").click()
    # 账号输入框输入已知qq账号
    driver.find_one_element_by_id("u").send_keys("596928539")
    # 密码框输入已知密码
    driver.find_one_element_by_id("p").send_keys("lx1228xbb")
    # 自动点击登陆按钮
    driver.find_one_element_by_id("login_button").click()
    sleep(15)
    # driver.switch_to.default_content()
pass
