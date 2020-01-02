#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from selenium import webdriver

if __name__ == '__main__':

    print("启动火狐浏览器")

    driver = webdriver.Firefox(executable_path="geckodriver")  # 初始化一个火狐浏览器实例：driver

    driver.maximize_window()  # 最大化浏览器

    driver.get("https://www.baidu.com")  # 通过get()方法，打开一个url站点
    print("启动成功")
