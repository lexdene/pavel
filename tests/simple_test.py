import unittest
import pavel

import test_helper


class CalcTestCase(unittest.TestCase):
    def testDemo(self):
        self.assertEqual(1, 1)

    def testCalc(self):
        result = test_helper.execute_file('calc')
        self.assertEqual(result, 23)


class VariableTestCase(unittest.TestCase):
    def testVariable(self):
        result = test_helper.execute_file('variable')
        self.assertEqual(result, 38)
