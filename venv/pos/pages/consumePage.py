#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
import time

class ConsumePage(basepage.BasePage):
    '''消费功能模块'''
    #会员卡号或手机号Tab
    selectCardNo_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/a[1]')
    confirmBtn_loc = (By.XPATH,"//div[@id='ipt_box1']/div[1]/div[1]/button")
    inputCardorPhone_loc = (By.ID,'charge_number')

    #消费界面断言
    assertPhone = (By.XPATH,'/html/body/div[1]/div/dl/dt[2]')

    #优惠券码Tab

    #封装操作
    def open(self,ck_dict=''):
        self._open(self.base_url,self.pagetitle)
        if ck_dict!='':
            self.addCookies(ck_dict)
            time.sleep(3)
            self.driver.refresh()

    def selectTab(self,*loc):
        '''选择tab操作'''
        self.find_element(*loc).click()

    def inputText(self,text,*loc):
        '''输入文本操作'''
        self.send_keys(text,*loc)

    def clickBtn(self,*loc):
        '''点击操作'''
        self.find_element(*loc).click()

    @property
    def assertCustom(self):
        '''断言操作'''
        return self.isExist(*(self.assertPhone))




'''

from selenium import webdriver
import time
driver = webdriver.Firefox()

driver.get('https://pos.acewill.net')
driver.add_cookie({"name":"pos_entry_number","value":"13522656892"})
driver.add_cookie({"name":"pos_entry_actualcard","value":"1726002880387638"})
driver.add_cookie({"name":"pos_bid","value":"2760627865"})
driver.add_cookie({"name":"pos_mid","value":"1134312064"})
driver.add_cookie({"name":"pos_sid","value":"3704059614"})
driver.add_cookie({"name":"pos_sign","value":"2a6ce62800f47551fd2826dab449b6cb"})

time.sleep(3)

driver.refresh()




driver.implicitly_wait(30)
driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div[1]/a[1]').click()
driver.find_element_by_id('charge_number').send_keys('13466750022')
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div/div/button').click()
driver.find_element_by_id('associatedIpt').send_keys('1908091660719654')
driver.find_element_by_name('asso').click()
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[3]/button[1]').click()
ico = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[2]/form/div[1]/div[1]/strong/i')
assert ico.is_displayed()
driver.find_element_by_id('tcTotalFee').send_keys('10')
'''


