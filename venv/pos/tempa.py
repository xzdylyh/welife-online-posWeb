#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.baidu.com')

kw = (By.ID,'kw')

def aaaa(*loc):
    driver.implicitly_wait(30)
    try:
        driver.find_element(*loc)
        print '找到元素:{0}'.format(loc)
    except NoSuchElementException as ex:
        print ex

    driver.quit()

if __name__=="__main__":
    aaaa(*kw)