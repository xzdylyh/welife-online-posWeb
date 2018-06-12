#coding=utf-8
from selenium import webdriver
from pos.pages import consumePage
import unittest,ddt,os
from pos.lib import gl,HTMLTESTRunnerCN

testData = [{"phoneOrCard":"13718651997","desc":'''手机号'''},
            {"phoneOrCard":"1003935039186461","desc":"卡号"}]

consumeData = [{"phoneOrCard":"1003935039186461","tcTotalFee":1,"tcStoredPay":1,"credit":1,"dualCode":"000000","desc":u"积分消费"}]

chargeDealData=[{"tcTotalFee":1,"desc":u"储值卡消费","phoneOrCard":"1003935039186461","dualCode":"000000"}]
custCouponData = [{"tcTotalFee":1,"desc":u"现金券消费","phoneOrCard":"1003935039186461","dualCode":"000000"}]


tmpData = [{"phoneOrCard":"1003935039186461","tcTotalFee":1,"credit":1,"dualCode":"000000","type":1,"desc":u"储值消费"},
           {"phoneOrCard": "1003935039186461", "tcTotalFee": 1, "credit": 1, "dualCode": "000000", "type": 2,"desc": u"积分消费"},
           {"phoneOrCard": "1003935039186461", "tcTotalFee": 1, "credit": 1, "dualCode": "000000", "type": 3,"desc": u"券消费"}
           ]

@ddt.ddt
class TestConsumePage(unittest.TestCase):
    '''消费模块'''
    @classmethod
    def setUpClass(cls):
        #cls.driver = webdriver.Firefox()
        cls.driver = webdriver.Firefox()
        cls.url = 'http://pos.beta.acewill.net/consume'
        #cookies 免登录，有效期一天。
        cls.cookinfo = {"pos_entry_number":"1003935039186461",
               "pos_entry_actualcard":"1003935039186461",
               "pos_bid":"2048695606",
               "pos_mid":"1155134323",
               "pos_sid":"1512995661",
               "pos_sign":"0bf7da4d84df8a8f01425d9fb58da120"}

    def consume_func(self,data):
        '''消费->输入卡号或手机号->确定'''
        self.consume = consumePage.ConsumePage(self.url, self.driver, '消费 - 微生活POS系统')

        # 打开浏览器，并转到消费页
        self.consume.open(ck_dict=self.cookinfo)
        # 选择会员卡号/手机号
        self.consume.selectTab(*(self.consume.selectCardNo_loc))
        # 输入卡号或手机号
        self.consume.inputText(data['phoneOrCard'], *(self.consume.inputCardorPhone_loc))
        # 点击确定按钮
        self.consume.clickBtn(*(self.consume.confirmBtn_loc))

    def iterCoupon(self):
        '''动态选择券'''
        couponDiv = self.driver.find_elements_by_class_name('ticket-wrapper') #现金券
        for e in couponDiv:
            divEle = e.find_element_by_xpath("//div[@class='ticket']")
            if divEle.is_displayed():
                    divEle.click()#单击
                    break

    @unittest.skip('测试其它case临时跳过')
    @ddt.data(*testData)
    def testCase1(self,data):
        '''根据手机号或卡号查询消费'''
        print u"根据{0}查询消费".format(data['desc'])
        self.consume_func(data)
        #断言
        self.assertTrue(self.consume.assertCustom,msg='消费->确定->未找到手机号')


    @ddt.data(*consumeData)
    def testCase2(self,data):
        '''积分消费'''
        print u'功能:{0},消费{1}元,抵扣{2}积分.'.format(data['desc'],data['tcTotalFee'],data['credit'])
        self.consume_func(data) #进入消费页
        self.consume.inputText(data['tcTotalFee'],*(self.consume.tcTotalFee_loc)) #输入金额
        self.consume.clearInputText(*(self.consume.tcStoredPay_loc)) #清除储值支付
        self.consume.inputText(data['credit'],*(self.consume.tcUseCredit_loc)) #使用积分
        self.consume.inputText(data['desc'],*(self.consume.note_loc)) #输入备注

        self.consume.clickBtn(*(self.consume.showSubmit_loc)) #确认消费按钮
        self.consume.clickBtn(*(self.consume.confirm_consume_loc)) #最终确认消费

        '''输入密码点击确认'''
        self.consume.isExistAndInput(data['dualCode'],*(self.consume.pay_pwd))
        self.consume.isExistAndClick(*(self.consume.pay_pwd_confirm))

        self.consume.assertPaySuccess #支付成功断言


    @ddt.data(*chargeDealData)
    def testCase3(self,data):
        '''储值销费'''
        print u'功能:{0},消费金额{1},储值抵扣{2}元.'.format(data['desc'],data['tcTotalFee'],data['tcTotalFee'])
        self.consume_func(data) #进入消费页
        self.consume.inputText(data['tcTotalFee'],*(self.consume.tcTotalFee_loc)) #输入金额

        self.consume.inputText(data['desc'],*(self.consume.note_loc)) #输入备注
        self.consume.clickBtn(*(self.consume.showSubmit_loc)) #确认消费按钮
        self.consume.clickBtn(*(self.consume.confirm_consume_loc)) #最终确认消费

        '''输入密码点击确认'''
        self.consume.isExistAndInput(data['dualCode'],*(self.consume.pay_pwd))
        self.consume.isExistAndClick(*(self.consume.pay_pwd_confirm))

        self.consume.assertPaySuccess #支付成功断言

    @unittest.skip('a')
    @ddt.data(*custCouponData)
    def testCase4(self,data):
        '''现金券消费'''
        self.consume_func(data)  # 进入消费页
        self.consume.inputText(data['tcTotalFee'], *(self.consume.tcTotalFee_loc))  # 输入金额
        self.iterCoupon()#选择现金券

        self.consume.inputText(data['desc'], *(self.consume.note_loc))  # 输入备注
        self.consume.clickBtn(*(self.consume.showSubmit_loc))  # 确认消费按钮
        self.consume.clickBtn(*(self.consume.confirm_consume_loc))  # 最终确认消费

        '''输入密码点击确认'''
        self.consume.isExistAndInput(data['dualCode'],*(self.consume.pay_pwd))
        self.consume.isExistAndClick(*(self.consume.pay_pwd_confirm))

        self.consume.assertPaySuccess #支付成功断言


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestConsumePage)]
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
