import unittest
import pavel

from tests import test_helper


class CalcTestCase(unittest.TestCase):
    def testDemo(self):
        self.assertEqual(1, 1)

    def testCalc(self):
        result, scope = test_helper.execute_file('calc')
        self.assertEqual(result, 23)

    def testNonAssocCompOperator(self):
        self.assertRaises(
            ValueError,
            test_helper.execute_file,
            'non_assoc_comp_operator'
        )

    def testKeywordOperator(self):
        result, scope = test_helper.execute_file('keyword_operator')
        self.assertEqual(result, 30)
        self.assertEqual(scope['r'], 30)
        self.assertEqual(scope['s'], 41)


class VariableTestCase(unittest.TestCase):
    def testVariable(self):
        result, scope = test_helper.execute_file('variable')
        self.assertEqual(result, 22)


class ConditionTestCase(unittest.TestCase):
    def testSimpleIf(self):
        result, scope = test_helper.execute_file('simple_if')

        self.assertEqual(scope['a'], 3)
        self.assertEqual(scope['b'], 1)
        self.assertEqual('c' in scope, False)

    def testIfWithElse(self):
        result, scope = test_helper.execute_file('if_with_else')

        self.assertEqual(scope['a'], 3)
        self.assertEqual(scope['b'], 2)

    def testAllIf(self):
        result, scope = test_helper.execute_file('if')


class LoopTestCase(unittest.TestCase):
    def testSimpleWhileLoop(self):
        result, scope = test_helper.execute_file('simple_while_loop')
        self.assertEqual(result, 10)

        self.assertEqual(scope['i'], 10)
        self.assertEqual(scope['sum'], 55)

    def testSimpleForLoop(self):
        result, scope = test_helper.execute_file('simple_for_loop')
        self.assertEqual(result, 45)

        self.assertEqual(scope['i'], 9)
        self.assertEqual(scope['sum'], 45)


class FunctionTestCase(unittest.TestCase):
    def testSimpleFunction(self):
        result, scope = test_helper.execute_file('simple_function')
        self.assertEqual(result, 210)

        self.assertEqual(scope['i'], 500)
        self.assertEqual(scope['a'], 55)
        self.assertEqual(scope['b'], 530)
        self.assertEqual(scope['c'], 1030)

    def testAnonymousFunction(self):
        result, scope = test_helper.execute_file('anonymous_function')
        self.assertEqual(result, 121)

    def testNoArgFunction(self):
        result, scope = test_helper.execute_file('no_param_function')
        self.assertEqual(result, 0)

    def testFunctionScope(self):
        result, scope = test_helper.execute_file('function_scope')
        self.assertEqual(result, 0)


class ObjectTestCase(unittest.TestCase):
    def testSimpleObject(self):
        result, scope = test_helper.execute_file('simple_object')
        self.assertEqual(result, 20)

        self.assertEqual(scope['a'], 1)
        self.assertEqual(scope['b'], 10)
        self.assertEqual(scope['c'], 20)

    def testAttrAndItem(self):
        result, scope = test_helper.execute_file('object_attr_and_item')

        self.assertEqual(scope['a'], 1)
        self.assertEqual(scope['b'], 10)
        self.assertEqual(scope['c'], 1)
        self.assertEqual(scope['d'], 10)

    def testMemberFunction(self):
        result, scope = test_helper.execute_file('simple_member_function')
        self.assertEqual(result, 10)

        self.assertEqual(scope['a'], 10)


class DelegatorTestCase(unittest.TestCase):
    def testDelegatorObject(self):
        result, scope = test_helper.execute_file('delegator_object')
        self.assertEqual(result, 20)

        self.assertEqual(scope['r1'], 20)
        self.assertEqual(scope['r2'], 90)
        self.assertEqual(scope['r3'], 90)

    def testSimpleSuper(self):
        result, scope = test_helper.execute_file('simple_super')

        self.assertEqual(scope['r1'], 10)
        self.assertEqual(scope['r2'], 90)
        self.assertEqual(scope['r3'], 90)
