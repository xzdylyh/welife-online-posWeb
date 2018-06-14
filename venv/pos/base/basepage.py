#coding=utf-8
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EX
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from pos.lib import gl
import os,time
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
        self.driver.maximize_window()
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        assert self.driver.title,pagetitle

    #查找元素
    def find_element(self,*loc):
        try:
            element = WebDriverWait(self.driver, 10, 0.5).until(EX.visibility_of_element_located((loc)))
            return element
        except TimeoutException as ex:
            self.getImage  #截取图片
            raise

    @property
    def getImage(self):
        '''截取图片,并保存在images文件夹'''
        timestrmap = time.strftime('%Y%m%d_%H.%M.%S')
        imgPath = os.path.join(gl.imgPath, '%s.png' % str(timestrmap))
        print '错误截图路径:{0}'.format(imgPath)
        self.driver.save_screenshot(imgPath)

    def find_elements(self,*loc):
        '''批量找标签'''
        try:
            elements = self.driver.find_elements(*loc)
            return elements
        except NoSuchElementException as ex:
            self.getImage  #截取图片
            raise


    def iterClick(self, *loc):
        '''批量点击某元素'''
        element = self.find_elements(*loc)
        for e in element:
            e.click()


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


    def isExistAndClick(self,*loc):
        '''如果元素存在则单击,不存在则忽略'''
        try:
            self.driver.find_element(*loc).click()
        except NoSuchElementException,TimeoutException:
            pass

    def isExistAndInput(self,text,*loc):
        '''如果元素存在则输入,不存在则忽略'''
        try:
            element = self.driver.find_element(*loc)
            element.clear()
            element.send_keys(text)
        except NoSuchElementException,TimeoutException:
            pass



if __name__=="__main__":
    ck_dict = {"pos_entry_number":"13522656892",
               "pos_entry_actualcard":"1726002880387638",
               "pos_bid":"2760627865",
               "pos_mid":"1134312064",
               "pos_sid":"3704059614",
               "pos_sign":"2a6ce62800f47551fd2826dab449b6cb"}

    #addCookies(ck_dict)


