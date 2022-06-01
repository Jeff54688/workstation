#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from unitpad import Count


class TestDemo(unittest.TestCase):
    """Test mathfuc.py"""

    @classmethod       #指定下面方法为类方法
    def setUpClass(cls):        #所有case执行的前置条件，只运行一次
        print ("this setupclass() method only called once\n")

    @classmethod                #所有case运行完后只运行一次
    def tearDownClass(cls):
        print ("this teardownclass() method only called once too\n")

    def setUp(self):            #准备环境，执行每个测试用例的的前置条件
        print ("do something before test : prepare environment\n")

    def tearDown(self):         #环境还原，执行每个测试用例的后置条件
        print ("do something after test : clean up\n")

    def test_add(self):         #test_被测函数
        """Test method add(a, b)"""
        self.assertEqual(3, Count().add(1, 2))       
        self.assertNotEqual(3, Count().add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        self.assertEqual(1, Count().minus(3, 2))
        self.assertNotEqual(1, Count().minus(3, 2))



if __name__ == '__main__':
    # verbosity=*：默认是1；设为0，则不输出每一个用例的执行结果；2-输出详细的执行结果
    unittest.main(verbosity=1)