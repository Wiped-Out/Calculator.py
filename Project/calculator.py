#!/usr/bin/env python3
import re
from collections import deque
from typing import Deque, List, Optional, Union, Dict
from operator import add, sub, mul, truediv


class SmartCalculator:
    def __init__(self) -> None:
        self.variables: Dict[str, str] = {}
        self.operator_stack: Deque[str] = deque()
        self.stack: Deque[str] = deque()

    @staticmethod
    def commands(comm: str) -> Optional[str]:
        if comm == '/exit':
            print('Bye!')
            exit()
        if comm == '/help':
            return 'I need somebody!'
        return 'Unknown command'

    def main(self) -> None:
        while True:
            expression: str = input()
            if expression.startswith('/'):
                print(self.commands(expression))
            elif (
                any(x in expression for x in ('/', '*', '-', '+'))
                and '=' not in expression
            ):
                print(self.check_operators(expression))
            elif expression.count('=') == 1:
                self.store_var(expression)
                continue
            elif expression:
                if self.var_in_dict(expression):
                    print(self.get_var(expression))
                elif expression.strip().isalpha():
                    print('Unknown variable')
                else:
                    print('Invalid identifier')

    def check_operators(self, expression: str) -> Union[str, int]:
        """Cleans the expression"""
        if (expression.count('(') + expression.count(')')) % 2 != 0:
            return 'Invalid expression'
        elif len(expression) <= 2:
            return expression
        while any(x in expression for x in ('--', '++', '-+', '+-')) is True:
            expression = expression.replace('--', '+')
            expression = expression.replace('++', '+')
            expression = expression.replace('-+', '-')
            expression = expression.replace('+-', '-')
        return self.infix_to_postfix(expression)

    def var_in_dict(self, key) -> bool:
        return True if key in self.variables else False

    def get_var(self, keys) -> str:
        return self.variables.setdefault(keys, keys)

    def store_var(self, variable: str) -> None:
        var: List[str] = variable.replace('=', ' ').split()
        if all(x.isalpha() for x in var[0]) is False:
            print('Invalid identifier')
            return
        elif var[1].isalpha() and not self.var_in_dict(var[1]):
            print('Unknown variable')
            return
        elif (var[1].isalpha() or var[1].isnumeric()) and len(var) >= 2:
            if any(x in var[1:] for x in ('/', '*', '-', '+')):
                self.variables[var[0]] = str(self.check_operators(' '.join(var[1:])))
            else:
                self.variables[var[0]] = self.get_var(var[1])
        else:
            print('Invalid assignment')

    # infix > postfix > answer

    def is_empty(self) -> bool:  # Checks if there are no operators left
        return True if len(self.operator_stack) == 0 else False

    def priority(self, operator: str) -> bool:
        """Checks operator priority"""
        priority = {'/': 2, '*': 2, '-': 1, '+': 1}
        try:
            a = priority[operator]
            b = priority[self.operator_stack[-1]]
            return True if b >= a else False
        except KeyError:
            return False

    def infix_to_postfix(self, infix: str) -> Union[int, str]:
        # Regex to split mathematical expressions
        r = re.compile(r'(\d+|[^ 0-9])')
        infix_exp: List[str] = r.findall(infix)
        for i in infix_exp:
            if i.isalnum():
                self.stack.append(self.get_var(i))
            elif i == '(':
                self.operator_stack.append(self.get_var(i))
            elif i == ')':
                while not self.is_empty() and self.operator_stack[-1] != '(':
                    a = self.operator_stack.pop()
                    self.stack.append(self.get_var(a))
                else:
                    if not self.is_empty():
                        self.operator_stack.pop()
            else:
                while not self.is_empty() and self.priority(i):
                    self.stack.append(self.operator_stack.pop())
                self.operator_stack.append(self.get_var(i))
        while not self.is_empty():
            self.stack.append(self.operator_stack.pop())
        return self.postfix_to_answer(list(self.stack))

    def postfix_to_answer(self, postfix: List[str]) -> Union[int, str]:
        operators = {'+': add, '-': sub, '*': mul, '/': truediv}
        for n in postfix:
            if n.isalnum():
                self.stack.append(n)
            if n in operators.keys():
                try:
                    if len(self.stack) >= 2:
                        b = self.stack.pop()
                        a = self.stack.pop()
                        ans = operators[n](float(a), float(b))
                        self.stack.append(str(ans))
                except (SyntaxError, ValueError):
                    return 'Invalid expression'
        result = float(self.stack[-1])
        self.stack.clear()
        return int(result)


if __name__ == '__main__':
    calc = SmartCalculator()
    calc.main()
