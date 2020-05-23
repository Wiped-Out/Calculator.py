#!/usr/bin/env python3


class SmartCalculator:
    def __init__(self):
        self.variables = {}

    @staticmethod
    def operator(operator) -> str:
        if operator.count("-") % 2 == 0:
            return '+'
        return '-'

    def main(self) -> None:
        while True:
            op = input()
            if op.startswith('/'):
                calc.commands(op)
            elif any(x in op for x in {'+', '-', '*', '/'}) and '=' not in op:
                op = op.split()
                print(self.calculator(op))
            elif '=' in op:
                calc.store_var(op)
                continue
            elif op:
                if op in self.variables:
                    print(self.variables.get(op))
                elif op.isalpha():
                    print('Unknown variable')
                else:
                    print('Invalid identifier')

    def calculator(self, array: list) -> int or str:
        try:
            operator: list = [self.operator(array[i]) for i in range(len(array)) if i % 2 != 0]
            numbers: list = [int(self.variables.setdefault(array[i],
                                                           array[i])) for i in range(len(array)) if i % 2 == 0]
            result: int = numbers[0]
            for i in range(1, len(numbers)):
                sign: int = 1
                if operator[i - 1] == '-':
                    sign = -1
                result += int(numbers[i]) * sign
            return result
        except (ValueError, TypeError):
            return 'Invalid expression'

    def store_var(self, var) -> None:
        var = var.replace('=', ' ').split()
        if all(x.isalpha() for x in var[0]) is False:
            print('Invalid identifier')
            return
        elif var[1].isalpha() and var[1] not in self.variables:
            print('Unknown variable')
            return
        elif (var[1].isalpha() or var[1].isnumeric()) and len(var) <= 2:
            if any(x in var for x in {'+', '-'}):
                self.variables[var[0]] = self.calculator(var[1:])
            elif var[1] in self.variables.keys():
                self.variables[var[0]] = self.variables.get(var[1])
            elif var[1].isnumeric():
                self.variables[var[0]] = var[1]
        else:
            print('Invalid assignment')

    @staticmethod
    def commands(comm):
        if comm == '/exit':
            print('Bye!')
            exit()
        if comm == '/help':
            print('The program calculates the sum and sub of numbers')
            return
        print('Unknown command')


calc = SmartCalculator()
calc.main()
