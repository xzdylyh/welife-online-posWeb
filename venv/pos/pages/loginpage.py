#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By

class LoginPage(basepage.BasePage):
    #定位器
    username_loc = (By.ID,"mid")
    password_loc = (By.ID,"pwd")
    code_loc = (By.NAME,"captcha")
    button_loc = (By.XPATH,"//div[@id='page_main']/form/div[4]/div/button")
    assertField_loc = (By.XPATH,"//div[@id='errPage']/button")
    '''
    功能描述:所有登录页面，操作，写在以下
    '''
    @property
    def open(self):
        '''打开浏览器'''
        self._open(self.base_url,self.pagetitle)

    def inputUserName(self,username):
        '''输入用户名'''
        self.send_keys(username,*(self.username_loc))
        #self.find_element(*(self.username_loc)).send_keys(username)

    def inputPassWord(self,password):
        '''输入密码'''
        self.find_element(*(self.password_loc)).send_keys(password)

    def inputCode(self,code):
        '''输入验证码'''
        self.find_element(*(self.code_loc)).send_keys(code)

    @property
    def btnClick(self):
        '''点击登录        '''
        self.find_element(*(self.button_loc)).click()

    def Assert(self):
        '''错误提示不存在'''
        assert self.find_element(*(self.assertField_loc)).text=='消费 - 微生活POS系统'

