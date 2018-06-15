#coding=utf-8
from selenium import webdriver
from pos.pages import chargePage
import unittest,ddt,os,time
from pos.lib import scripts
from pos.lib import gl,HTMLTESTRunnerCN

chargeData = [{"charge_number":"1003935039186461","present":2,"note":u"自动化测试充值","desc":u"储值正常流程"}]


@ddt.ddt
class TestChargePage(unittest.TestCase):
    '''储值模块'''

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.url = 'http://pos.beta.acewill.net/charge/index'
        cls.cookinfo = {"pos_entry_number":"1003935039186461",
               "pos_entry_actualcard":"1003935039186461",
               "pos_bid":"2048695606",
               "pos_mid":"1234871385",
               "pos_sid":"1512995661",
               "pos_sign":"369240630d5e17a24bf7e5a70f073465"}


    def inChargePage(self,data):
        self.charge = chargePage.ChargePage(self.url,self.driver,'充值 - 微生活POS系统')
        self.charge.open(ck_dict=self.cookinfo)
        """输入卡号，确定，进入储值页面"""
        self.charge.inputText(data['charge_number'],'输入会员卡号或手机号',*(self.charge.charge_number_loc))
        self.charge.clickBtn('确定',*(self.charge.confirmBtn_loc))
        """断言"""
        self.assertTrue(self.charge.find_element(*(self.charge.chargeRMB_loc))) #储值余额
        self.usChargeSaving = self.driver.find_element(*(self.charge.chargeRMB_loc)).text[:-1]
        print '当前余额:{0}'.format(self.usChargeSaving[:-1])

    #@unittest.skip('a')
    @ddt.data(*chargeData)
    def testCase1(self,data):
        """储值"""
        print '功能:{0}'.format(data['desc'])
        """输入卡号或手机号，确定，进入储值页面"""
        self.inChargePage(data)
        """储值操作"""
        self.charge.clickBtn('选择储值奖励规则',*(self.charge.chargeGZ_loc))
        self.charge.clickBtn('自定义规则',*(self.charge.coustomGZ_loc))
        self.charge.inputText(data['present'],'自定义金额',*(self.charge.present_loc))
        self.charge.clickBtn('确定',*(self.charge.customBtn_loc))
        self.charge.clickBtn('现金',*(self.charge.payType_loc))
        self.charge.inputText(data['note'],'备注',*(self.charge.noteRemark_loc))
        self.charge.clickBtn('确定',*(self.charge.chargeSubmit_loc))
        self.charge.clickBtn('确认',*(self.charge.chargesBtn_loc))
        """断言操作"""
        self.charge.assertChargeSuccess
        """后置操作"""
        self.charge.clickBtn('立即消费',*(self.charge.consumeBtn_loc))
        time.sleep(3)
        """断言储值余额，是否正确"""
        self.usDualSaving = self.driver.find_element(*(self.charge.usSaving_loc)).text
        print '储值后当前余额:{0}'.format(self.usDualSaving)
        self.assertTrue(float(data['present']) + float(self.usChargeSaving) ==float(self.usDualSaving))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__=="__main__":

    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestChargePage)]
    suite.addTests(tests)
    filePath = os.path.join(gl.reportPath, 'Report.html')  # 确定生成报告的路径
    print filePath

    with file(filePath, 'wb') as fp:
        runner = HTMLTESTRunnerCN.HTMLTestRunner(
            stream=fp,
            title=u'UI自动化测试报告',
            description=u'详细测试用例结果',  # 不传默认为空
            tester=u"yhleng"  # 测试人员名字，不传默认为小强
        )
        # 运行测试用例
        runner.run(suite)
        fp.close()
