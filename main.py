import logging
from calculator_class import SimpleCalculator
import sys
logging.basicConfig(level=logging.INFO)


def run_calculation():

    # init calculator
    calculator = SimpleCalculator()
    sys.stdout.write(
        'This is a simple calculator that can calculate expressions'
        ' with the following operators: +-*/^.\nJust type '
        'the expression you want to calculate.\nIf you want to stop '
        'the program, just type `done`.\n')
    # status `run` till `done` provided as an input
    run = True
    while run:
        # query expression
        sys.stdout.write('Please, type the expression you want to calculate:'
                         '\n')
        # read expression
        query = sys.stdin.readline().strip('\n')
        # check if stop
        if query == 'done':
            run = False
            continue
        # otherwise calculate expression
        result = calculator.process_calculation_query(query)
        # print result
        if isinstance(result, float):
            # if the result is integral, print as int
            # it is just more visually pleasing
            if int(result) == result:
                sys.stdout.write(f'Answer: {int(result)}\n')
            else:
                sys.stdout.write(f'Answer: {result}\n')
        # if something went wrong, inform
        else:
            logging.warning('Sorry, the given expression cannot be calculated')
            logging.warning(str(result))


def main():
    run_calculation()


if __name__ == '__main__':
    main()
