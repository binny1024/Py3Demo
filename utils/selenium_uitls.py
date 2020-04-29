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
    def __init__(self,
                 forbidden_image=False,
                 headless=True,
                 proxy=None,
                 ua=None,
                 download_path=None):
        # # get直接返回，不再等待界面加载完成
        # desired_capabilities = DesiredCapabilities.CHROME
        # desired_capabilities["pageLoadStrategy"] = "none"
        self.last_height = 0
        self.__prefs = {}
        self.__options = webdriver.ChromeOptions()
        if forbidden_image:
            self.set_chrome_forbidden_image()
        if headless:
            self.__options.add_argument('headless')  # 设置option
        if proxy:
            self.__options.add_argument("--proxy-server=http://" + proxy)

        if ua:
            # 通过设置user-agent，用来模拟移动设备
            self.__options.add_argument('user-agent=%s' % ua)
        if download_path:
            # 设置为 0 禁止弹出窗口
            self.__prefs['profile.default_content_settings.popups'] = 0
            self.__prefs['download.default_directory'] = download_path

        self.__options.add_argument('disable-infobars')
        self.__options.add_experimental_option('prefs', self.__prefs)
        self.__driver = webdriver.Chrome(r'../driver/chromedriver81',options=self.__options)
        self.waiting_time = 20

    def set_window_size_max(self):
        self.__driver.maximize_window()

    def set_window_size(self, w, h):
        self.__driver.set_window_size(w, h)

    def set_waiting_time(self, seconds=20):
        self.waiting_time = seconds

    def set_chrome_language_cn(self):
        # 设置中文
        self.__options.add_argument('lang=zh_CN.UTF-8')

    def set_chrome_close_test_hint(self):
        # 除去“正受到自动测试软件的控制”
        self.__options.add_argument('disable-infobars')

    def set_chrome_forbidden_image(self):
        # 禁止加载图片
        self.__options.add_argument('blink-settings=imagesEnabled=false')
        # 不加载图片和css
        self.__prefs["profile.managed_default_content_settings.images"] = 2
        self.__prefs['permissions.default.stylesheet'] = 2

    def set_chrome_mobile(self):
        # 更换头部
        self.__options.add_argument(
            'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

    def get_driver(self):
        return self.__driver

    def wait_presence_by_id(self, ele_id):
        """
        local element  by tag id
        :param ele_id:
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(
            EC.presence_of_element_located((By.ID, ele_id))
        )

    def wait_presence_by_link_text(self, link_text):
        """
        local element by link text
        :param link_text:
        """
        print('正在检查 ' + link_text + '是否可见')
        WebDriverWait(self.__driver, self.waiting_time, 1).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_text))
        )
        print(link_text + ' 可见')

    def scroll_window_to_down(self, distance=500):
        """
        向下滚动 一段距离
        :param distance:
        """
        self.__driver.execute_script('window.scrollBy(0,' + str(distance) + ');')

    def scroll_window_to_top(self):
        js = "var q=document.documentElement.scrollTop=0"
        self.__driver.execute_script(js)

    def refresh(self):
        self.__driver.refresh()

    def scroll_window_to_bottom(self):
        js_bottom = "var q=document.documentElement.scrollTop=10000"
        self.__driver.execute_script(js_bottom)

    def switch_to_frame(self, iframe):
        self.__driver.switch_to.frame(iframe)

    def switch_to_default_content(self):
        self.__driver.switch_to.default_content()

    def find_one_element_by_id(self, ele_id):
        WebDriverWait(self.__driver, self.waiting_time, 1).until(
            EC.presence_of_element_located(
                (By.ID, ele_id)
            )
        )
        return self.__driver.find_element_by_id(ele_id)

    def find_all_elements_by_id(self, ele_id):
        WebDriverWait(self.__driver, self.waiting_time, 1).until(
            EC.presence_of_element_located(
                (By.ID, ele_id)
            )
        )
        return self.__driver.find_elements_by_id(ele_id)

    def find_all_elements_by_class_name(self, class_name):
        WebDriverWait(self.__driver, self.waiting_time, 0.5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, class_name)
            )
        )
        return self.__driver.find_elements_by_class_name(class_name)

    def find_one_element_by_class_name(self, class_name):
        WebDriverWait(self.__driver, self.waiting_time, 0.5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, class_name)
            )
        )
        return self.__driver.find_element_by_class_name(class_name)

    def find_one_child_element_by_class_name(self, element, class_name):
        """
        查找 element 元素的子元素中类名为 class_name 的子元素
        :param element: 父元素
        :param class_name: 子元素的类名
        :return: 指定类名的子元素
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, class_name)
            )
        )
        return element.find_element_by_class_name(class_name)

    def find_all_child_elements_by_class_name(self, element, class_name):
        """
        查找 element 元素的子元素中类名为 class_name 的子元素
        :param element: 父元素
        :param class_name: 子元素的类名
        :return: 指定类名的子元素
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, class_name)
            )
        )
        return element.find_elements_by_class_name(class_name)

    def find_one_element_by_tag(self, tag_name):
        """

        :param tag_name:
        :return:
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.TAG_NAME, tag_name)
        ))
        return self.__driver.find_element_by_tag_name(tag_name)

    def find_all_elements_by_tag(self, tag_name):
        """

        :param tag_name:
        :return:
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.TAG_NAME, tag_name)
        ))
        return self.__driver.find_elements_by_tag_name(tag_name)

    def find_all_child_elements_by_tag(self, element, tag_name):
        """

        :param element:
        :param tag_name:
        :return:
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.TAG_NAME, tag_name)
        ))
        return element.find_elements_by_tag_name(tag_name)

    def find_one_child_element_by_tag(self, element, tag_name):
        """

        :param element:
        :param tag_name:
        :return:
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.TAG_NAME, tag_name)
        ))
        return element.find_element_by_tag_name(tag_name)

    def find_one_element_by_name(self, name):
        """

        :param name:
        :return:
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.NAME, name)
        ))
        return self.__driver.find_elements_by_name(name)

    def find_all_elements_by_xpath(self, xpath):
        """
        查找 指定 xpath 的所有元素
        :param xpath:
        :return:
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
        ))
        return self.__driver.find_elements_by_xpath(xpath)

    def find_all_child_elements_by_xpath(self, element, xpath):
        """
        查找 指定 xpath 的所有元素
        :param element:
        :param xpath:
        :return:
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
        ))
        return element.find_elements_by_xpath(xpath)

    def find_one_child_element_by_xpath(self, element, xpath):
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
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
        ))
        return element.find_element_by_xpath(xpath)

    def find_one_element_by_xpath(self, xpath):
        """
        查找 指定 xpath 的元素
        :param xpath:
        :return:
        """
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
        ))
        return self.__driver.find_element_by_xpath(xpath)

    def find_one_element_by_link_text(self, link_text):
        """

        :param link_text: 放文本不是 link_text 的时候 ,会走异常
        :return:
        """
        try:
            WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
                (By.LINK_TEXT, link_text)
            ))
        except Exception as e:
            print(e)
            return None
        return self.__driver.find_element_by_link_text(link_text)

    def find_all_elements_by_link_text(self, link_text):
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.LINK_TEXT, link_text)
        ))
        return self.__driver.find_elements_by_link_text(link_text)

    def element_to_be_clickable(self, link_text):
        WebDriverWait(self.__driver, self.waiting_time, 1).until(EC.presence_of_element_located(
            (By.LINK_TEXT, link_text)
        ))
        return EC.element_to_be_clickable((By.LINK_TEXT, link_text))

    def get(self, url):
        self.__driver.get(url)

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)

    def maximize_window(self):
        self.__driver.maximize_window()

    def close(self):
        self.__driver.close()

    def click_by_id(self, element_id):
        self.__driver.find_element_by_id(element_id).click()

    def set_element_value_by_id(self, element_id, value):
        """
        通过 执行js脚本获取 元素，然后设置元素的属性的值
        :param element_id:
        :param value:
        :return:
        """
        js = 'document.getElementById("' + element_id + '").value ="' + value + '"'
        print(js)
        self.__driver.execute_script(js)

    @staticmethod
    def send_text(element, text):
        """
        向元素发送文本
        :param element:
        :param text:
        :return:
        """
        element.send_keys(text)
