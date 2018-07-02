#coding=utf-8
from selenium import webdriver
from pos.pages import consumePage
import unittest,ddt,os
from pos.lib.excel import Excel
from pos.lib import scripts
from pos.lib import gl,HTMLTESTRunnerCN
import time,json

consumeData = [{"phoneOrCard":"1003935039186461","desc":u"积分消费","tcTotalFee":1,"tcStoredPay":1,"credit":1,"dualCode":"000000"}]
chargeDealData=[{"tcTotalFee":1,"desc":u"储值卡消费","phoneOrCard":"1003935039186461","dualCode":"000000"}]
custCouponData = [{"tcTotalFee":1,"desc":u"券消费","phoneOrCard":"1003935039186461","dualCode":"000000"}]
cardData = [{"PhoneNo":"13712345676","desc":u"实体卡开卡",'username':'yhleng','birthday':'1985-03-21','password':'000000'}]
cardBindData = [{"PhoneNo": "13712345678","desc":u"绑卡正常流程"}]
cardofData = [{"desc":u"次卡开卡"}]

@ddt.ddt
class TestConsumePage(unittest.TestCase):
    '''消费模块'''
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.url = 'http://pos.beta.acewill.net/consume'
        cls.excel = Excel(os.path.join(gl.dataPath, 'posCardData.xls').decode('utf-8'))
        cls.toexcel = Excel(os.path.join(gl.dataPath, 'posNotNameCardData.xls').decode('utf-8'))

    def consume_func(self,data):
        '''消费->输入卡号或手机号->确定'''
        self.consume = consumePage.ConsumePage(self.url, self.driver, '消费 - 微生活POS系统')

        # 打开浏览器，并转到消费页
        self.consume.open
        # 选择会员卡号/手机号
        self.consume.selectTab(*(self.consume.selectCardNo_loc))
        # 输入卡号或手机号
        self.consume.inputText(data['phoneOrCard'], *(self.consume.inputCardorPhone_loc))
        # 点击确定按钮
        self.consume.clickBtn(*(self.consume.confirmBtn_loc))


    """消费模块，动态选择券"""
    def iterCoupon(self):
        '''动态选择券'''
        couponDiv = self.driver.find_elements_by_class_name(self.consume.couponDiv_loc) #现金券
        for e in couponDiv:
            divEle = e.find_element_by_xpath(self.consume.ticket_loc)
            if divEle.is_displayed():
                divEle.click()  # 单击
                useCount = self.driver.find_element_by_name(self.consume.useCount)
                if useCount.is_displayed():
                    useCount.send_keys(1)
                    break


    def getCode(self,data):
        """
        从Boss获取验证码
        :param data: 参数化数据
        :return: 验证码
        """
        """参数变量url,cookies,time"""
        yamldict = scripts.getYamlfield(os.path.join(gl.configPath, 'config.yaml'))
        cookies= yamldict['CONFIG']['Cookies']['BossLoginCookies']
        #timeStr = time.strftime('%Y-%m-%d')
        url = 'http://boss.beta.acewill.net/sms/search?phone={0}&begin={1}&end={2}'.format(data['PhoneNo'], gl.curDate, gl.curDate)

        """设置浏览器,选项,隐藏获窗口运行"""
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars') #不显示"Chrome正在受自动测试软件控制"
        option.add_argument('headless') #后台运行,不显示界面

        """启动浏览器,增加cookies"""
        driver1 = webdriver.Chrome(chrome_options=option)
        driver1.maximize_window()
        driver1.get(url)
        driver1.implicitly_wait(30)
        driver1.add_cookie(cookies)
        driver1.get(url)

        """获取验证码,并返回验证码"""
        txtcode = driver1.find_element_by_xpath(self.consume.boss_code_xpath).text
        code = json.loads(txtcode)['template']['yanzhengma']
        driver1.quit()
        return code


    @unittest.skipIf(scripts.getRunFlag('CONSUME',('testCase1'))=='N','验证执行配置')
    @ddt.data(*cardData)
    def testCase1(self,data):
        '''实体卡开卡'''
        print '功能：{0}'.format(data['desc'])
        cardNo = {'phoneOrCard':str(self.excel.getCardNo())} #获取卡号
        print u"实体卡，卡号为：{0}".format(cardNo['phoneOrCard'])
        self.consume_func(cardNo)
        self.consume.clickBtn(*(self.consume.openCard_loc)) #实体卡开卡
        self.consume.inputText(data['PhoneNo'],*(self.consume.phoneNo_loc)) #输入手机号
        self.consume.inputText(data['username'],*(self.consume.username_loc)) #姓名
        self.consume.clickBtn(*(self.consume.sex_loc)) #性别
        self.consume.inputText(data['birthday'],*(self.consume.birthday_loc)) #生日
        self.consume.inputText(data['password'],*(self.consume.password_loc)) #交易密码
        self.consume.clickBtn(*(self.consume.cardConfirmBtn_loc)) #确定

        #断言
        self.assertTrue(self.consume.assertCardSuccess)



    @unittest.skipIf(scripts.getRunFlag('CONSUME',('testCase6'))=='N','验证执行配置')
    @ddt.data(*cardofData)
    def testCase6(self,data):
        """不记名卡开卡"""
        print '功能：{0}'.format(data['desc'])

        cardNo = {'phoneOrCard':str(self.toexcel.getCardNo(cell_col=0))} #获取磁道号
        print cardNo
        self.consume_func(cardNo)

        """开卡页面"""
        self.consume.clickBtn(*(self.consume.cardOfOpenBtn_loc)) #开卡页面,确定按钮

        """断言操作"""
        self.assertTrue(self.consume.assertOpenCardSuccess)


    @unittest.skipIf(scripts.getRunFlag('CONSUME','testCase5')=='N','验证执行配置')
    @ddt.data(*cardBindData)
    def testCase5(self,data):
        """实体卡绑卡"""
        print '功能：{0}'.format(data['desc'])
        cardNo = {'phoneOrCard': str(self.excel.getCardNo())}  # 获取卡号
        print u"实体卡，卡号为：{0}".format(cardNo['phoneOrCard'])
        self.consume_func(cardNo)
        self.consume.clickBtn(*(self.consume.cardBind_loc)) #绑卡按钮
        self.consume.inputText(data['PhoneNo'],*(self.consume.cardPhone_loc)) #输入卡号
        self.consume.clickBtn(*(self.consume.cardBindBtn_loc)) #确定
        code = self.getCode(data)  #获取验证码
        print '验证码:{0}'.format(code)
        self.consume.inputText(code,*(self.consume.code_loc)) #输入验证码
        self.consume.clickBtn(*(self.consume.codeBtn_loc)) #验证码确认

        """断言"""
        self.assertTrue(self.consume.assertCardSuccess, msg='实体卡绑定失败')



    @unittest.skipIf(scripts.getRunFlag('CONSUME','testCase2')=='N','验证执行配置')
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

    @unittest.skipIf(scripts.getRunFlag('CONSUME', 'testCase3') == 'N', '验证执行配置')
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

    @unittest.skipIf(scripts.getRunFlag('CONSUME', 'testCase4') == 'N', '验证执行配置')
    @ddt.data(*custCouponData)
    def testCase4(self,data):
        '''券消费'''
        print u'功能:{0},消费{1}积分.'.format(data['desc'], data['tcTotalFee'])
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
