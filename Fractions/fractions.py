class Fraction:
    def __init__(self, n, den=1):
        if isinstance(n, float):
            string = str(n)
            decimalCount = len(string[string.find("."):]) - 1
            self.numerator = int(n * 10 ** decimalCount)
            self.denominator = int(10 ** decimalCount)
            self.reduce(self)
        else:
            self.numerator = n
            self.denominator = den

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def lcm(a, b):
        return a * b // Fraction.gcd(a, b)

    @staticmethod
    def reduce(frac: "Fraction"):
        gcd = Fraction.gcd(frac.numerator, frac.denominator)
        frac.numerator //= gcd
        frac.denominator //= gcd
        return frac

    @property
    def decimal(self):
        return self.numerator / self.denominator

    def __mul__(self, other):
        otherF = Fraction(other) if not isinstance(other, Fraction) else other

        frac = Fraction(1)
        frac.numerator = self.numerator * otherF.numerator
        frac.denominator = self.denominator * otherF.denominator

        return self.reduce(frac)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        otherF = Fraction(other) if not isinstance(other, Fraction) else other

        frac = Fraction(1)
        frac.numerator, frac.denominator = otherF.denominator, otherF.numerator

        return self.__mul__(frac)

    def __rtruediv__(self, other):
        frac = Fraction(1)
        frac.numerator, frac.denominator = self.denominator, self.numerator
        return frac * other

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __rfloordiv__(self, other):
        return self.__rtruediv__(other)

    def __add__(self, other):
        otherF = Fraction(other) if not isinstance(other, Fraction) else other

        frac = Fraction(1)
        lcm = Fraction.lcm(self.denominator, otherF.denominator)
        frac.denominator = lcm
        frac.numerator = self.numerator * lcm // self.denominator + otherF.numerator * lcm // otherF.denominator

        return self.reduce(frac)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        otherF = Fraction(other) if not isinstance(other, Fraction) else other

        frac = Fraction(1)
        frac.numerator = otherF.numerator * -1
        frac.denominator = otherF.denominator

        return self.__add__(frac)

    def __rsub__(self, other):
        return self.__neg__().__add__(other)

    def __neg__(self):
        frac = Fraction(1)
        frac.numerator, frac.denominator = -self.numerator, self.denominator
        return frac

    def __str__(self):
        if self.denominator == 1 or self.numerator == 0:
            return f"{self.numerator}"
        else:
            return f"{self.numerator}/{self.denominator}"


"""
fraction1 = Fraction(0.25)
fraction2 = Fraction(0.2)

print(fraction1, fraction2)
print(-fraction1, -fraction2)

print(fraction1 - 3)
print(3 - fraction1)

print(fraction1 + 2)
print(2 + fraction1)

print(fraction1 * fraction2)
print(fraction2 * fraction1)

print(fraction1 / fraction2)
print(fraction2 / fraction1)
"""