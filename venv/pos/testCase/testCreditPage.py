#coding=utf-8
from selenium import webdriver
from pos.pages import creditPage
import unittest,ddt,os
from pos.lib import gl,HTMLTESTRunnerCN

creditData = [{"charge_number":"1003935039186461","ExchangeNumber":1,"ExchangeDetail":u"自动化测试大礼包1个"}]

@ddt.ddt
class TestCreditPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.url = 'http://pos.beta.acewill.net/credit'
        #cookies 免登录，有效期一天。
        cls.cookinfo = {"pos_entry_number":"1003935039186461",
               "pos_entry_actualcard":"1003935039186461",
               "pos_bid":"2048695606",
               "pos_mid":"1155134323",
               "pos_sid":"1512995661",
               "pos_sign":"0bf7da4d84df8a8f01425d9fb58da120"}

    def creditFunc(self,data):
        print '查询方式:{0}'.format(data['charge_number'])
        self.credit = creditPage.CreditPage(self.url,self.driver,u"积分换礼 - 微生活POS系统")
        self.credit.open(ck_dict=self.cookinfo) #增加cookies信息,并打开积分换礼页

        self.credit.selectTab(*(self.credit.creditTab_loc)) #选择tab
        self.credit.inputText(data['charge_number'],*(self.credit.charge_number_loc)) #输入手机号或卡号
        self.credit.clickBtn(*(self.credit.creditBtn_loc)) #确定按钮



    @ddt.data(*creditData)
    def testCase1(self,data):
        '''积分换礼:'''
        print '\r扣减积分:{0}\r'.format(data['ExchangeNumber'])
        print '兑换礼品详情:{0}'.format(data['ExchangeDetail'])
        self.creditFunc(data) #输入手机号,或卡号,进入积分换礼页面
        self.credit.inputText(data['ExchangeNumber'],*(self.credit.inputExchangeNumber_loc)) #输入扣减积分数量
        self.credit.inputText(data['ExchangeDetail'],*(self.credit.inputExchangeDetail_loc)) #兑换礼品详情
        self.credit.clickBtn(*(self.credit.sendMessageBtn_loc)) #确定按钮

        self.credit.assertPaySuccess #成功兑换断言

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()




if __name__=="__main__":
    suite = unittest.TestSuite()
    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCreditPage)]
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
