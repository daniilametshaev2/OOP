import math

#класс для углов
class Angle:

    def __init__(self, value=0.0, degrees=False):
        if degrees:
            self._radians = math.radians(value)
        else:
            self._radians = float(value)
        self._normalize()

    def _normalize(self):
        self._radians = self._radians % (2 * math.pi)

#свойства
    @property
    def radians(self):
        return self._radians

    @radians.setter
    def radians(self, value):
        self._radians = float(value)
        self._normalize()

    @property
    def degrees(self):
        return math.degrees(self._radians)

    @degrees.setter
    def degrees(self, value):
        self._radians = math.radians(value)
        self._normalize()

#преобразования
    def __float__(self):
        return self._radians

    def __int__(self):
        return int(self._radians)

    def __str__(self):
        return f"{self.degrees:.2f}°"

    def __repr__(self):
        return f"Angle({self._radians:.5f} rad)"

#сравнения
    def __eq__(self, other):
        if isinstance(other, Angle):
            return math.isclose(self._radians % (2 * math.pi), other._radians % (2 * math.pi), rel_tol=1e-9)
        elif isinstance(other, (int, float)):
            return math.isclose(self._radians % (2 * math.pi), other % (2 * math.pi), rel_tol=1e-9)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Angle):
            return self._radians < other._radians
        elif isinstance(other, (int, float)):
            return self._radians < other
        return NotImplemented

#арифметика
    def __add__(self, other):
        if isinstance(other, Angle):
            return Angle(self._radians + other._radians)
        elif isinstance(other, (int, float)):
            return Angle(self._radians + other)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Angle):
            return Angle(self._radians - other._radians)
        elif isinstance(other, (int, float)):
            return Angle(self._radians - other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Angle(self._radians * other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Angle(self._radians / other)
        return NotImplemented


#класс диапазонов углов

class AngleRange:
    def __init__(self, start, end, include_start=True, include_end=True):
        self.start = Angle(start) if not isinstance(start, Angle) else start
        self.end = Angle(end) if not isinstance(end, Angle) else end
        self.include_start = include_start
        self.include_end = include_end

    def __repr__(self):
        return f"AngleRange({self.start}, {self.end}, include_start={self.include_start}, include_end={self.include_end})"

    def __str__(self):
        left = "[" if self.include_start else "("
        right = "]" if self.include_end else ")"
        return f"{left}{self.start} .. {self.end}{right}"

    def __eq__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented
        return (self.start == other.start and
                self.end == other.end and
                self.include_start == other.include_start and
                self.include_end == other.include_end)

    def length(self):
        #длина промежутка в радианах
        diff = (self.end.radians - self.start.radians) % (2 * math.pi)
        return diff

    def __abs__(self):
        return self.length()

    def __contains__(self, value):
        """Проверка принадлежности угла или диапазона"""
        if isinstance(value, (int, float)):
            value = Angle(value)
        if isinstance(value, Angle):
            s = self.start.radians
            e = self.end.radians
            v = value.radians
            if s <= e:
                if self.include_start and self.include_end:
                    return s <= v <= e
                elif self.include_start:
                    return s <= v < e
                elif self.include_end:
                    return s < v <= e
                else:
                    return s < v < e
            else:
                #диапазон "через 0"
                return v >= s or v <= e
        elif isinstance(value, AngleRange):
            return (value.start in self) and (value.end in self)
        return NotImplemented

#арифметика
    def __add__(self, other):
        #сдвиг диапазона на угол
        if isinstance(other, (int, float, Angle)):
            if not isinstance(other, Angle):
                other = Angle(other)
            return AngleRange(self.start + other, self.end + other,
                              self.include_start, self.include_end)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (int, float, Angle)):
            if not isinstance(other, Angle):
                other = Angle(other)
            return AngleRange(self.start - other, self.end - other,
                              self.include_start, self.include_end)
        return NotImplemented


#пример
a1 = Angle(180, degrees=True)
a2 = Angle(math.pi)
a3 = Angle(3 * math.pi)

print("a1 =", a1)
print("a2 =", a2)
print("a1 == a2?", a1 == a2)
print("a3 == a2?", a3 == a2)
print("a1 + 1 rad =", a1 + 1)
print("a1 * 2 =", a1 * 2)
print("float(a1) =", float(a1))

#диапазон
r1 = AngleRange(0, math.pi / 2)  #[0, π/2]
r2 = AngleRange(Angle(math.pi / 4), Angle(3 * math.pi / 4), include_end=False)

print("\nДиапазоны:")
print("r1 =", r1)
print("r2 =", r2)
print("Длина r1 =", abs(r1))
print("π/3 в r1?", Angle(math.pi / 3) in r1)
print("r2 сдвинут на π/4:", r2 + (math.pi / 4))
