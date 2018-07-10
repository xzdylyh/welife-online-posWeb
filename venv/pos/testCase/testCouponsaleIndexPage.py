#coding=utf-8
from selenium import webdriver
from pos.pages import couponsaleIndexPage
import unittest,ddt,os
from pos.lib import scripts
from pos.lib import gl,HTMLTESTRunnerCN

shopData = [{"phoneOrCard":"13712345678","iterInput":[1,1],"desc":u"券包+次卡+直接购买","title":u"商品售卖 - 微生活POS系统"}]

@ddt.ddt
class TestCouponsaleIndexPage(unittest.TestCase):
    """商品售卖模块"""
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.url = 'http://pos.beta.acewill.net/couponsale/index'



    @unittest.skipIf(scripts.getRunFlag('COUPONSALEINDEX',('testCase1'))=='N','验证执行配置')
    @ddt.data(*shopData)
    def testCase1(self,data):
        """商品售卖-券包+次卡+直接购买"""
        print '功能:{0}'.format(data['desc'])

        self.shop = couponsaleIndexPage.CouponsaleIndexPage(self.url,self.driver,data['title'])
        self.shop.open #打开目标url

        """输入会员卡号,或手机号页"""
        self.shop.inputText(data['phoneOrCard'],'手机号或卡号',*(self.shop.shop_phone_loc))
        self.shop.clickBtn('确定',*(self.shop.shop_phoneBtn_loc))

        """商品售卖页"""
        self.shop.iterClick(*(self.shop.shop_select_loc))
        self.shop.clickBtn('确认',*(self.shop.shop_confirmBtn_loc))

        """后置断言操作"""
        self.assertTrue(self.shop.assertShopSuccess,msg='断言售卖成功后,返回到输入卡号或手机号页面')



    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()




if __name__=="__main__":

    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCouponsaleIndexPage)]
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