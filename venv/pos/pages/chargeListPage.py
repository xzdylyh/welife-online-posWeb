#coding=utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from pos.lib import scripts,gl
import time,os


class ChargeListPage(basepage.BasePage):
    '''储值模块'''
    #定位器
    charge_undoLink_loc = (By.XPATH,'//*[@id="chargeRunWater"]/table/tbody/tr[1]/td[16]/span[1]/a') #充值撤销链接
    charge_confirmBtn_loc = (By.ID,'confirmBtn') #确定按钮
    charge_undoSuccess_loc = (By.XPATH,'//*[@id="showSuccess"]/div/i') #成功提示
    charge_undoStatus_loc = (By.XPATH,'//*[@id="chargeRunWater"]/table/tbody/tr[1]/td[13]/span') #撤销充值后,流程增加一条


    #封装操作
    @property
    def open(self):
        yamldict = scripts.getYamlfield(os.path.join(gl.configPath, 'config.yaml'))
        ck_dict = yamldict['CONFIG']['Cookies']['LoginCookies']
        self._open(self.base_url,self.pagetitle)
        self.addCookies(ck_dict)
        self._open(self.base_url, self.pagetitle)

    @scripts.Replay
    def selectTab(self,*loc):
        '''选择tab操作'''
        self.find_element(*loc).click()

    @scripts.Replay
    def inputText(self,text,desc,*loc):
        '''输入文本操作'''
        print 'Input{0}:{1}'.format(desc,text)
        self.send_keys(text,*loc)

    @scripts.Replay
    def clickBtn(self,desc,*loc):
        '''点击操作'''
        print 'Click:{0}'.format(desc)
        self.find_element(*loc).click()




    @property
    def assertCustom(self):
        '''断言进入消费页面'''
        return self.isExist(*(self.assertPhone))

    @property
    def assertUndoSuccess(self):
        '''断言支付成功'''
        return self.isExist(*(self.charge_undoSuccess_loc))





if __name__=="__main__":
    pass