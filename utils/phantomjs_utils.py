from selenium import webdriver


class PhantomJsUtil:
    @staticmethod
    def get_phantom_browser():
        return webdriver.PhantomJS('/Users/binny/sdk/phantomjs-2.1.1-macosx/bin/phantomjs')


if __name__ == '__main__':
    browser = PhantomJsUtil.get_phantom_browser()
    browser.get("http://www.ccgp.gov.cn/cggg/dfgg/gzgg/202003/t20200313_14003212.htm")
    browser.maximize_window()
    # //*[@id="hideGG"]
    browser.find_element_by_class_name('displayArti').click()
    browser.save_screenshot("tttt.png")
    browser.close()
