# coding=utf-8
import unittest
from BeautifulReport import BeautifulReport
from pos.lib import gl



def add_case(case_path=gl.casePath, rule="test*.py"):
    '''加载所有的测试用例'''
    discover = unittest.defaultTestLoader.discover(case_path,
                                                  pattern=rule,
                                                  top_level_dir=None)
    return discover


def run(test_suit):
    result = BeautifulReport(test_suit)
    result.report(filename='report.html', description='测试deafult报告', log_path=gl.reportPath)

if __name__ == "__main__":
    # 用例集合
    cases = add_case()

    print(cases)
    for i in cases:
        print(i)
        run(i)