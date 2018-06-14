#coding=utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
import time

class ChargePage(basepage.BasePage):
    '''储值模块'''
    #定位器
    charge_number_loc = (By.ID,'charge_number')  #手机号或卡号
    confirmBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/button') #确定按钮
    chargeGZ_loc = (By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/div[1]/p[2]') #储值奖历规则
    coustomGZ_loc = (By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/a') #自定义储值规则
    present_loc = (By.ID,'present') #自定义输入金额
    customBtn_loc = (By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div/button')#确定按钮
    payType_loc =(By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[4]/div/div[1]/div/label[1]')#支付类型
    noteRemark_loc = (By.ID,'note') #备注
    chargeSubmit_loc = (By.ID,'chargeSubmit') #储值提交确定按钮
    chargeRMB_loc = (By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[1]/div')
    chargesBtn_loc = (By.ID,'chargeCheckBtn') #储值最后确认
    assertChargeSuccess_loc = (By.XPATH,'//*[@id="chargeSuccessModal"]/div/div/div[1]/h3') #储值成功提示
    consumeBtn_loc = (By.ID,'consumeBtn') #立即消费按钮


    #封装操作
    def open(self,ck_dict=''):
        self._open(self.base_url,self.pagetitle)
        if ck_dict!='':
            self.addCookies(ck_dict)
            #time.sleep(3)
            self._open(self.base_url, self.pagetitle)


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




    @property
    def assertCustom(self):
        '''断言进入消费页面'''
        return self.isExist(*(self.assertPhone))

    @property
    def assertChargeSuccess(self):
        '''断言支付成功'''
        self.isExist(*(self.assertChargeSuccess_loc))





if __name__=="__main__":
    pass