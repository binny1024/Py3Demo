from time import sleep

from selenium import webdriver

if __name__ == "__main__":
    # 打开火狐浏览器(唯一默认支持的浏览器)
    driver = webdriver.Chrome()
    try:
        # 浏览器窗口最大化
        driver.maximize_window()
        # 浏览器地址定向为qq登陆页面
        driver.get("https://user.qzone.qq.com/615807914")

        sleep(20)
        # 找到留言板
        driver.find_element_by_link_text("留言板").click()
    except Exception as e:
        print(e)
        # driver.close()
