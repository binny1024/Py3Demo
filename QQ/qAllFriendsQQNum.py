from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get("https://qzone.qq.com/")   #访问QQ空间登陆页面
browser.maximize_window()   #设成全屏，可要可不要
browser.switch_to.frame('login_frame')   #切换到输入账号密码的框架
browser.find_element_by_id("switcher_plogin").click()  #点击账号密码登陆选项
time.sleep(1)
browser.find_element_by_id('u').clear()   #输入账号密码
browser.find_element_by_id('u').send_keys('596928539')
browser.find_element_by_id('p').clear()
browser.find_element_by_id('p').send_keys('gx1024wr')
browser.find_element_by_id('login_button').click()
time.sleep(10)   #唔。。虽然是脚本，但并没有全自动，验证码还得自己拉，这里的时间是留着拉验证码和网页加载的


browser.get("https://user.qzone.qq.com/596928539/profile/permit")   #一开始想一直用点击，后来发现这样更方便
time.sleep(5)
browser.switch_to.frame("ttinfo")   #切换到空间设置框架
browser.find_element_by_id('entry_desc').click()   #点击蓝色字体，拉出好友列表
time.sleep(2)

browser.execute_script('document.getElementsByClassName("friends-detail friends-detail-visit qz-scrollbar")[0].scrollTop=10000')#控制滚轮往下翻，为啥这么多一样的代码呢，因为我想了个最省事的方法，好友不多，直接滚六次，哈哈哈
time.sleep(1)
browser.execute_script('document.getElementsByClassName("friends-detail friends-detail-visit qz-scrollbar")[0].scrollTop=10000')
time.sleep(1)
browser.execute_script('document.getElementsByClassName("friends-detail friends-detail-visit qz-scrollbar")[0].scrollTop=10000')
time.sleep(1)
browser.execute_script('document.getElementsByClassName("friends-detail friends-detail-visit qz-scrollbar")[0].scrollTop=10000')
time.sleep(1)
browser.execute_script('document.getElementsByClassName("friends-detail friends-detail-visit qz-scrollbar")[0].scrollTop=10000')
time.sleep(1)
browser.execute_script('document.getElementsByClassName("friends-detail friends-detail-visit qz-scrollbar")[0].scrollTop=10000')
time.sleep(1)

for link in browser.find_elements_by_xpath("//*[@data-uin]"):   #获取所有QQ号并写入文件
    print (link.get_attribute('data-uin'))
    with open('qqlist.txt','a') as f:
        f.write(link.get_attribute('data-uin')+'\n')
        f.close()