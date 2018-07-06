#coding=utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from pos.lib import scripts,gl
import time,os

class BjPrintPage(basepage.BasePage):
    """班结小票打印,页"""
    #定位器
    bjPrintLink_loc = (By.XPATH,'//*[@id="header-navbar-collapse"]/ul/li[3]/a') #首页,班结小票打印连接
    bjPrintStartDate_loc = (By.ID,'inputDateStart') #打印小票,开始时间
    bjPrintEndDate_loc = (By.ID,'inputDateEnd') #打印班结小票,结束时间
    bjPrintBtn_loc = (By.XPATH,'/html/body/div[2]/div/div/div[2]/form/div[2]/div/a[1]') #打印按钮
    #弹出的打印按钮
    bjPrintPopBtn_loc =(By.XPATH,'//*[@id="print-header"]/div/button[1]') #弹出页的打印按钮


    #操作
    @property
    def open(self):
        yamldict = scripts.getYamlfield(os.path.join(gl.configPath, 'config.yaml'))
        ck_dict = yamldict['CONFIG']['Cookies']['LoginCookies']
        self._open(self.base_url, self.pagetitle)
        self.addCookies(ck_dict)
        self._open(self.base_url, self.pagetitle)

    @scripts.Replay
    def selectTab(self, *loc):
        '''选择tab操作'''
        self.find_element(*loc).click()

    @scripts.Replay
    def inputText(self, text,desc, *loc):
        '''输入文本操作'''
        print '输入{0}:{1}'.format(desc,text)
        self.send_keys(text, *loc)

    @scripts.Replay
    def clickBtn(self, desc,*loc):
        '''点击操作'''
        print '单击:{0}'.format(desc)
        self.find_element(*loc).click()

    @property
    def assertPrint(self):
        """断言,弹出打印页面,点击打后后,页面消失_"""
        bool_var = self.isOrNoExist(*(self.bjPrintPopBtn_loc))
        self.getImage
        return bool_var

