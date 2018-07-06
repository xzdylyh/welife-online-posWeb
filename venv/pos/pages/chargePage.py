#coding=utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from pos.lib import scripts,gl
import time,os


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
    chargeRMB_loc = (By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div[1]/div') #储值余额
    chargesBtn_loc = (By.ID,'chargeCheckBtn') #储值最后确认
    assertChargeSuccess_loc = (By.XPATH,'//*[@id="chargeSuccessModal"]/div/div/div[1]/h3') #储值成功提示
    consumeBtn_loc = (By.ID,'consumeBtn') #立即消费按钮
    usSaving_loc = (By.ID,'usSaving') #储值余额

    #被开发票
    toReceipt_loc = (By.ID,"toReceipt") #补开发票
    fill_RMB_loc = (By.XPATH,'//*[@id="receipt"]/div[2]/div[1]/div[2]/div[1]/div[5]/input') #第一行发票金额

    not_fill_RMB_loc = (By.XPATH,'//*[@id="receipt"]/div[2]/div[1]/div[2]/div[1]/div[4]') #未开发票金额
    fillBtn_loc = (By.XPATH,'//*[@id="receipt"]/div[2]/div[3]/div') #确定按钮


    #封装操作
    @property
    def open(self):
        yamldict = scripts.getYamlfield(os.path.join(gl.configPath, 'config.yaml'))
        ck_dict = yamldict['CONFIG']['Cookies']['LoginCookies']
        self._open(self.base_url,self.pagetitle)
        self.addCookies(ck_dict)
        #time.sleep(3)
        self._open(self.base_url, self.pagetitle)

    @scripts.Replay
    def selectTab(self,*loc):
        '''选择tab操作'''
        self.find_element(*loc).click()

    @scripts.Replay
    def inputText(self,text,desc,*loc):
        '''输入文本操作'''
        print '输入{0}:{1}'.format(desc,text)
        self.send_keys(text,*loc)

    @scripts.Replay
    def clickBtn(self,desc,*loc):
        '''点击操作'''
        print '单击:{0}'.format(desc)
        self.find_element(*loc).click()




    @property
    def assertCustom(self):
        '''断言进入消费页面'''
        bool_var = self.isExist(*(self.assertPhone))
        self.getImage
        return bool_var

    @property
    def assertChargeSuccess(self):
        '''断言支付成功'''
        bool_var = self.isExist(*(self.assertChargeSuccess_loc))
        self.getImage
        return bool_var





if __name__=="__main__":
    pass