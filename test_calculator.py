import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        from calculator_class import SimpleCalculator
        self.simple_calculator = SimpleCalculator()

    def test_addition(self):
        expression = '58+23'
        expected_result = 81
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_subtraction(self):
        expression = '245-699'
        expected_result = -454
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_multiplication(self):
        expression = '45*145'
        expected_result = 6525
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_division(self):
        expression = '56789/678'
        expected_result = 83.75958702064896
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_exponentiation(self):
        expression = '4^5'
        expected_result = 1024
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_floats1(self):
        expression = '5.78/3.2'
        expected_result = 1.80625
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_floats2(self):
        expression = '45.3*3.9-7.6+(4.5-2)'
        expected_result = 171.57
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_brackets(self):
        expression = '(45+6)*5+3/(2+1)'
        expected_result = 256
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def unary_minus(self):
        expression = '-45*(-45)'
        expected_result = 2025
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_big_expression1(self):
        expression = '(9+8)*3+(-6)'
        expected_result = 45
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_big_expression2(self):
        expression = '(456-3)*5+45/6'
        expected_result = 2272.5
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_big_expression3(self):
        expression = '(456*4)-(4+3)*4+3^3'
        expected_result = 1823
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)

    def test_big_expression4(self):
        expression = '(-456*4)-(-5+3)*4'
        expected_result = -1816
        result = self.simple_calculator.process_calculation_query(expression)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
