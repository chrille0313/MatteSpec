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
        frac.denominator = Fraction.lcm(self.denominator, otherF.denominator)
        frac.numerator = self.numerator * frac.denominator // self.denominator + otherF.numerator * frac.denominator // otherF.denominator

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

    def __lt__(self, other):
        otherF = Fraction(other) if not isinstance(other, Fraction) else other
        return self.decimal < otherF.decimal

    def __gt__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        otherF = Fraction(other) if not isinstance(other, Fraction) else other
        return self.numerator == otherF.numerator and self.denominator == otherF.denominator

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __str__(self):
        if self.numerator == 0:
            return "0"
        elif self.denominator == 1:
            return f"{self.numerator}"
        else:
            return f"{self.numerator}/{self.denominator}"


def fractify(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = Fraction(matrix[i][j])


def determinant(matrix):
    return matrix[0][0] if len(matrix) == 1 else sum([(-1) ** r * matrix[r][0] * determinant([[matrix[i][j] for j in range(len(matrix)) if j != 0] for i in range(len(matrix)) if i != r]) for r in range(len(matrix))])


"""m = [
    [1, 2, 1, 0],
    [0, 3, 1, 1],
    [-1, 0, 3, 1],
    [3, 1, 2, 0]
]"""


# print(laplace(m))

def gauss_eliminate(matrix):
    fractify(matrix)

    for i in range(len(matrix)):
        currentRow = matrix[i]
        factor = 1 / currentRow[i]
        if factor != 1:
            matrix[i] = [n * factor for n in currentRow]

        for j in range(len(matrix)):
            if i != j:
                factor = -matrix[j][i]

                for k in range(len(matrix) + 1):
                    matrix[j][k] += matrix[i][k] * factor

    return matrix


m = [
    [3, -8, 1, 22],
    [2, -3, 4, 20],
    [1, -2, 1, 8],
]

[print(f"[ {' '.join(str(col) for col in row)} ]") for row in gauss_eliminate(m)]

# n1, n2 = Fraction(5), Fraction(5)
# print(2 - n1)
