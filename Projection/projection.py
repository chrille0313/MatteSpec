import pygame
import numpy as np
from numpy import array, sin, cos, tan, deg2rad, rad2deg


class Transform:
    """
    A component to keep track of the transform of an object (position, rotation, scale).
    Every object that exists in the "world" will inherit from this.
    """

    def __init__(self, position, rotation, scale):
        self._pos = array(position)
        self._rot = array(rotation)
        self._scale = array(scale)

        self.forward = 0
        self.up = 0
        self.right = 0
        self.__calculate_local_vectors()

        # self.transformMatrix = 0
        # self.rotationMatrix = 0

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, newPos):
        self._pos = array(newPos)

    @property
    def rotation(self):
        return self._rot

    @rotation.setter
    def rotation(self, newRot):
        self._rot = newRot
        self.__calculate_local_vectors()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, newScale):
        self._scale = newScale

    def __calculate_local_vectors(self, worldUp=None):
        worldUp = [0, 1, 0] if worldUp is None else worldUp

        self.forward = self.rotate(array([0, 0, 1]), self.rotation)
        self.right = np.cross(self.forward, worldUp)
        self.up = np.cross(self.right, self.forward)

    @staticmethod
    def rotate(vector, angles):
        angleX, angleY, angleZ = deg2rad(angles)

        rotationX = array([[1, 0, 0],
                           [0, cos(angleX), -sin(angleX)],
                           [0, sin(angleX), cos(angleX)]])

        rotationY = array([[cos(angleY), 0, sin(angleY)],
                           [0, 1, 0],
                           [-sin(angleY), 0, cos(angleY)]])

        rotationZ = array([[cos(angleY), -sin(angleY), 0],
                           [sin(angleY), cos(angleY), 0],
                           [0, 0, 1]])

        rotationMatrix = np.dot(rotationZ, np.dot(rotationY, rotationX))

        return np.dot(vector, rotationMatrix)


class Face:
    def __init__(self):
        pass


class Mesh:
    """
    A mesh consists of vertices that make up "faces" (triangles) of an object.
    """

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

        vertices *= transform.scale

        for i in range(len(vertices)):
            vertices[i] = transform.rotate(vertices[i], transform.rotation)

        super().__init__(vertices, transform)


class Camera:
    """
    A camera with the ability to render a mesh from its perspective.
    """

    def __init__(self, transform: Transform, fov=90, near=0.01, far=1000):
        self.transform = transform

        self.fov = fov
        self.near = near
        self.far = far

        self.viewingTransform = array([[1 / np.tan(np.deg2rad(fov / 2)), 0, 0, 0],
                                       [0, 1 / np.tan(np.deg2rad(fov / 2)), 0, 0],
                                       [0, 0, (self.far + self.near) / (self.far - self.near), -1],
                                       [0, 0, 2 * self.far * self.near / (self.far - self.near), 0]])

    def project(self, mesh: Mesh):
        rotationX = array([[1, 0, 0, 0], 
                              [0, np.cos(np.deg2rad(self.transform.rotation[0])), -np.sin(np.deg2rad(self.transform.rotation[0])), 0],
                              [0, np.sin(np.deg2rad(self.transform.rotation[0])), np.cos(np.deg2rad(self.transform.rotation[0])), 0],
                              [0, 0, 0, 1]])

        rotationY = array([[np.cos(np.deg2rad(self.transform.rotation[1])), 0, -np.sin(np.deg2rad(self.transform.rotation[1])), 0],
                              [0, 1, 0, 0],
                              [np.sin(np.deg2rad(self.transform.rotation[1])), 0, np.cos(np.deg2rad(self.transform.rotation[1])), 0],
                              [0, 0, 0, 1]])

        rotationZ = array([[-np.cos(np.deg2rad(self.transform.rotation[2])), -np.sin(np.deg2rad(self.transform.rotation[2])), 0, 0],
                              [np.sin(np.deg2rad(self.transform.rotation[2])), np.cos(np.deg2rad(self.transform.rotation[2])), 0, 0],
                              [0, 0, 1, 0], 
                              [0, 0, 0, 1]])

        rotation = np.dot(rotationX, np.dot(rotationY, rotationZ))

        projectedVertices = []
        for vertex in mesh.vertices:
            newVertex = np.append(vertex, 1)
            relativeVertex = np.dot(rotation, newVertex - self.transform.position)
            projectedVertex = np.dot(self.viewingTransform, relativeVertex)
            projectedVertex /= projectedVertex[3]
            projectedVertices.append(projectedVertex)

        return projectedVertices

    def display(self, mesh: Mesh):
        pass


cam = Camera(Transform([0, 0, -2, 1], [0, 0, 0], [1, 1, 1]))
cube = Cube(Transform([0, 0, 0], [0, 0, 0], [1, 1, 1]))


pygame.init()

window = pygame.display.set_mode((800, 800))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0, 0, 0))

    for vertex in cam.project(cube):
        surfaceTransform = array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [400, 400, 1, 1]])

        x = np.dot(vertex, surfaceTransform)
        pygame.draw.circle(window, (255, 255, 255), x[:2], 3)

    # print(cam.transform.right, cam.transform.up, cam.transform.forward)

    pygame.display.update()
    # break
