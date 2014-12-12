import unittest
import pavel

from tests import test_helper


class CalcTestCase(unittest.TestCase):
    def testDemo(self):
        self.assertEqual(1, 1)

    def testCalc(self):
        result, env = test_helper.execute_file('calc')
        self.assertEqual(result, 23)

    def testNonAssocCompOperator(self):
        self.assertRaises(
            ValueError,
            test_helper.execute_file,
            'non_assoc_comp_operator'
        )

    def testKeywordOperator(self):
        result, env = test_helper.execute_file('keyword_operator')
        self.assertEqual(result, 30)
        self.assertEqual(env['r'], 30)


class VariableTestCase(unittest.TestCase):
    def testVariable(self):
        result, env = test_helper.execute_file('variable')
        self.assertEqual(result, 22)


class ConditionTestCase(unittest.TestCase):
    def testSimpleIf(self):
        result, env = test_helper.execute_file('simple_if')

        self.assertEqual(env['a'], 3)
        self.assertEqual(env['b'], 1)
        self.assertEqual('c' in env, False)

    def testIfWithElse(self):
        result, env = test_helper.execute_file('if_with_else')

        self.assertEqual(env['a'], 3)
        self.assertEqual(env['b'], 2)

    def testAllIf(self):
        result, env = test_helper.execute_file('if')


class LoopTestCase(unittest.TestCase):
    def testSimpleWhileLoop(self):
        result, env = test_helper.execute_file('simple_while_loop')
        self.assertEqual(result, 10)

        self.assertEqual(env['i'], 10)
        self.assertEqual(env['sum'], 55)

    def testSimpleForLoop(self):
        result, env = test_helper.execute_file('simple_for_loop')
        self.assertEqual(result, 45)

        self.assertEqual(env['i'], 9)
        self.assertEqual(env['sum'], 45)


class FunctionTestCase(unittest.TestCase):
    def testSimpleFunction(self):
        result, env = test_helper.execute_file('simple_function')
        self.assertEqual(result, 210)

        self.assertEqual(env['i'], 500)
        self.assertEqual(env['a'], 55)
        self.assertEqual(env['b'], 530)
        self.assertEqual(env['c'], 1030)

    def testAnonymousFunction(self):
        result, env = test_helper.execute_file('anonymous_function')
        self.assertEqual(result, 121)

    def testNoArgFunction(self):
        result, env = test_helper.execute_file('no_param_function')
        self.assertEqual(result, 0)

    def testFunctionScope(self):
        result, env = test_helper.execute_file('function_scope')
        self.assertEqual(result, 0)


class ObjectTestCase(unittest.TestCase):
    def testSimpleObject(self):
        result, env = test_helper.execute_file('simple_object')
        self.assertEqual(result, 20)

        self.assertEqual(env['a'], 1)
        self.assertEqual(env['b'], 10)
        self.assertEqual(env['c'], 20)

    def testMemberFunction(self):
        result, env = test_helper.execute_file('simple_member_function')
        self.assertEqual(result, 10)

        self.assertEqual(env['a'], 10)
