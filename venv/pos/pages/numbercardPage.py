#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from pos.lib import scripts,gl
import time,os

class NumberCardPage(basepage.BasePage):
    """次卡消费模块"""
    """定位器"""
    number_phone_Loc = (By.ID,'charge_number') #手机号或卡号
    number_conrimBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/button') #确定
    number_usenum_loc = (By.XPATH,'//*[@id="numberCardInfo"]/div/div[1]/div/div[1]/div[2]/span[2]/input') #次卡使用数
    number_remark_loc = (By.XPATH,'//*[@id="note"]') #备注
    number_submit_loc = (By.ID,'numberSubmit') #提交

    """操作"""
    @property
    def open(self):
        yamldict = scripts.getYamlfield(os.path.join(gl.configPath, 'config.yaml'))
        ck_dict = yamldict['CONFIG']['Cookies']['LoginCookies']
        self._open(self.base_url,self.pagetitle)
        self.addCookies(ck_dict)
        #time.sleep(3)
        self._open(self.base_url, self.pagetitle)

    @scripts.Replay
    def selectTab(self,desc,*loc):
        '''选择tab操作'''
        print 'Select{0}:{1}'.format(desc,loc)
        self.find_element(*loc).click()

    @scripts.Replay
    def inputText(self,text,desc,*loc):
        '''输入文本操作'''
        print 'Input{0}:{1}'.format(desc,text)
        self.send_keys(text,*loc)


    @scripts.Replay
    def clickBtn(self,desc,*loc):
        '''单击操作'''
        print 'Click{0}:{1}'.format(desc,loc)
        self.find_element(*loc).click()

    @property
    def assertSuccess(self):
        """断言,消费成功"""
        print '断言:返回到次卡消费初始页'
        self.getImage
        return self.isOrNoExist(*(self.number_phone_Loc))