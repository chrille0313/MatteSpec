class Fraction:
    def __init__(self, n):
        if isinstance(n, float):
            string = str(n)
            decimalCount = len(string[string.find("."):]) - 1
            self.numerator = int(n * 10 ** decimalCount)
            self.denominator = int(10 ** decimalCount)
            self.reduce(self)
        else:
            self.numerator = n
            self.denominator = 1

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
        frac.denominator, frac.numerator = Fraction.lcm(self.denominator,
                                                        otherF.denominator), self.numerator * frac.denominator // self.denominator + otherF.numerator * frac.denominator // otherF.denominator

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
        frac.numerator, frac.denominator = -self.numerator, frac.denominator
        return frac

    def __str__(self):
        if self.numerator == 0:
            return "0"
        elif self.denominator == 1:
            return f"{self.numerator}"
        else:
            return f"{self.numerator}/{self.denominator}"
