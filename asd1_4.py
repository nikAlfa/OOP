### ЛАБОРАТОРНАЯ РАБОТА №1

# def check_brackets(s):
#     stack = []
#     pairs = {')': '(', '}': '{', ']': '['}
#
#     for char in s:
#         if char in '({[':
#             stack.append(char)
#         elif char in ')}]':
#             if not stack or stack[-1] != pairs[char]:
#                 return False
#             stack.pop()
#
#     return len(stack) == 0
#
#
# def main():
#     print("Введите строку:")
#     s = input().strip()
#
#     if not s:
#         print("Строка не существует")
#         return
#
#     if check_brackets(s):
#         print("Строка существует")
#     else:
#         print("Строка не существует")
#
#
# if name == "main":
#     main()

### ЛАБОРАТОРНАЯ РАБОТА №2

def check_brackets(s):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0


class Parser:
    def init(self, expr):
        self.expr = expr
        self.pos = 0 # pos - положение нашего курсора в настоящий момент

    def parse(self):
        result = self.expression()
        return result

    def expression(self):
        result = self.term()
        while self.pos < len(self.expr) and self.expr[self.pos] in '+-':
            op = self.expr[self.pos]
            self.pos += 1
            right = self.term()
            if op == '+':
                result += right
            else:
                result -= right
        return result

    def term(self):
        result = self.factor()
        while self.pos < len(self.expr) and self.expr[self.pos] in '*/':
            op = self.expr[self.pos]
            self.pos += 1
            right = self.factor()
            if op == '*':
                result *= right
            else:
                if right == 0:
                    raise ZeroDivisionError()
                result /= right
        return result

    def factor(self):
        if self.pos < len(self.expr) and self.expr[self.pos] == '(':
            self.pos += 1
            result = self.expression()
            if self.pos < len(self.expr) and self.expr[self.pos] == ')':
                self.pos += 1
            return result

        start = self.pos
        while self.pos < len(self.expr) and (self.expr[self.pos].isdigit() or self.expr[self.pos] == '.'):
            self.pos += 1
        return float(self.expr[start:self.pos])


def main():
    print("Введите выражение:")
    s = input().strip()

    if not s.endswith('='):
        print("Выражение должно заканчиваться '='")
        return

    expr = s[:-1]

    if not check_brackets(expr):
        print("Скобки расставлены неверно")
        return

    try:
        parser = Parser(expr)
        result = parser.parse()
        print(f"Результат: {result}")
    except ZeroDivisionError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


if name == "main":
    main()

### ЛАБОРАТОРНАЯ РАБОТА №3

def is_valid(x):
    if x == 1:
        return True
    for p in (3, 5, 7):
        while x % p == 0:
            x //= p
    return x == 1


def main():
    print("Введите число x:")
    x = int(input())

    for i in range(1, x + 1):
        if is_valid(i):
            print(i, end=' ')


if name == "main":
    main()

### ЛАБОРАТОРНАЯ РАБОТА №4

import random

# def comb_sort(arr):
#     n = len(arr)
#     gap = n
#     swapped = True
#     while gap > 1 or swapped:
#         gap = max(1, int(gap / 1.3))
#         swapped = False
#         for i in range(n - gap):
#             if arr[i] > arr[i + gap]:
#                 arr[i], arr[i + gap] = arr[i + gap], arr[i]
#                 swapped = True
#     return arr
#
#
# if name == "main":
#     print("Введите числа через пробел:")
#     arr = list(map(float, input().split()))
#
#     result = (comb_sort(arr))
#     print("Отсортированный массив:", result)

### ЛАБОРАТОРНАЯ РАБОТА №5

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

if name == "main":
    print("Введите числа через пробел:")
    arr = list(map(float, input().split()))

    result = (insertion_sort(arr))
    print("Отсортированный массив:", result)
