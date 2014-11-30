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


class LoopTestCase(unittest.TestCase):
    def testSimpleWhileLoop(self):
        result, env = test_helper.execute_file('simple_while_loop')
        self.assertEqual(result, 10)

        block = env.current_block()
        self.assertEqual(block.get_variable('i'), 10)
        self.assertEqual(block.get_variable('sum'), 55)


class FunctionTestCase(unittest.TestCase):
    def testSimpleFunction(self):
        result, env = test_helper.execute_file('simple_function')
        self.assertEqual(result, 210)

        block = env.current_block()

        self.assertEqual(block.get_variable('i'), 500)
        self.assertEqual(block.get_variable('a'), 55)
        self.assertEqual(block.get_variable('b'), 530)
        self.assertEqual(block.get_variable('c'), 1030)
