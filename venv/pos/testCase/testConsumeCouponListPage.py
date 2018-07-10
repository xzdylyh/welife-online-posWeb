#coding=utf-8
from selenium import webdriver
from pos.pages import consumeCouponListPage
import unittest,ddt,os
from pos.lib import scripts
from pos.lib import gl,HTMLTESTRunnerCN

shopCancelData = [{"desc":u"券包+次卡+直接购买","title":u"商品售卖流水 - 微生活POS系统"}]

@ddt.ddt
class TestConsumeCouponListPage(unittest.TestCase):
    """交易流水模块"""
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.url = 'http://pos.beta.acewill.net/consume/couponlist'



    @unittest.skipIf(scripts.getRunFlag('CONSUMECOUPONLIST',('testCase1'))=='N','验证执行配置')
    @ddt.data(*shopCancelData)
    def testCase1(self,data):
        """交易流水-撤销商品售卖"""
        print '功能:{0}'.format(data['desc'])

        self.undo = consumeCouponListPage.ConsumeCouponListPage(self.url,self.driver,data['title'])
        self.undo.open #打开目标url

        """商品售卖,撤销"""
        self.undo.clickBtn('撤销',*(self.undo.coupon_undoLink_loc))
        self.undo.clickBtn('确认',*(self.undo.coupon_confirmBtn_loc))
        self.undo.wait(3000)

        """后置断言操作"""
        self.assertTrue(self.undo.assertSuccess)
        self.assertEqual(self.undo.find_element(
            *(self.undo.coupon_assert_loc)).text,'撤销商品售卖')



    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()




if __name__=="__main__":

    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestConsumeCouponListPage)]
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