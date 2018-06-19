#coding=utf-8
from selenium import webdriver
from pos.pages import chargePage
import unittest,ddt,os,time
from pos.lib import scripts
from pos.lib import gl,HTMLTESTRunnerCN

chargeData = [{"charge_number":"1003935039186461","present":2,"note":u"自动化测试充值","desc":u"储值正常流程"}]
FillData = [{"charge_number":"1003935039186461","present":2,"note":u"自动化测试充值","desc":u"储值并补开发票","txtName":"text"}]


@ddt.ddt
class TestChargePage(unittest.TestCase):
    '''储值模块'''

    @classmethod
    def setUpClass(cls):
        cls.option = webdriver.ChromeOptions()
        cls.option.add_argument('disable-infobars') #不显示"Chrome正在受自动测试软件控制"
        #cls.option.add_argument('headless') #后台运行,不显示界面
        cls.driver = webdriver.Chrome(chrome_options=cls.option)
        cls.url = 'http://pos.beta.acewill.net/charge/index'


    def inChargePage(self,data):
        """输入卡号进入储值页面"""
        self.charge = chargePage.ChargePage(self.url,self.driver,'充值 - 微生活POS系统')
        self.charge.open #打开目标url
        """输入卡号，确定，进入储值页面"""
        self.charge.inputText(data['charge_number'],'输入会员卡号或手机号',*(self.charge.charge_number_loc))
        self.charge.clickBtn('确定',*(self.charge.confirmBtn_loc))
        """断言"""
        self.assertTrue(self.charge.find_element(*(self.charge.chargeRMB_loc))) #储值余额
        self.usChargeSaving = self.driver.find_element(*(self.charge.chargeRMB_loc)).text[:-1]
        print '当前余额:{0}'.format(self.usChargeSaving[:-1])


    def chargeFunc(self,data):
        """储值功能操作"""
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



    @unittest.skipIf(scripts.getRunFlag('CHARGE', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*chargeData)
    def testCase1(self,data):
        """储值"""
        self.chargeFunc(data) #调用储值功能函数


    @unittest.skipIf(scripts.getRunFlag('CHARGE', 'testCase2') == 'N', '验证执行配置')
    @ddt.data(*FillData)
    def testCase2(self,data):
        """储值->补开发票"""
        self.chargeFunc(data) #调用储值功能函数
        """补开发票"""
        self.charge.clickBtn('补开发票',*(self.charge.toReceipt_loc))
        NotRMB = self.charge.getTagText(data['txtName'],*(self.charge.not_fill_RMB_loc)) #未开票金额
        self.charge.inputText(NotRMB,'开票金额',*(self.charge.fill_RMB_loc))
        self.charge.clickBtn('确定',*(self.charge.fillBtn_loc))
        """断言补开票成功"""
        self.charge.clickBtn('补开发票',*(self.charge.toReceipt_loc))
        time.sleep(1)
        notRMB = (self.charge.getTagText(data['txtName'],*(self.charge.not_fill_RMB_loc))).encode('utf-8') #未开票金额
        print '补开发票金额剩余:{0}'.format(notRMB)
        self.assertEqual(notRMB,'0.00',msg='开票余额,不为零.')


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
