#coding=utf-8
from selenium.webdriver.support.wait import WebDriverWait
from pos.lib import gl
import os
'''
basepage封装所有公共方法
'''
class BasePage(object):
    def __init__(self,baseurl,driver,pagetitle):
        self.base_url = baseurl
        self.driver = driver
        self.pagetitle = pagetitle

    '''
    功能描述：所有公共方法，都写在以下
    '''
    #打开浏览器
    def _open(self,url,pagetitle):
        self.driver.get(url)
        #self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        assert self.driver.title,pagetitle

    #查找元素
    def find_element(self,*loc):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda a: self.driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except:
            self.driver.get_screenshot_as_file(os.path.join(gl.reportPath,'images/error.png'))
            assert False,u'未能找到页面%s元素' % loc
            #print(u'未能找到页面%s元素' % loc)

    #文本框输入
    def send_keys(self,content,*loc):
        '''
        :param content: 文本内容
        :param itype: 如果等1，先清空文本框再输入。否则不清空直接输入
        :param loc: 文本框location定位器
        :return:
        '''
        inputElement = self.find_element(*loc)
        inputElement.clear()
        inputElement.send_keys(content)

    def clearInputText(self,*loc):
        '''清除文本框内容'''
        self.find_element(*loc).clear()



    def addCookies(self,ck_dict):
        '''
        增加cookies到浏览器
        :param ck_dict: cookies字典对象
        :return: 无
        '''
        for key in ck_dict.keys():
            #cookdict.append({"name":key,"value":ck_dict[key]})
            self.driver.add_cookie({"name":key,"value":ck_dict[key]})

    def isExist(self,*loc):
        '''
        判断元素是否存在
        :param loc: 定位器
        :return: 元素存在返回True;否则返回False
        '''
        if self.find_element(*loc).is_displayed():
            return True
        else:
            return False


if __name__=="__main__":
    ck_dict = {"pos_entry_number":"13522656892",
               "pos_entry_actualcard":"1726002880387638",
               "pos_bid":"2760627865",
               "pos_mid":"1134312064",
               "pos_sid":"3704059614",
               "pos_sign":"2a6ce62800f47551fd2826dab449b6cb"}

    #addCookies(ck_dict)


