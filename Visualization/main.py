import numpy as np
import matplotlib.pyplot as plt

"""
STEP = 0.1


def f1(x):
    return np.sin(x)


def f2(x):
    return 2*np.cos(2*x)


def f3(x):
    return x + 3


def f4(x):
    return x * 3


xVals = np.arange(-2*np.pi, 2*np.pi, STEP)
functions = [
    [[f1, f2], []],
    [[f3], [f4]]
]

fig, axis = plt.subplots(2, 2)

for i, pos in enumerate(axis):
    for j, ax in enumerate(pos):
        for func in functions[i][j]:
            ax.plot(xVals, func(xVals))

plt.show()
"""


def mandelbrot(x, y, width, height, zoom=1.0, maxIterations=100):
    aspectRatio = height/width
    screen = np.array([1.5, 1.5 * aspectRatio])/zoom

    xCoords = np.linspace(x - 0.5 - screen[0], x - 0.5 + screen[0], width).reshape((1, width))
    yCoords = np.linspace(y - screen[1], y + screen[1], height).reshape((height, 1))
    complexNumbers = xCoords + 1j * yCoords

    z = np.zeros(complexNumbers.shape, dtype=np.complex128)

    for i in range(maxIterations + 1):
        z = z ** 2 + complexNumbers
        z[np.abs(z) > 2] = i

    return np.abs(z)


colors = mandelbrot(0, 0, 800, 800, 1, 100)
plt.imshow(colors)
plt.show()
