import numpy as np
import pygame
from numpy import array, sin, cos, tan, deg2rad, rad2deg, matrix


class Transform:
    def __init__(self, position, rotation, scale):
        self._pos = array(position)
        self._rot = array(rotation)
        self._scale = scale

        self.forward = 0
        self.up = 0
        self.right = 0

        self.transformMatrix = 0
        self.rotationMatrix = 0

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, newPos):
        self._pos = array(newPos)

    @property
    def rotation(self):
        return self._pos

    @rotation.setter
    def rotation(self, newRot, worldUp=None):
        worldUp = [0, 1, 0] if worldUp is None else worldUp
        self._rot = newRot

    @staticmethod
    def rotate(vector, angles):
        angleX, angleY, angleZ = deg2rad(angles)

        rotationX = matrix([[1, 0, 0],
                           [0, cos(angleX), -sin(angleX)],
                           [0, sin(angleX), cos(angleX)]])

        rotationY = matrix([[cos(angleY), 0, sin(angleY)],
                           [0, 1, 0],
                           [-sin(angleY), 0, cos(angleY)]])

        rotationZ = matrix([[cos(angleY), -sin(angleY), 0],
                           [sin(angleY), cos(angleY), 0],
                           [0, 0, 1]])

        rotationMatrix = rotationZ * rotationY * rotationX

        return vector * rotationMatrix


class Mesh:
    def __init__(self, vertices, transform: Transform):
        self.transform = transform
        self.vertices = vertices


class Cube(Mesh):
    def __init__(self, transform: Transform):
        vertices = [[-1, 1, 1],
                    [-1, -1, 1],
                    [1, 1, 1],
                    [1, -1, 1],

                    [-1, 1, -1],
                    [-1, -1, -1],
                    [1, 1, -1],
                    [1, -1, -1]]

        super().__init__(vertices, transform)


class Camera:
    def __init__(self, transform: Transform, fov=90, near=0.01, far=1000):
        self.transform = transform

        self.fov = fov
        self.near = near
        self.far = far

    def project(self, mesh: Mesh):
        fov = deg2rad(self.fov)
        projectionMatrix = matrix([[1 / tan(fov / 2), 0, 0, 0],
                                  [0, 1 / tan(fov / 2), 0, 0],
                                  [0, 0, (self.far + self.near) / (self.far - self.near), 0, -1],
                                  [0, 0, 2 * self.far * self.near / (self.far - self.near), 0]])

        projectedVertices = []
        for vertex in mesh.vertices:
            newVertex = np.append(vertex, 1)
            projectedVertices.append(projectionMatrix * (newVertex - self.transform.position))

        return projectedVertices


cam = Camera(Transform([0, 0, 0, 1], [0, 0, 0], [1, 1, 1]))
cube = Cube(Transform([0, 0, -10], [0, 0, 0], [1, 1, 1]))

# print(cam.transform.position)
print(cam.project(cube))
