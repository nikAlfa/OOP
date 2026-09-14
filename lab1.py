import math


class Angle:

    def __init__(self, radians):
        self._radians = float(radians)

    @classmethod
    def from_radians(cls, radians):
        """Радианы"""
        return cls(radians)

    @classmethod
    def from_degrees(cls, degrees):
        """Градусы"""
        return cls(math.radians(degrees))

    def get_radians(self):
        return self._radians

    def set_radians(self, radians):
        self._radians = float(radians)

    def get_degrees(self):
        return math.degrees(self._radians)

    def set_degrees(self, degrees):
        self._radians = math.radians(degrees)

    def __str__(self):
        return f"{self.get_degrees()}°"

    def __repr__(self):
        return f"Angle.from_radians({self._radians})"

    def _normalized(self):
        return self._radians % (2 * math.pi)

    def _compare_value(self, other):
        """Получить значение второго объекта для сравнения."""
        if isinstance(other, Angle):
            return other._normalized()
        if isinstance(other, (int, float)):
            return float(other) % (2 * math.pi)
        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, (Angle, int, float)):
            return NotImplemented
        return math.isclose(
            self._normalized(),
            self._compare_value(other),
            rel_tol=1e-9,
            abs_tol=1e-9
        )

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other):
        if not isinstance(other, (Angle, int, float)):
            return NotImplemented
        return self._normalized() < self._compare_value(other)

    def __le__(self, other):
        if not isinstance(other, (Angle, int, float)):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other):
        if not isinstance(other, (Angle, int, float)):
            return NotImplemented
        return self._normalized() > self._compare_value(other)

    def __ge__(self, other):
        if not isinstance(other, (Angle, int, float)):
            return NotImplemented
        return self == other or self > other

    def __float__(self):
        return self._radians

    def __int__(self):
        return int(self._radians)

    def __add__(self, other):
        if isinstance(other, Angle):
            return Angle.from_radians(self._radians + other._radians)
        if isinstance(other, (int, float)):
            # Число считается заданным в радианах
            return Angle.from_radians(self._radians + other)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Angle):
            return Angle.from_radians(self._radians - other._radians)
        if isinstance(other, (int, float)):
            # Число считается заданным в радианах
            return Angle.from_radians(self._radians - other)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            # Число считается заданным в радианах
            return Angle.from_radians(other - self._radians)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Angle.from_radians(self._radians * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Нельзя делить угол на ноль")
            return Angle.from_radians(self._radians / other)
        return NotImplemented


class AngleRange:
    def __init__(self, start, end, start_inclusive=True, end_inclusive=True):
        if isinstance(start, Angle):
            self._start = start
        elif isinstance(start, (int, float)):
            self._start = Angle.from_radians(start)

        if isinstance(end, Angle):
            self._end = end
        elif isinstance(end, (int, float)):
            self._end = Angle.from_radians(end)

        self._start_inclusive = bool(start_inclusive)
        self._end_inclusive = bool(end_inclusive)

    def get_start(self):
        return Angle.from_radians(self._start.get_radians())

    def get_end(self):
        return Angle.from_radians(self._end.get_radians())

    def __str__(self):
        left = "[" if self._start_inclusive else "("
        right = "]" if self._end_inclusive else ")"
        return f"{left}{self._start.get_degrees()}°, {self._end.get_degrees()}°{right}"

    def __repr__(self):
        return (
            f"AngleRange("
            f"Angle.from_radians({self._start.get_radians()}), "
            f"Angle.from_radians({self._end.get_radians()}), "
            f"start_inclusive={self._start_inclusive}, "
            f"end_inclusive={self._end_inclusive})"
        )

    def __abs__(self):
        start = self._start._normalized()
        end = self._end._normalized()
        length = end - start
        if length < 0:
            length += 2 * math.pi
        return length

    def length(self):
        return abs(self)

    def __eq__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented
        return self <= other and other <= self

    def __le__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented

        # Промежуток self должен полностью лежать в other.
        s1 = self._start._normalized()
        s2 = other._start._normalized()
        length1 = abs(self)
        length2 = abs(other)

        if length1 > length2 and not math.isclose(length1, length2):
            return False

        offset = (s1 - s2) % (2 * math.pi)
        if offset > length2 + 1e-9:
            return False

        if math.isclose(offset, length2, abs_tol=1e-9):
            return self._start_inclusive <= other._start_inclusive

        finish = offset + length1
        if finish > length2 + 1e-9:
            return False

        if math.isclose(finish, length2, abs_tol=1e-9):
            return self._end_inclusive <= other._end_inclusive

        return True

    def __lt__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented
        return self <= other and self != other

    def __ge__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented
        return other <= self

    def __gt__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented
        return other <= self and self != other

    def __add__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented

        length = abs(self) + abs(other)
        if length >= 2 * math.pi - 1e-9:
            return [
                AngleRange(
                    Angle.from_radians(0),
                    Angle.from_radians(2 * math.pi),
                    True,
                    False
                )
            ]

        start = self._start + other._start
        end = self._end + other._end
        start_inc = self._start_inclusive and other._start_inclusive
        end_inc = self._end_inclusive and other._end_inclusive

        start_n = start._normalized()
        end_n = end._normalized()

        if start_n <= end_n:
            return [AngleRange(start, end, start_inc, end_inc)]

        return [
            AngleRange(
                Angle.from_radians(0), end,
                True, end_inc
            ),
            AngleRange(
                start, Angle.from_radians(2 * math.pi),
                start_inc, False
            )
        ]

    def __sub__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented

        start = self._start - other._end
        end = self._end - other._start
        start_inc = self._start_inclusive and other._end_inclusive
        end_inc = self._end_inclusive and other._start_inclusive

        if abs(self) + abs(other) >= 2 * math.pi - 1e-9:
            return [
                AngleRange(
                    Angle.from_radians(0),
                    Angle.from_radians(2 * math.pi),
                    True,
                    False
                )
            ]

        start_n = start._normalized()
        end_n = end._normalized()

        if start_n <= end_n:
            return [AngleRange(start, end, start_inc, end_inc)]

        return [
            AngleRange(
                Angle.from_radians(0), end,
                True, end_inc
            ),
            AngleRange(
                start, Angle.from_radians(2 * math.pi),
                start_inc, False
            )
        ]

    def __contains__(self, item):
        if isinstance(item, (Angle, int, float)):
            if not isinstance(item, Angle):
                item = Angle.from_radians(item)

            value = item._normalized()
            start = self._start._normalized()
            distance = (value - start) % (2 * math.pi)
            length = abs(self)

            if distance > length + 1e-9:
                return False
            if math.isclose(distance, 0, abs_tol=1e-9):
                return self._start_inclusive
            if math.isclose(distance, length, abs_tol=1e-9):
                return self._end_inclusive
            return distance < length

        # Проверка вложенности промежутка
        if isinstance(item, AngleRange):
            return item <= self

        return False


print("\n========== Angle ==========")
# Создание углов
a = Angle.from_degrees(90)
b = Angle.from_radians(math.pi / 2)

print("a =", a)
print("b =", b)

# Геттеры
print("a в радианах:", a.get_radians())
print("a в градусах:", a.get_degrees())

# Сеттеры
a.set_degrees(180)
print("После set_degrees(180):", a)

a.set_radians(math.pi / 2)
print("После set_radians(pi / 2):", a)

# repr
print("repr(a):", repr(a))

# Сравнение
c = Angle.from_degrees(360)
d = Angle.from_degrees(0)

print("360° == 0°:", c == d)

e = Angle.from_degrees(450)
f = Angle.from_degrees(90)

print("450° == 90°:", e == f)

# Преобразования
print("float(a):", float(a))
print("int(a):", int(a))

# Сложение углов
x = Angle.from_degrees(30)
y = Angle.from_degrees(60)

print("30° + 60° =", x + y)

# Сложение с числом (число в радианах)
print("30° + 1 радиан =", x + 1)

# Вычитание
print("60° - 30° =", y - x)
print("60° - 1 радиан =", y - 1)

# Умножение
print("30° * 2 =", x * 2)
print("30° * 2.5 =", x * 2.5)

# Деление
print("60° / 2 =", y / 2)

# Обратные операции
print("2 * 30° =", 2 * x)
print("1 + 30° =", 1 + x)



print("\n========== AngleRange ==========")

r1 = AngleRange(Angle.from_degrees(30), Angle.from_degrees(120))
r2 = AngleRange(0, math.pi / 2, False, True)
r3 = AngleRange(Angle.from_degrees(30), Angle.from_degrees(120), False, False)

print("\n--- Создание ---")
print("r1 =", r1)
print("r2 =", r2)
print("r3 =", r3)

print("\n--- repr ---")
print("repr(r1) =", repr(r1))

print("\n--- Границы ---")
print("Начало r1:", r1.get_start())
print("Конец r1:", r1.get_end())

print("\n--- Длина ---")
print("Длина r1 в радианах:", abs(r1))
print("Длина r1 в градусах:", math.degrees(abs(r1)))

print("\n--- Проверка угла через in ---")
print("30° in r1:", Angle.from_degrees(30) in r1)
print("90° in r1:", Angle.from_degrees(90) in r1)
print("150° in r1:", Angle.from_degrees(150) in r1)

print("\n--- Проверка числа через in ---")
print("pi/2 in r1:", math.pi / 2 in r1)

print("\n--- Проверка вложенности ---")
r4 = AngleRange(Angle.from_degrees(60), Angle.from_degrees(90))
r5 = AngleRange(Angle.from_degrees(0), Angle.from_degrees(180))

print("r4 =", r4)
print("r5 =", r5)
print("r4 in r1:", r4 in r1)
print("r1 in r5:", r1 in r5)

print("\n--- Сравнение ---")
print("r4 < r1:", r4 < r1)
print("r4 <= r1:", r4 <= r1)
print("r1 >= r4:", r1 >= r4)
print("r1 == r1:", r1 == r1)
print("r1 == r3:", r1 == r3)

print("\n--- Включающие и исключающие границы ---")
print("30° in r1:", Angle.from_degrees(30) in r1)
print("30° in r3:", Angle.from_degrees(30) in r3)
print("120° in r1:", Angle.from_degrees(120) in r1)
print("120° in r3:", Angle.from_degrees(120) in r3)

print("\n--- Сложение ---")
a = AngleRange(Angle.from_degrees(10), Angle.from_degrees(40))
b = AngleRange(Angle.from_degrees(20), Angle.from_degrees(50))

print("a + b =", ", ".join(str(r) for r in a + b))

print("\n--- Вычитание ---")
print("a - b =", ", ".join(str(r) for r in a - b))



print("\n--- Промежуток через 0° ---")
c = AngleRange(Angle.from_degrees(330), Angle.from_degrees(30))
d = AngleRange(Angle.from_degrees(20), Angle.from_degrees(60))

print("c =", c)
print("20° in c:", Angle.from_degrees(20) in c)
print("c + d =", ", ".join(str(r) for r in c + d))
print("c - d =", ", ".join(str(r) for r in c - d))