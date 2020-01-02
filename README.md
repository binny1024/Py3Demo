# Py3Utils
py3 scripting tools, including crawling tiger-teeth live stream, QQ space bulk message, increase the number of visits, etc.

# Environment
2, install selenium
```
pip3 install selenium
```
3,isntall chromedriver

I use chrome ,you you can download a driver depending your browser.

Chromedriver`s version must be same with your chrome browser version in you computer.

You can get the chromedriver from [Firefox](https://github.com/mozilla/geckodriver/releases/),[chromedriver](https://sites.google.com/a/chromium.org/chromedriver/)
or [chromedriver](http://chromedriver.storage.googleapis.com/index.html),[IE](http://selenium-release.storage.googleapis.com/index.html)

After you download  the driver ,you can put it in to the dictionary :
copy it into the path where python installed, 
or if you sue mac ,you can put it into `/usr/local/bin`.

Form now on ,you can use it like this:
```python
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://www.baidu.com/')
```

# Capacity 
Each module is a separate feature, and you can use only one of them. 
## huya
In this module, you can use it to grab the live stream information of tiger teeth.

![ee](https://github.com/binny1024/Py3Utils/blob/master/huya/img/grab_result.jpg)

