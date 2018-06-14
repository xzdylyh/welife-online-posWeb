#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
import time

class CreditPage(basepage.BasePage):
    '''积分换礼页面'''
    #会员或手机号选择页面
    creditTab_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[1]/ul/li[2]/a') #积分换礼Tab
    charge_number_loc =(By.ID,'charge_number') #会员卡号或手机号
    creditBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/button') #确定按钮


    #换礼页面
    inputExchangeNumber_loc = (By.ID,'inputExchangeNumber') #扣减积分
    inputExchangeDetail_loc = (By.ID,'inputExchangeDetail') #礼品详情
    sendMessageBtn_loc = (By.XPATH,'//*[@id="creditInfo"]/form/div/div[2]/div/div/a[1]') #确定按钮
    cancelBtn_loc = (By.XPATH,'//*[@id="creditInfo"]/form/div/div[2]/div/div/a[2]') #返回按钮

    #-----
    credit_checkbox_loc =(By.XPATH,"//input[@name='rules[]']") #积分兑换规则div
    creditNum_loc = (By.NAME,'credit') #积分数量
    detail_loc = (By.NAME,'detail') #积分详情
    #成功提示
    #success_loc = (By.XPATH,'/html/body/div[2]/div[1]/div/div[5]/div') #兑换成功提示消息
    success_loc = (By.XPATH, '/html/body/div[5]')  # 兑换成功提示消息

    '''操作'''
    def open(self,ck_dict=''):
        self._open(self.base_url,self.pagetitle)
        if ck_dict!='':
            self.addCookies(ck_dict)
            #time.sleep(3)
            #self.driver.refresh()
            self._open(self.base_url, self.pagetitle)
            #time.sleep(3)

    def selectTab(self,*loc):
        '''选择tab操作'''
        self.find_element(*loc).click()

    def inputText(self,text,desc,*loc):
        '''输入文本操作'''
        print '输入{0}:{1}'.format(desc,text)
        self.send_keys(text,*loc)

    def clickBtn(self,desc,*loc):
        '''点击操作'''
        print '点击:{0}'.format(desc)
        self.find_element(*loc).click()

    def iterClick(self,desc,*loc):
        '''批量勾选积分规则'''
        elements = self.find_elements(*loc)
        for box in elements:
            i = 1
            if not box.is_selected():
                print '勾选:{0}{1}'.format(desc,i)
                box.click()
                i+=1


    @property
    def assertPaySuccess(self):
        '''断言支付成功'''
        self.isExist(*(self.charge_number_loc))