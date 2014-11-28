import unittest
import pavel

from tests import test_helper


class CalcTestCase(unittest.TestCase):
    def testDemo(self):
        self.assertEqual(1, 1)

    def testCalc(self):
        result, env = test_helper.execute_file('calc')
        self.assertEqual(result, 23)


class VariableTestCase(unittest.TestCase):
    def testVariable(self):
        result, env = test_helper.execute_file('variable')
        self.assertEqual(result, 22)


class ConditionTestCase(unittest.TestCase):
    def testSimpleIf(self):
        result, env = test_helper.execute_file('simple_if')

        block = env.current_block()
        self.assertEqual(block.get_variable('a'), 3)
        self.assertEqual(block.get_variable('b'), 1)
        self.assertEqual(block.contains_variable('c'), False)

    def testIfWithElse(self):
        result, env = test_helper.execute_file('if_with_else')

        block = env.current_block()
        self.assertEqual(block.get_variable('a'), 3)
        self.assertEqual(block.get_variable('b'), 2)

    def testAllIf(self):
        result, env = test_helper.execute_file('if')
