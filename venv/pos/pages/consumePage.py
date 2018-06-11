#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
import time

class ConsumePage(basepage.BasePage):
    '''消费功能模块'''

    '''消费方式选择界面'''
    #会员卡号或手机号Tab
    selectCardNo_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/a[1]')
    confirmBtn_loc = (By.XPATH,"//div[@id='ipt_box1']/div[1]/div[1]/button")
    inputCardorPhone_loc = (By.ID,'charge_number')

    #消费界面断言
    assertPhone = (By.XPATH,'/html/body/div[1]/div/dl/dt[2]')

    #优惠券码Tab

    '''消费界面'''
    tcTotalFee_loc = (By.ID,'tcTotalFee')  #消费总金额输入框
    tcStoredPay_loc = (By.ID,'tcStoredPay') #储值支付输入框
    tcUseCredit_loc = (By.ID,'tcUseCredit') #使用积分输入框
    checkbox_activity_loc = (By.XPATH,"//div[@id='userInfo']/form[1]/div[8]/div[1]/div[1]/div[1]") #参加活动复选框
    note_loc = (By.ID,'note') #备注
    showSubmit_loc = (By.ID,'showSubmit') #确认按钮,进入确认销费
    confirm_consume_loc = (By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div[2]/div/button[1]')  #确认消费按钮
    #使用积分
    tcUseCredit_loc = (By.ID,'tcUseCredit') #使用积分输入框

    #支付方式
    pay_loc = (By.XPATH,'/html/body/div[2]/div/div/div[1]/div[2]/form/div[10]/div/div/div/label[2]') #银行卡

    #交易密码
    pay_pwd = (By.ID,"password")
    pay_pwd_confirm = (By.XPATH,"/html/body/div[2]/div[2]/div/div/div[2]/form/div[3]/div/button[1]")

    #支付成功
    pay_success_loc = (By.XPATH,'/html/body/div[2]/div[1]/div/div[5]/div')

    #封装操作
    def open(self,ck_dict=''):
        self._open(self.base_url,self.pagetitle)
        if ck_dict!='':
            self.addCookies(ck_dict)
            #time.sleep(3)
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
        '''断言进入消费页面'''
        return self.isExist(*(self.assertPhone))

    @property
    def assertPaySuccess(self):
        '''断言支付成功'''
        self.isExist(*(self.pay_success_loc))


