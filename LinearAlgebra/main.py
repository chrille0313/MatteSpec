from Fractions.fractions import Fraction


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

# [print(row) for row in gauss_eliminate(m)]

# n1, n2 = Fraction(5), Fraction(5)
# print(2 - n1)

print(7/3)