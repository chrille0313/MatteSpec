import numpy
import numpy as np
from typing import Union

OPERATIONS = {
    "add": np.add,
    "sub": np.subtract,
    "mul": np.multiply,
    "div": np.true_divide,
    "dot": np.dot,
    "cross": np.cross,
}


class Vector3D(object):
    up = None
    down = None
    left = None
    right = None
    forward = None
    back = None

    def __init__(self, x, y, z, w=1.0, dtype=None):
        self._data = np.array([x, y, z, w], dtype=dtype)

    def __repr__(self):
        return 'Vector3D({0}, {1}, {2}, {3})'.format(*self._data)

    def __str__(self):
        return repr(self)

    @property
    def x(self) -> Union[int, float]:
        """
        Property x is first element of vector.

        :return: Union[int, float]

        >>> Vector3D(10, 20, 30).x
        10.0

        >>> Vector3D(10.0, 20.0, 30.0).x
        10.0
        """

        return self._data[0]

    @x.setter
    def x(self, value):
        self._data[0] = value

    @property
    def y(self) -> Union[int, float]:
        """
        Property y is second element of vector.

        :return: Union[int, float]

        >>> Vector3D(10, 20, 30).y
        20.0

        >>> Vector3D(10.0, 20.0, 30.0).y
        20.0
        """

        return self._data[1]

    @y.setter
    def y(self, value):
        self._data[1] = value

    @property
    def z(self) -> Union[int, float]:
        """
        Property z is third element of vector.

        :return: Union[int, float]

        >>> Vector3D(10, 20, 30).z
        30.0

        >>> Vector3D(10.0, 20.0, 30.0).z
        30.0
        """

        return self._data[2]

    @z.setter
    def z(self, value):
        self._data[2] = value

    @property
    def w(self) -> Union[int, float]:
        """
        Property w is fourth element of vector.

        :return: Union[int, float]

        >>> Vector3D(10, 20, 30).w
        1.0

        >>> Vector3D(10.0, 20.0, 30.0).w
        1.0

        >>> Vector3D(10.0, 20.0, 30.0, 2.0).w
        2.0
        """

        return self._data[3]

    @w.setter
    def w(self, value):
        self._data[3] = value

    @property
    def components(self):
        return self._data

    @property
    def length(self) -> float:
        """
        Calculates magnitude of self and returns result as a float.

        :return: float

        >>> Vector3D(0, 1, 0).length
        1.0
        """

        return np.linalg.norm(self._data[:3])

    @property
    def normalized(self):
        """
        Normalizes self and returns result as a Vector3D.

        :return: Vector3D

        >>> Vector3D(0, 1, 0).normalized
        Vector3D(0.0, 1.0, 0.0, 1.0)
        """
        vector = type(self)(*(self._data / np.linalg.norm(self._data[:3])))
        vector.w = 1
        return vector

    def _apply_operation(self, operation, value):
        return type(self)(*OPERATIONS[operation](*(self._data, value._data) if isinstance(value, type(self)) else (self._data, value)))

    def __neg__(self):
        """
        Negates each component of self.

        :return: Vector3D

        >>> -Vector3D(1, 2, 3)
        Vector3D(-1.0, -2.0, -3.0, 1.0)
        """

        vector = Vector3D(*numpy.negative(self._data))
        vector.w = 1
        return vector

    def __add__(self, value):
        """
        Adds the value into self, and returns result as Vector3D.

        :param value:  Union[Vector3D, int, float]
        :return: Vector3D

        >>> Vector3D(1, 2, 3) + Vector3D(2, 4, 6)
        Vector3D(3.0, 6.0, 9.0, 1.0)

        >>> Vector3D(1, 2, 3) + 5
        Vector3D(6.0, 7.0, 8.0, 1.0)

        >>> Vector3D(1.0, 2.0, 3.0) + 5.0
        Vector3D(6.0, 7.0, 8.0, 1.0)
        """

        vector = self._apply_operation("add", value)
        vector.w = 1
        return vector

    def __sub__(self, value):
        """
        Subtracts the value from self, and returns result as Vector3D.

        :param value:  Union[Vector3D, int, float]
        :return: Vector3D

        >>> Vector3D(2, 4, 6) - Vector3D(1, 2, 3)
        Vector3D(1.0, 2.0, 3.0, 1.0)

        >>> Vector3D(6, 7, 8) - 5
        Vector3D(1.0, 2.0, 3.0, 1.0)

        >>> Vector3D(6.0, 7.0, 8.0) - 5.0
        Vector3D(1.0, 2.0, 3.0, 1.0)
        """

        vector = self._apply_operation("sub", value)
        vector.w = 1
        return vector

    def __mul__(self, value):
        """
        Multiplies self with the value, and returns result as Vector3D.

        :param value:  Union[Vector3D, int, float]
        :return: Vector3D

        >>> Vector3D(1, 2, 3) * Vector3D(2, 4, 6)
        Vector3D(2.0, 8.0, 18.0, 1.0)

        >>> Vector3D(1, 2, 3) * 2
        Vector3D(2.0, 4.0, 6.0, 1.0)

        >>> Vector3D(1.0, 2.0, 3.0) * 2.0
        Vector3D(2.0, 4.0, 6.0, 1.0)
        """

        vector = self._apply_operation("mul", value)
        vector.w = 1
        return vector

    def __truediv__(self, value):
        """
        Divides self with the value, and returns result as Vector3D.

        :param value:  Union[Vector3D, int, float]
        :return: Vector3D

        >>> Vector3D(1, 2, 3) / Vector3D(2, 4, 6)
        Vector3D(0.5, 0.5, 0.5, 1.0)

        >>> Vector3D(1, 2, 3) / 2
        Vector3D(0.5, 1.0, 1.5, 1.0)

        >>> Vector3D(1.0, 2.0, 3.0) / 2.0
        Vector3D(0.5, 1.0, 1.5, 1.0)
        """

        vector = self._apply_operation("div", value)
        vector.w = 1
        return vector

    def dot(self, other: 'Vector3D') -> Union[int, float]:
        """
        Returns the dot-product of two vectors.

        :param other: Vector3D
        :return: Union[int, float, Vector3D, ndarray]

        >>> Vector3D(1, 0, 0).dot(Vector3D(-1, 0, 0))
        -1.0

        >>> Vector3D(1.0, 0.0, 0.0).dot(Vector3D(-1.0, 0.0, 0.0))
        -1.0
        """

        return np.dot(self[:3], other[:3])

    def cross(self, other):
        """
        Returns the cross-product of two vectors.

        :param other: Vector3D
        :return: Vector3D

        >>> Vector3D(0, 0, 1).cross(Vector3D(1, 0, 0))
        Vector3D(0.0, 1.0, 0.0, 1.0)
        """

        return type(self)(*np.cross(self._data[:3], other._data[:3]))

    def __array__(self, dtype=None):
        if dtype:
            return np.array([self.x, self.y, self.z, self.w], dtype=dtype)
        else:
            return np.array([self.x, self.y, self.z, self.w])

    def __iter__(self):
        return (component for component in self._data[:3])

    def __getitem__(self, item):
        return self._data[item]


Vector3D.up = Vector3D(0, 1, 0)
Vector3D.down = Vector3D(0, -1, 0)
Vector3D.left = Vector3D(-1, 0, 0)
Vector3D.right = Vector3D(1, 0, 0)
Vector3D.forward = Vector3D(0, 0, 1)
Vector3D.back = Vector3D(0, 0, -1)


def dot(a, b):
    return np.dot(a, b)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(Vector3D.forward)

    print(dot(Vector3D(1, 0, 0), Vector3D(-1, 0, 0)))
    print(Vector3D(1, 0, 0).dot(Vector3D(-1, 0, 0)))

    print(Vector3D(0, 0, 1).cross(Vector3D(-1, 0, 0)))
