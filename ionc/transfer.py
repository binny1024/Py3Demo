from utils.selenium_uitls import SeleniumUtil

selenium_util = SeleniumUtil()


def crawler():
    try:
        # 以太坊浏览器
        url = 'https://www.yitaifang.com/accounts/0xacb1b4ff1974e7ef03cacbbad98448237b913036#tab2'
        selenium_util.set_waiting_time(50)

        # 浏览器窗口最大化
        selenium_util.set_window_size_max()
        # 浏览器地址定向为qq登陆页面
        selenium_util.get(url)
        # /html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr[1]
        tx_lists = selenium_util.find_all_elements_by_xpath(
            '/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr')
        tx_lists_size = len(tx_lists)
        print('第一页,一共多少个 : ' + str(tx_lists_size))
        for index in range(0, tx_lists_size):
            tx_hash = selenium_util.find_one_child_element_by_class_name(tx_lists[index], 'address').text
            print('hash : ' + tx_hash)

            tx_time = selenium_util.find_one_child_element_by_class_name(tx_lists[index], 'time').text
            print("date : " + tx_time)

            tx_from_element = selenium_util.find_one_child_element_by_class_name(tx_lists[index], 'from')
            tx_from_text = selenium_util.find_one_child_element_by_class_name(tx_from_element, 'address').text
            print('from : ' + tx_from_text)

            tx_to_element = selenium_util.find_one_child_element_by_class_name(tx_lists[index], 'to')
            tx_to_text = selenium_util.find_one_child_element_by_class_name(tx_to_element, 'address').text
            print('  to : ' + tx_to_text)

            tx_value_element = selenium_util.find_all_child_elements_by_tag(tx_lists[index], 'td')[5]
            tx_value_element_text = tx_value_element.text
            print('value : ' + tx_value_element_text)

        selenium_util.close()
    except Exception as e:
        selenium_util.close()
        print(e)


if __name__ == "__main__":
    crawler()
