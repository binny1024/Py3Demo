from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver


class PhantomJsUtil:
    @staticmethod
    def get_phantom_browser():
        options = webdriver.FirefoxOptions()
        # options.headless = True
        return webdriver.Firefox(options=options)


if __name__ == '__main__':
    options = webdriver.FirefoxOptions()
    browser = webdriver.Firefox(options=options)
    browser.get("http://www.ccgp.gov.cn/cggg/dfgg/gzgg/202003/t20200313_14003212.htm")
    browser.maximize_window()
    # //*[@id="hideGG"]
    title = browser.find_element_by_class_name('tc').text
    browser.save_screenshot("./uu/"+title + ".png")
    browser.close()
