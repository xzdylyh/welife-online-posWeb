#coding=utf-8
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EX
from selenium.common.exceptions import NoSuchElementException,TimeoutException,ElementNotVisibleException
from pos.lib import gl
import os,time
from PIL import Image


'''
basepage封装所有公共方法
'''
class BasePage(object):
    """PO公共方法类"""
    def __init__(self,baseurl,driver,pagetitle):
        """
        初始化,driver对象及数据
        :param baseurl: 目标地址
        :param driver: webdriver对象
        :param pagetitle: 用来断言的目标页标题
        """
        self.base_url = baseurl
        self.driver = driver
        self.pagetitle = pagetitle

    '''
    功能描述：所有公共方法，都写在以下
    '''
    #打开浏览器
    def _open(self,url,pagetitle):
        """
        打开浏览器，并断言标题
        :param url: 目标地址
        :param pagetitle: 目标页标题
        :return: 无
        """
        self.driver.maximize_window()
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        assert self.driver.title,pagetitle

    '''
    #查找元素
    def find_element(self,*loc):
        """
        自封装，查找元素，智能等待
        :param loc: 元素定位器(By.ID,"xxxx")
        :return: 元素对象
        """
        try:
            #element = WebDriverWait(self.driver, 10, 0.5).until(EX.visibility_of_element_located((loc)))
            element = WebDriverWait(self.driver, 10, 0.5).until(lambda d: d.find_element(*loc))
            #元素高亮显示
            self.hightlight(element)
            return element
        except TimeoutException,NoSuchElementException:
            self.getImage  #截取图片
            raise
        '''

    def find_element(self,*loc):
        """
        查询元素
        :param loc: 定位器
        :return: 找到返回元素对象 否则返回 None
        """
        """时间设置(秒)"""
        timeout = 10  # 超时时间
        poll_frequency = 0.5  # 轮询间隔时间

        start_time = time.time().__int__()
        while True:
            try:
                element = self.driver.find_element(*loc)
                if element.is_displayed():
                    self.hightlight(element) #高亮显示
                    return element
                else:
                    self.getImage  # 截取图片
                    raise ElementNotVisibleException

            except NoSuchElementException as ex:
                if (time.time().__int__() - start_time) > timeout:
                    self.getImage  # 截取图片
                    raise ex
                    #return None
            time.sleep(poll_frequency)




    def hightlight(self,element):
        """
        元素高亮显示
        :param element: 元素对象
        :return: 无
        """
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                   element, "border: 2px solid red;")

    def getElementImage(self,element):
        """
        截图,指定元素图片
        :param element: 元素对象
        :return: 无
        """
        """图片路径"""
        timestrmap = time.strftime('%Y%m%d_%H.%M.%S')
        imgPath = os.path.join(gl.imgPath, '%s.png' % str(timestrmap))

        self.driver.save_screenshot(imgPath)
        left = element.location['x']
        top = element.location['y']
        elementWidth = left + element.size['width']
        elementHeight = top + element.size['height']

        picture = Image.open(imgPath)
        picture = picture.crop((left, top, elementWidth, elementHeight))
        timestrmap = time.strftime('%Y%m%d_%H.%M.%S')
        imgPath = os.path.join(gl.imgPath, '%s.png' % str(timestrmap))
        picture.save(imgPath)
        print  'screenshot:', timestrmap, '.png'

    @property
    def getImage(self):
        '''
        截取图片,并保存在images文件夹
        :return: 无
        '''
        timestrmap = time.strftime('%Y%m%d_%H.%M.%S')
        imgPath = os.path.join(gl.imgPath, '%s.png' % str(timestrmap))

        self.driver.save_screenshot(imgPath)
        print  'screenshot:', timestrmap, '.png'

    def find_elements(self,*loc):
        '''批量找标签'''
        try:
            elements = self.driver.find_elements(*loc)

            #元素高亮显示
            for e in elements:
                self.hightlight(e)

            return elements
        except NoSuchElementException as ex:
            self.getImage  #截取图片
            raise


    def iterClick(self, *loc):
        '''批量点击某元素'''
        element = self.find_elements(*loc)
        for e in element:
            e.click()

    def iterInput(self,text=[],*loc):
        """
        批量输入
        :param text: 输入内容
        :param loc: 定位器(By.XPATH,'//*[@id='xxxx']/input')
        :return: 无
        """
        elements = self.find_elements(*loc)
        for i,e in enumerate(elements):
            self.wait(1000)
            #e.clear()
            e.send_keys(text[i])


    #文本框输入
    def send_keys(self,content,*loc):
        '''
        :param content: 文本内容
        :param itype: 如果等1，先清空文本框再输入。否则不清空直接输入
        :param loc: 文本框location定位器
        :return:
        '''
        inputElement = self.find_element(*loc)
        #inputElement.clear()
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
        元素存在,判断是否显示
        :param loc: 定位器
        :return: 元素存在返回True;否则返回False
        '''
        try:
            element = WebDriverWait(self.driver, 10, 0.5).until(lambda d: d.find_element(*loc))
            if element.is_displayed():
                return True
            else:
                self.getImage
                return False
        except NoSuchElementException as ex:
            self.getImage
            return False


    def isOrNoExist(self,*loc):
        """
        判断元素,是否存在
        :param loc: 定位器(By.ID,'kw')
        :return: True 或 False
        """
        try:
            e = WebDriverWait(self.driver, 10, 0.5).until(lambda d:d.find_element(*loc))
            """高亮显示,定位元素"""
            self.hightlight(e)

            return True
        except NoSuchElementException as ex:
            self.getImage
            return False


    def isExistAndClick(self,*loc):
        '''如果元素存在则单击,不存在则忽略'''
        try:
            self.driver.find_element(*loc).click()
            #self.find_element(*loc).click()
        except NoSuchElementException as ex:
            pass

    def isExistAndInput(self,text,*loc):
        '''如果元素存在则输入,不存在则忽略'''
        try:
            element =self.driver.find_element(*loc)
            #element = self.find_element(*loc)
            #element.clear()
            element.send_keys(text)
        except NoSuchElementException as ex:
            pass

    def getTagText(self,txtName,*loc):
        """
        获取元素对象属性值
        :param propertyName: 属性名称
        :param loc: #定位器
        :return: 属性值 或 raise
        """
        element = self.find_element(*loc)
        try:
            proValue = getattr(element,str(txtName))
            return proValue
        except Exception as ex:
            self.getImage

    @property
    def switch_window(self):
        """
        切换window窗口,切换一次后退出
        :return: 无
        """
        curHandle = self.driver.current_window_handle
        allHandle = self.driver.window_handles
        for h in allHandle:
            if h != curHandle:
                self.driver.switch_to.window(h)
                break


    def wait(self,ms):
        """
        线程休眼时间
        :param ms: 毫秒
        :return: 无
        """

        ms = float(ms) / 1000
        time.sleep(ms)





if __name__=="__main__":
    ck_dict = {"pos_entry_number":"13522656892",
               "pos_entry_actualcard":"1726002880387638",
               "pos_bid":"2760627865",
               "pos_mid":"1134312064",
               "pos_sid":"3704059614",
               "pos_sign":"2a6ce62800f47551fd2826dab449b6cb"}

    #addCookies(ck_dict)


