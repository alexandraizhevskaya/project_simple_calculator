from typing import Dict, Union
import logging
logging.basicConfig(level=logging.INFO)


class SimpleCalculator:

    def __init__(self) -> None:
        """
        Calculator class to perform simple arithmetic operations.

        It supports the following operations:
        -addition `+`
        -subtraction `-`
        -multiplication `*`
        -division `/`
        -exponentiation `^`
        It also can handle unary negation `-` and operation priorities
        marked with brackets `()`

        Calculator takes the input arithmetic expression, converts its
        infix notation to postfix one (reverse polish notation), calculates and
        returns the result
        Example of polish notation: `7+5*3` -> `7 5 3 * +`
        """
        # init dictionary with operations priorities
        self._operator_priorities = {'(': 0,
                                     '+': 1,
                                     '-': 1,
                                     '*': 2,
                                     '/': 2,
                                     '^': 3,
                                     '~': 4  # unary minus (special symbol to
                                     # avoid confusion
                                     }

    def get_priorities(self) -> Dict:
        """Get priorities dictionary"""
        return self._operator_priorities

    def get_polish_notation(self) -> str:
        """Convert infix notation to postfix one"""
        input_expression = input()
        return self.to_postfix_notation(input_expression)

    def to_postfix_notation(self, infix_notation: str) -> str:
        """Convert infix notation of arithmetic expression to postfix one
        This method implements sorting elements of the input string to create
        its postfix notation version.
        1) We create `postfix_notation` - output string and `stack` - stack
        to put operators
        2) All the elements of the input string are processed iteratively
        -If an element is a digit (float or int),
        it is put in the output string.
        -If the element is an operator it is put to the stack
        with consideration to its priority
        - Cases with brackets and unary minus are also considered
        3) All the elements in stack are put in the output string
        :param infix_notation: arithmetic expression in its infix notation
        :return the given arithmetic expression in its postfix notation"""

        # init output postfix notation string and stack
        postfix_notation = ""
        stack = []

        # process all the elements iteratively
        for i in range(len(infix_notation)):
            element = infix_notation[i]

            # consider dots (meaning its float) for correct float processing
            if element == '.':
                postfix_notation += element

            # process digits - they are put to output string
            if element.isdigit():
                if i != len(infix_notation) - 1 and \
                        (infix_notation[i + 1].isdigit() or
                         infix_notation[i + 1] == '.'):
                    postfix_notation += element
                else:
                    postfix_notation += element + " "

            # process opening and closing brackets to handle priorities
            elif element == '(':
                stack.append(element)
            elif element == ')':
                while len(stack) > 0 and stack[-1] != '(':
                    postfix_notation += stack.pop() + " "
                stack.pop()

            # process and put to the output string operators
            # considering priorities
            elif element in self._operator_priorities.keys():
                operator = element
                # unary negation
                if operator == '-' and \
                        (i == 0 or (i > 1 and infix_notation[i - 1] in
                                    self._operator_priorities.keys())):
                    operator = '~'
                # operator priorities
                while len(stack) > 0 and self._operator_priorities[stack[-1]] \
                        >= self._operator_priorities[operator]:
                    postfix_notation += stack.pop() + " "
                stack.append(operator)
        # push rest of operators from stack
        while stack:
            postfix_notation += stack.pop() + " "
        return postfix_notation.strip()

    @staticmethod
    def execute_operation(operator: str, x: float, y: float) \
            -> Union[float, str]:
        """Perform one arithmetic operation
        :param operator: binary operator, one of `+-*/^`
        :param x: first argument
        :param y: second argument
        :return: result of the arithmetic operation or `not supported`
        if operator is not correct
        """
        # addition
        if operator == '+':
            return x + y
        # subtraction
        elif operator == '-':
            return x - y
        # multiplication
        elif operator == '*':
            return x*y
        # division
        elif operator == '/':
            try:
                return x / y
            except ZeroDivisionError:
                return 'Zero division is not possible!'
        # exponentiation
        elif operator == '^':
            return x**y
        # if operation is not supported
        else:
            return 'the given operation is not supported:('

    def calculate(self, prefix_notation: str) -> Union[float, str]:
        """
        Calculate arithmetic expression in its polish notation
        :param prefix_notation: arithmetic expression in its prefix form
        :return: the result of calculation
        """

        # split to get tokens
        prefix_notation = prefix_notation.split()
        # print(prefix_notation)

        # init stack of calculation
        local = []

        # process all the elements iteratively
        for i in range(len(prefix_notation)):
            element = prefix_notation[i]

            # convert digits to float and put to stack
            if element.isdigit() or element.find('.') != -1:
                local.append(float(element))

            # process operators in accordance with their priority
            elif element in self._operator_priorities.keys():
                # take care of unary minus
                if element == '~':
                    if len(local) > 0:
                        last = local.pop()
                    else:
                        last = 0
                    local.append(self.execute_operation('-', 0, last))
                    continue
                # execute binary operation if the operand is not unary minus
                if len(local) > 0:
                    second = local.pop()
                else:
                    second = 0

                if len(local) > 0:
                    first = local.pop()
                else:
                    first = 0
                # add the result to stack and return the top element
                outcome = self.execute_operation(element, first, second)
                if isinstance(outcome, float):
                    local.append(outcome)
                else:
                    return outcome
        return local.pop()

    def process_calculation_query(self, query: str) -> float:
        """
        Calculate arithmetic expression given in infix notation
        -convert to polish notation
        -calculate expression
        :param query: arithmetic expression to calculate
        :return: the result of calculation
        """

        # to do: check correctness
        polish_notation = self.to_postfix_notation(query)
        print(f'Polish notation of the expression: {polish_notation}')
        result = self.calculate(polish_notation)
        return result


# calculator = SimpleCalculator()
# query_ = input()
# result_of_calculation = calculator.process_calculation_query(query_)
# print(f'Answer: {result_of_calculation}')
