import logging
from calculator import SimpleCalculator
import sys

logging.basicConfig(level=logging.INFO)


def main():
    calculator = SimpleCalculator()
    sys.stdout.write(
        'This is a simple calculator that can calculate expressions'
        ' with the following operators: +-*/^.\nProvide '
        'the expression you want to calculate.\nIf you want to stop '
        'the program, just type `done`')

    while True:
        sys.stdout.write('Please, type the expression you want to calculate:'
                         '\n')
        query = sys.stdin.readline().strip('\n')
        if query == 'done':
            break
        result = calculator.process_calculation_query(query)
        if isinstance(result, float):
            sys.stdout.write(f'Answer: {result}\n')
        else:
            logging.warning('Sorry, the given expression cannot be calculated')
            logging.warning(str(result))


if __name__ == '__main__':
    main()
