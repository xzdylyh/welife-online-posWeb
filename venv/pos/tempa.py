#coding:utf-8
from requests import Session
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
'''
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.baidu.com')
driver.implicitly_wait(30)

loc = (By.ID,'kw')
'''
def find_element(*loc):
    """
    查询元素
    :param loc: 定位器
    :return: 找到返回元素对象 否则返回 None
    """
    """时间设置(秒)"""
    timeout = 10 #超时时间
    poll_frequency = 0.5 #轮询间隔时间

    start_time = time.time().__int__()
    while True:
        try:
            element = driver.find_element(*loc)
            return element
        except NoSuchElementException as ex:
            if (time.time().__int__() - start_time) >timeout:
                return None
        time.sleep(poll_frequency)


a = r"""%(id)s"""
print a % 3






