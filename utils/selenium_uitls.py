# -*- coding: utf-8 -*-
# @Time : 2020/1/7 10:41
# @Author : xubinbin
import os
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import traceback
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SeleniumUtil:
    def __init__(self, forbidden_image=False):
        # # get直接返回，不再等待界面加载完成
        # desired_capabilities = DesiredCapabilities.CHROME
        # desired_capabilities["pageLoadStrategy"] = "none"
        self.last_height = 0
        self.options = webdriver.ChromeOptions()
        if forbidden_image:
            self.set_chrome_forbidden_image()
        self.driver = webdriver.Chrome(options=self.options)
        self.waiting_time = 20

    def init(self):
        self.driver = webdriver.Chrome(options=self.options)

    def set_window_size_max(self):
        self.driver.maximize_window()

    def set_window_size(self, w, h):
        self.driver.set_window_size(w, h)

    def set_waiting_time(self, seconds=20):
        self.waiting_time = seconds

    def set_chrome_language_cn(self):
        # 设置中文
        self.options.add_argument('lang=zh_CN.UTF-8')

    def set_chrome_close_test_hint(self):
        # 除去“正受到自动测试软件的控制”
        self.options.add_argument('disable-infobars')

    def set_chrome_forbidden_image(self):
        # 禁止加载图片
        self.options.add_argument('blink-settings=imagesEnabled=false')
        # 不加载图片和css
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        self.options.add_experimental_option('prefs', prefs)

    def set_chrome_mobile(self):
        # 更换头部
        self.options.add_argument(
            'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

    def get_driver(self):
        return self.driver

    def wait_presence_by_id(self, ele_id):
        """
        local element  by tag id
        :param ele_id:
        """
        WebDriverWait(self.driver, self.waiting_time, 1).until(
            EC.presence_of_element_located((By.ID, ele_id))
        )

    def wait_presence_by_link_text(self, link_text):
        """
        local element by link text
        :param link_text:
        """
        print('正在检查 ' + link_text + '是否可见')
        WebDriverWait(self.driver, self.waiting_time, 1).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_text))
        )
        print(link_text + ' 可见')

    def scroll_window_to_down(self, distance=500):
        """
        向下滚动 一段距离
        :param distance:
        """
        self.driver.execute_script('window.scrollBy(0,' + str(distance) + ');')

    def scroll_window_to_top(self):
        js = "var q=document.documentElement.scrollTop=0"
        self.driver.execute_script(js)

    def refresh(self):
        self.driver.refresh()

    def scroll_window_to_bottom(self):
        js_bottom = "var q=document.documentElement.scrollTop=10000"
        self.driver.execute_script(js_bottom)

    def switch_to_frame(self, iframe):
        self.driver.switch_to.frame(iframe)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def find_element_by_id(self, ele_id):
        WebDriverWait(self.driver, self.waiting_time, 1).until(
            EC.presence_of_element_located(
                (By.ID, ele_id)
            )
        )
        return self.driver.find_element_by_id(ele_id)

    def find_elements_by_id(self, ele_id):
        WebDriverWait(self.driver, self.waiting_time, 1).until(
            EC.presence_of_element_located(
                (By.ID, ele_id)
            )
        )
        return self.driver.find_elements_by_id(ele_id)

    def find_elements_by_class_name(self, class_name):
        WebDriverWait(self.driver, self.waiting_time, 0.5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, class_name)
            )
        )
        return self.driver.find_elements_by_class_name(class_name)

    def find_child_element_by_class_name(self, element, class_name):
        """
        查找 element 元素的子元素中类名为 class_name 的子元素
        :param element: 父元素
        :param class_name: 子元素的类名
        :return: 指定类名的子元素
        """
        WebDriverWait(self.driver, self.waiting_time, 1).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, class_name)
            )
        )
        return element.find_element_by_class_name(class_name)

    def find_element_by_tag(self, tag_name):
        """

        :param tag_name:
        :return:
        """
        WebDriverWait(self.driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.TAG_NAME, tag_name)
        ))
        return self.driver.find_element_by_tag_name(tag_name)

    def find_elements_by_tag(self, tag_name):
        """

        :param tag_name:
        :return:
        """
        WebDriverWait(self.driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.TAG_NAME, tag_name)
        ))
        return self.driver.find_elements_by_tag_name(tag_name)

    def find_child_elements_by_tag(self, element, tag_name):
        """

        :param tag_name:
        :return:
        """
        WebDriverWait(self.driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.TAG_NAME, tag_name)
        ))
        return element.find_elements_by_tag_name(tag_name)

    def find_elements_by_xpath(self, xpath):
        """
        查找 指定 xpath 的所有元素
        :param xpath:
        :return:
        """
        WebDriverWait(self.driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
        ))
        return self.driver.find_elements_by_xpath(xpath)

    def find_child_elements_by_xpath(self, element, xpath):
        """
        查找 指定 xpath 的所有元素
        :param element:
        :param xpath:
        :return:
        """
        WebDriverWait(self.driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
        ))
        return element.find_elements_by_xpath(xpath)

    def find_child_element_by_xpath(self, element, xpath):
        """
        通过 xpath 查找指定 元素 的子元素,比如查找

        <tr>
          <td class="tab_fwit" style="height: 27px; width: 28px;">1</td>
          <td style="height: 27px; width: 56px;">
            <a href="/stock/summary/832113/" target="_blank">832113</a>
          </td>
          <td style="height: 27px; width: 56px;">
            <a href="/stock/summary/832113/" target="_blank">中康国际</a>
          </td>
        </tr>

        a = selenium_util.find_child_element_by_xpath(tr, './/td[2]/a')

        . 表示 选取当前节点。从 tr 开始查找

        :param element: 待查找的子元素的父元素
        :param xpath: 相对于当前父元素的 xpath
        :return: 查找到的元素
        """
        WebDriverWait(self.driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
        ))
        return element.find_element_by_xpath(xpath)

    def find_element_by_xpath(self, xpath):
        """
        查找 指定 xpath 的元素
        :param xpath:
        :return:
        """
        WebDriverWait(self.driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
        ))
        return self.driver.find_element_by_xpath(xpath)

    def find_element_by_link_text(self, link_text):
        """

        :param link_text: 放文本不是 link_text 的时候 ,会走异常
        :return:
        """
        try:
            WebDriverWait(self.driver, self.waiting_time, 1).until(EC.presence_of_element_located(
                (By.LINK_TEXT, link_text)
            ))
        except Exception as e:
            print(e)
            return None
        return self.driver.find_element_by_link_text(link_text)

    def find_elements_by_link_text(self, link_text):
        WebDriverWait(self.driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.LINK_TEXT, link_text)
        ))
        return self.driver.find_elements_by_link_text(link_text)

    def element_to_be_clickable(self, link_text):
        WebDriverWait(self.driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.LINK_TEXT, link_text)
        ))
        return EC.element_to_be_clickable((By.LINK_TEXT, link_text))

    def sleep(self, seconds):
        time.sleep(seconds)

    def maximize_window(self):
        self.driver.maximize_window()

    def close(self):
        self.driver.close()
