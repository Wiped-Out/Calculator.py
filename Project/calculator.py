#!/usr/bin/env python3
import re
from collections import deque


class SmartCalculator:
    def __init__(self):
        self.variables = {}  # variables stored by the user
        self.op = {'/': 2, '*': 2, '-': 1, '+': 1}  # operators priority
        self.operators = deque()  # stack
        self.stack = deque()  # postfix

    @staticmethod
    def commands(comm):
        if comm == '/exit':
            print('Bye!')
            exit()
        if comm == '/help':
            print('The program calculates addition, subtraction, multiplication and integer division')
            return
        return 'Unknown command'

    def main(self) -> None:  # Main driver
        while True:
            op = input()
            if op.startswith('/'):
                print(self.commands(op))
            elif any(x in op for x in self.op.keys()) and '=' not in op:
                print(self.check_operators(op))
            elif op.count('=') == 1:
                self.store_var(op)
                continue
            elif op:
                if self.var_in_dict(op):
                    print(self.get_var(op))
                elif op.strip().isalpha():
                    print('Unknown variable')
                else:
                    print('Invalid identifier')

    def check_operators(self, operator: str):
        if (operator.count('(') + operator.count(')')) % 2 != 0:
            return 'Invalid expression'
        elif len(operator) <= 2:
            return operator
        while any(x in operator for x in ('--', '++', '-+', '+-')) is True:
            operator = operator.replace('--', '+')
            operator = operator.replace('++', '+')
            operator = operator.replace('-+', '-')
            operator = operator.replace('+-', '-')
        return self.infix_to_postfix(operator)

    def var_in_dict(self, key):
        return True if key in self.variables else False

    def get_var(self, keys):
        return self.variables.setdefault(keys, keys)

    def store_var(self, var) -> None:
        var = var.replace('=', ' ').split()
        if all(x.isalpha() for x in var[0]) is False:
            print('Invalid identifier')
            return
        elif var[1].isalpha() and not self.var_in_dict(var[1]):
            print('Unknown variable')
            return
        elif (var[1].isalpha() or var[1].isnumeric()) and len(var) >= 2:
            if any(x in var[1:] for x in self.op):
                self.variables[var[0]] = str(self.check_operators(' '.join(var[1:])))
            else:
                self.variables[var[0]] = self.get_var(var[1])
        else:
            print('Invalid assignment')

# infix > postfix > answer

    def is_empty(self) -> bool:  # Checks if there are no operators left
        return True if len(self.operators) == 0 else False

    def priority(self, operator: str) -> bool:  # Checks operator priority
        try:
            a = self.op[operator]
            b = self.op[self.operators[-1]]
            return True if b >= a else False
        except KeyError:
            return False

    def infix_to_postfix(self, infix: str) -> int:
        infix = re.compile(r'(\d+|[^ 0-9])').findall(infix)  # Regex to split mathematical expressions
        for i in infix:  # Scanning operation...
            if i.isalnum():
                self.stack.append(self.get_var(i))
            elif i == '(':
                self.operators.append(self.get_var(i))
            elif i == ')':
                while not self.is_empty() and self.operators[-1] != '(':
                    a = self.operators.pop()
                    self.stack.append(self.get_var(a))
                else:
                    if not self.is_empty():
                        self.operators.pop()
            else:
                while not self.is_empty() and self.priority(i):
                    self.stack.append(self.operators.pop())
                self.operators.append(self.get_var(i))
        while not self.is_empty():
            self.stack.append(self.operators.pop())
        return self.postfix_to_answer(list(self.stack))


#TODO: Sometimes 2+2 explodes, I need to fix that.
    def postfix_to_answer(self, postfix: list) -> int or str:
        for n in postfix:
            if n.isalnum():
                self.stack.append(n)
            if n in self.op:
                try:
                    if len(self.stack) >= 2:
                        b = self.stack.pop()
                        a = self.stack.pop()
                        x = str(eval(f'{a}{n}{b}'))
                        self.stack.append(x)
                except (SyntaxError):
                    return 'Invalid expression'
        result = float(self.stack[-1])
        return int(result)
# SyntaxError, NameError

calc = SmartCalculator()
calc.main()
