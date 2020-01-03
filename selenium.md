# 关于 selenium 的使用总结
## 元素定位
## 鼠标悬停
```python
from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
leave_msg_ele = driver.find_element_by_class_name('nav-list-inner')
ActionChains(driver).move_to_element(leave_msg_ele).perform()
```