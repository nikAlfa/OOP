from math import sqrt


class Point3d:
    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __repr__(self):
        return f"Point3d(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"


class Vector3d:
    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __repr__(self):
        return f"Vector3d(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"

    @classmethod
    def from_points(cls, start: Point3d, end: Point3d):
        return cls(end.x - start.x, end.y - start.y, end.z - start.z)

    def _vector(self, other):
        if isinstance(other, Vector3d):
            return other.x, other.y, other.z
        if isinstance(other, (int, float)):
            return other, other, other
        return NotImplemented

    def __eq__(self, other):
        other = self._vector(other)
        return other is not NotImplemented and (
            self.x, self.y, self.z
        ) == other

    def __lt__(self, other):
        other = self._vector(other)
        return other is not NotImplemented and len(self) < sqrt(
            other[0] ** 2 + other[1] ** 2 + other[2] ** 2
        )

    def __gt__(self, other):
        other = self._vector(other)
        return other is not NotImplemented and len(self) > sqrt(
            other[0] ** 2 + other[1] ** 2 + other[2] ** 2
        )

    def __add__(self, other):
        x, y, z = self._vector(other)
        return Vector3d(self.x + x, self.y + y, self.z + z)

    __radd__ = __add__

    def __sub__(self, other):
        x, y, z = self._vector(other)
        return Vector3d(self.x - x, self.y - y, self.z - z)

    def __rsub__(self, other):
        x, y, z = self._vector(other)
        return Vector3d(x - self.x, y - self.y, z - self.z)

    def __mul__(self, other):
        x, y, z = self._vector(other)
        return Vector3d(self.x * x, self.y * y, self.z * z)

    __rmul__ = __mul__

    def __truediv__(self, other):
        x, y, z = self._vector(other)
        return Vector3d(self.x / x, self.y / y, self.z / z)

    def __rtruediv__(self, other):
        x, y, z = self._vector(other)
        return Vector3d(x / self.x, y / self.y, z / self.z)

    def __iadd__(self, other):
        x, y, z = self._vector(other)
        self.x += x
        self.y += y
        self.z += z
        return self

    def __isub__(self, other):
        x, y, z = self._vector(other)
        self.x -= x
        self.y -= y
        self.z -= z
        return self

    def __imul__(self, other):
        x, y, z = self._vector(other)
        self.x *= x
        self.y *= y
        self.z *= z
        return self

    def __itruediv__(self, other):
        x, y, z = self._vector(other)
        self.x /= x
        self.y /= y
        self.z /= z
        return self

    def __matmul__(self, other):
        return Vector3d(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    @staticmethod
    def is_collinear(a, b, c):
        return (a @ b).x == 0 and (a @ b).y == 0 and (a @ b).z == 0

    @staticmethod
    def is_complanar(a, b, c):
        return (
            a.x * (b.y * c.z - b.z * c.y)
            - a.y * (b.x * c.z - b.z * c.x)
            + a.z * (b.x * c.y - b.y * c.x)
        ) == 0

    def __len__(self):
        return int(sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2))

    def __getitem__(self, key):
        if key in (0, 'x'):
            return self.x
        if key in (1, 'y'):
            return self.y
        if key in (2, 'z'):
            return self.z
        raise IndexError("Индекс должен быть 0, 1, 2 или 'x', 'y', 'z'")

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z



print("=== Создание ===")
a = Vector3d(3, 4, 5)
b = Vector3d(1, 2, 3)

print(a)
print(repr(a))


print("\n=== from_points ===")
p1 = Point3d(1, 2, 3)
p2 = Point3d(5, 7, 9)

v = Vector3d.from_points(p1, p2)
print(v)


print("\n=== Сравнение ===")
print(a == b)
print(a > b)
print(a < b)


print("\n=== Арифметика ===")
print(a + b)
print(a + 3)
print(3 + a)

print(a - b)
print(a - 2)
print(10 - a)

print(a * b)
print(a * 2)
print(2 * a)

print(a / b)
print(a / 2)
print(100 / a)


print("\n=== Инкрементальные операции ===")
c = Vector3d(3, 4, 5)

c += 2
print(c)

c -= Vector3d(1, 1, 1)
print(c)

c *= 2
print(c)

c /= 2
print(c)


print("\n=== Векторное произведение ===")
print(a @ b)


print("\n=== Коллинеарность ===")
v1 = Vector3d(1, 2, 3)
v2 = Vector3d(2, 4, 6)
v3 = Vector3d(3, 6, 9)

print(Vector3d.is_collinear(v1, v2, v3))


print("\n=== Компланарность ===")
v1 = Vector3d(1, 0, 0)
v2 = Vector3d(0, 1, 0)
v3 = Vector3d(1, 1, 0)

print(Vector3d.is_complanar(v1, v2, v3))


print("\n=== Длина ===")
print(len(Vector3d(3, 4, 0)))


print("\n=== Индексация ===")
print(a[0])
print(a[1])
print(a[2])

print(a['x'])
print(a['y'])
print(a['z'])


print("\n=== Перебор ===")
for coordinate in a:
    print(coordinate)
