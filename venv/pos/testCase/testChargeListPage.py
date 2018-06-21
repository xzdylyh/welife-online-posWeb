#coding=utf-8
from selenium import webdriver
from pos.pages import chargeListPage
import unittest,ddt,os
from pos.lib import scripts
from pos.lib import gl,HTMLTESTRunnerCN

chargeData = [{"desc": u"充值撤销正常流程", "pageTitle": u"充值流水 - 微生活POS系统"}]

@ddt.ddt
class TestChargeListPage(unittest.TestCase):
    """交易流水模块-充值"""
    @classmethod
    def setUpClass(cls):
        cls.option = webdriver.ChromeOptions()
        cls.option.add_argument('disable-infobars') #不显示"Chrome正在受自动测试软件控制"
        #cls.option.add_argument('headless') #后台运行,不显示界面
        cls.driver = webdriver.Chrome(chrome_options=cls.option)
        cls.url = 'http://pos.beta.acewill.net/charge/listcharge'

    @unittest.skipIf(scripts.getRunFlag('CHARGELIST', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*chargeData)
    def testCase1(self,data):
        """充值撤销"""
        print '功能:{0}'.format(data['desc'])
        self.charge = chargeListPage.ChargeListPage(self.url,self.driver,data['pageTitle'])
        self.charge.open #打开目标页
        self.charge.clickBtn('充值撤销',*(self.charge.charge_undoLink_loc))
        self.charge.clickBtn('确定',*(self.charge.charge_confirmBtn_loc))
        """断言"""
        self.assertTrue(self.charge.assertUndoSuccess,msg='储值撤销失败,请检查状态.')
        txt = self.driver.find_element(*(self.charge.charge_undoStatus_loc)).text
        print '充值撤销状态:{0}'.format(txt)
        self.assertEqual(txt,u'撤销充值',msg='撤销充值记录列表中,不存在状态为<撤销充值>的记录')


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()




if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestChargeListPage)]
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
