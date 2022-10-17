import re
from typing import Dict, Union, List
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

        Calculator takes an  arithmetic expression as an input, converts its
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
        """
        Get priorities dictionary
        """
        return self._operator_priorities

    @staticmethod
    def validate_input(input_string: str) -> bool:
        """
        Validate input string
        :param input_string: string to validate
        :return: bool whether the provided string is correct or not
        """
        input_string = ''.join(input_string.split())
        if re.search(r"[^ \d.+\-*^/()]", input_string):
            return False
        else:
            return True

    def parse_string(self, input_string: str) -> str:
        """
        Parse input string correctly to get separate numbers and operators
        :param input_string: string to parse
        :return parsed elements
        """

        # init element
        output = ""

        # process string iteratively
        for idx, element in enumerate(input_string):

            # if digit or `.` (meaning it is float) -> put to string
            if element.isdigit() or \
                    (element == '.' and output.isdigit()):
                output += element
            # return number
            elif output:
                yield float(output)
                output = ""
            # return operator
            if element in self._operator_priorities.keys() or element in ")":
                # take care of unary negation -> `~`
                if element == '-' and \
                        (idx == 0 or (idx > 1 and input_string[idx - 1] in
                                      self._operator_priorities.keys())):
                    element = '~'
                yield element
        # return last number
        if output:
            yield float(output)

    def to_postfix_notation(self, infix_notation: str) \
            -> List[Union[float, str]]:
        """
        Convert infix notation of arithmetic expression to postfix one
        This method implements sorting elements of the input string to create
        its postfix notation version
        :param infix_notation: arithmetic expression in its infix notation
        :return the given arithmetic expression in its postfix notation
        """

        # init output postfix notation container
        # and stack
        postfix_notation = []
        stack = []

        # parse string and process elements
        for element in self.parse_string(infix_notation):

            # if number -> put it into output
            if isinstance(element, float):
                postfix_notation.append(element)

            # process opening and closing brackets to handle priorities
            # if element is opening bracket -> put it into stack
            elif element == '(':
                stack.append(element)

            # if element is closing bracket -> push all the elements
            # till opening bracket and put them into output
            # then push the opening bracket itself
            elif element == ')':
                while len(stack) > 0 and stack[-1] != '(':
                    postfix_notation.append(stack.pop())
                stack.pop()

            # process and put to the output string operators
            # considering priorities
            elif element in self._operator_priorities.keys():
                operator = element

                # if element is an operator -> put into output all
                # the operators which priorities are >= the given element
                # till the opening bracket or the end of stack
                while len(stack) > 0 and self._operator_priorities[stack[-1]] \
                        >= self._operator_priorities[operator]:
                    postfix_notation.append(stack.pop())
                stack.append(operator)

        # push rest of operators from stack
        while stack:
            postfix_notation.append(stack.pop())
        return postfix_notation

    @staticmethod
    def execute_operation(operator: str, x: float, y: float) \
            -> Union[float, str]:
        """
        Perform one arithmetic operation
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
            return x * y
        # division
        elif operator == '/':
            try:
                return x / y
            except ZeroDivisionError:
                return 'Zero division is not possible!'
        # exponentiation
        elif operator == '^':
            return x ** y
        # if operation is not supported
        else:
            return 'The given operation is not supported:('

    def calculate(self, prefix_notation: List[Union[float, str]]) \
            -> Union[float, str]:
        """
        Calculate arithmetic expression in its polish notation
        :param prefix_notation: arithmetic expression in its prefix form
        :return: the result of calculation
        """

        # init stack of calculation
        calculation_stack = []

        # process all the elements iteratively
        for idx in range(len(prefix_notation)):
            element = prefix_notation[idx]

            # if number -> put into stack
            if isinstance(element, float):
                calculation_stack.append(element)

            # if operator -> process in accordance with priority
            elif element in self._operator_priorities.keys():
                # take care of unary minus
                if element == '~':
                    if len(calculation_stack) > 0:
                        last = calculation_stack.pop()
                    else:
                        last = 0
                    calculation_stack.append(
                        self.execute_operation('-', 0, last))
                    continue

                # execute binary operation if the operand is not unary minus
                if len(calculation_stack) > 0:
                    second = calculation_stack.pop()
                else:
                    second = 0

                if len(calculation_stack) > 0:
                    first = calculation_stack.pop()
                else:
                    first = 0

                # add the result to stack and return the top element
                outcome = self.execute_operation(element, first, second)
                if isinstance(outcome, float):
                    calculation_stack.append(outcome)
                else:
                    return outcome
        return calculation_stack.pop()

    def process_calculation_query(self, query: str) -> Union[float, str]:
        """
        Calculate arithmetic expression given in infix notation
        -check correctness
        -convert to polish notation
        -calculate expression
        :param query: arithmetic expression to calculate
        :return: the result of calculation
        """

        # remove redundant spaces
        query = ''.join(query.split())
        # check correctness
        valid_input = self.validate_input(query)
        if not valid_input:
            return 'You provided an incorrect input.\n' \
                   'The allowed symbols are: digits: 0-9, ' \
                   'operators: `+-*\\^` and brackets: `()`'
        # transform to  polish notation
        polish_notation = self.to_postfix_notation(query)
        # calculate result
        result = self.calculate(polish_notation)
        return result
