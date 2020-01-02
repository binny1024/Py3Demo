https://www.jianshu.com/p/1531e12f8852

1,安装selenium
```
pip3 install selenium
```

2,webdriver安装

各大浏览器webdriver地址可参见：https://docs.seleniumhq.org/download/

[Firefox](https://github.com/mozilla/geckodriver/releases/),[chromedriver](https://sites.google.com/a/chromium.org/chromedriver/)
或者[chromedriver](http://chromedriver.storage.googleapis.com/index.html),[IE](http://selenium-release.storage.googleapis.com/index.html)

3,webdriver安装路径

Win：`复制webdriver到Python安装目录下`

Mac：`复制webdriver到/usr/local/bin目录下`

### 启动Chrome浏览器
```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://www.baidu.com/')
```