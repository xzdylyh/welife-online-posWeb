#coding=utf-8
from selenium import webdriver
from pos.page import loginpage
import pytest
import allure

@allure.feature('登录功能')
class TestLogin:

    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    url = 'http://pos.acewill.net/'
    username = '13522656892'
    password = '123456'
    code = '1234'

    @allure.story('加入购物车')
    @allure.title('登录')
    def testLogin(self):
        login = loginpage.LoginPage(self.url,self.driver,'POS系统登录')
        login.open     #打开登录页面
        login.inputUserName(self.username) #输入用户名
        login.inputPassWord(self.password) #输入密码
        login.inputCode(self.code) #输入验证码
        login.btnClick #单击登录

if __name__=="__main__":
    pytest.main(['--allure_stories=登录功能', '--allure_severities=critical, blocker'])