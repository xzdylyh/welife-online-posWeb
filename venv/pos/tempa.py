#coding=utf-8
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
url = 'http://pos.beta.acewill.net/credit'

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)


# cookies 免登录，有效期一天。
# cls.driver.delete_all_cookies()
cookinfo = {"pos_entry_number": "1003935039186461",
                "pos_entry_actualcard": "1003935039186461",
                "pos_bid": "2048695606",
                "pos_mid": "1234871385",
                "pos_sid": "1512995661",
                "pos_sign": "369240630d5e17a24bf7e5a70f073465"}
for key in cookinfo.keys():
    driver.add_cookie({"name": key, "value": cookinfo[key]})

driver.get(url)

driver.find_element_by_id('charge_number').send_keys('1003935039186461')
driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/button').click()
time.sleep(3)

elements = driver.find_elements_by_xpath("//input[@name='rules[]']")
print elements
for box in elements:
    if not box.is_selected():
        box.click()


driver.find_element_by_name('credit').send_keys(1)
driver.find_element_by_name('detail').send_keys(u'自动化大礼包')
