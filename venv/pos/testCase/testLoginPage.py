#coding=utf-8
from selenium import webdriver
from pos.pages import loginpage
import unittest
class LoginPageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(30)
        cls.url = 'http://pos.acewill.net/'
        cls.username = '13522656892'
        cls.password = '123456'
        cls.code = '1234'


    def testLogin(self):
        login = loginpage.LoginPage(self.url,self.driver,'POS系统登录')
        login.open     #打开登录页面
        login.inputUserName(self.username) #输入用户名
        login.inputPassWord(self.password) #输入密码
        login.inputCode(self.code) #输入验证码
        login.btnClick #单击登录
        login.Assert()




if __name__=="__main__":
    unittest.main()