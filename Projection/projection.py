import pygame
import numpy as np
from numpy import array, sin, cos, tan, deg2rad, rad2deg
from vector3d import Vector3D


class Transform:
	"""
    A component to keep track of the transform of an object (position, rotation, scale).
    Every object that exists in the "world" will inherit from this.
    """

	def __init__(self, position: Vector3D, rotation: Vector3D, scale: Vector3D):
		self._pos = position
		self._rot = rotation
		self._scale = scale

		self.transformMatrix = np.zeros((4, 4))
		self.rotationMatrix = np.zeros((4, 4))
		self.worldToLocalMatrix = np.zeros((4, 4))
		self.localToWorldMatrix = np.zeros((4, 4))
		self.__calculate_matrices()

		self.forward = Vector3D.forward
		self.up = Vector3D.up
		self.right = Vector3D.right
		self.__calculate_local_vectors()

	@property
	def position(self):
		return self._pos

	@position.setter
	def position(self, newPos: Vector3D):
		self._pos = newPos
		self.__calculate_matrices()

	@property
	def rotation(self):
		return self._rot

	@rotation.setter
	def rotation(self, newRot: Vector3D):
		self._rot = newRot
		self.__calculate_matrices()
		self.__calculate_local_vectors()

	@property
	def scale(self):
		return self._scale

	@scale.setter
	def scale(self, newScale: Vector3D):
		self._scale = newScale
		self.__calculate_matrices()

	def __calculate_local_vectors(self):
		self.forward = self.rotate(-Vector3D.forward, self.rotation).normalized
		self.up = self.rotate(Vector3D.up, self.rotation).normalized
		self.right = self.forward.cross(self.up).normalized

		print(self.forward, self.up, self.right)

	def __calculate_matrices(self):
		rotation = self.__get_rotation_matrix(self.rotation)

		scale = np.array([[self.scale.x, 0, 0, 0],
		                  [0, self.scale.y, 0, 0],
		                  [0, 0, self.scale.z, 0],
		                  [0, 0, 0, 1]])

		translation = np.array([[1, 0, 0, 0],
		                        [0, 1, 0, 0],
		                        [0, 0, 1, 0],
		                        [self.position.x, self.position.y, self.position.z, 1]])

		self.rotationMatrix = rotation
		self.transformMatrix = np.array([[1, 0, 0, 0],
		                                 [0, 1, 0, 0],
		                                 [0, 0, 1, 0],
		                                 [-self.position.x, -self.position.y, -self.position.z, 1]])

		self.worldToLocalMatrix = np.dot(self.rotationMatrix, self.transformMatrix)
		self.localToWorldMatrix = np.dot(np.dot(self.rotationMatrix, scale), translation)

	@staticmethod
	def rotate(vector: Vector3D, angles: Vector3D):
		rotationX = array([[1, 0, 0],
		                   [0, cos(angles.x), sin(angles.x)],
		                   [0, -sin(angles.x), cos(angles.x)]])

		rotationY = array([[cos(angles.y), 0, -sin(angles.y)],
		                   [0, 1, 0],
		                   [sin(angles.y), 0, cos(angles.y)]])

		rotationZ = array([[cos(angles.z), sin(angles.z), 0],
		                   [-sin(angles.z), cos(angles.z), 0],
		                   [0, 0, 1]])

		rotationMatrix = np.dot(rotationX, np.dot(rotationY, rotationZ))

		return Vector3D(*np.dot(vector[:3], rotationMatrix))

	@staticmethod
	def __get_rotation_matrix(angles: Vector3D):
		rotationX = np.array([[1, 0, 0, 0],
		                      [0, cos(deg2rad(angles.x)), sin(deg2rad(angles.x)), 0],
		                      [0, -sin(deg2rad(angles.x)), cos(deg2rad(angles.x)), 0],
		                      [0, 0, 0, 1]])

		rotationY = np.array([[cos(deg2rad(angles.y)), 0, -sin(deg2rad(angles.y)), 0],
		                      [0, 1, 0, 0],
		                      [sin(deg2rad(angles.y)), 0, cos(deg2rad(angles.y)), 0],
		                      [0, 0, 0, 1]])

		rotationZ = np.array([[cos(deg2rad(angles.z)), sin(deg2rad(angles.z)), 0, 0],
		                      [-sin(deg2rad(angles.z)), cos(deg2rad(angles.z)), 0, 0],
		                      [0, 0, 1, 0],
		                      [0, 0, 0, 1]])

		return np.dot(rotationX, np.dot(rotationY, rotationZ))


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
	"""
	An example use of a mesh
	"""
	def __init__(self, transform: Transform):
		baseVertices = [Vector3D(-1, 1, 1),
		                Vector3D(-1, -1, 1),
		                Vector3D(1, 1, 1),
		                Vector3D(1, -1, 1),

		                Vector3D(-1, 1, -1),
		                Vector3D(-1, -1, -1),
		                Vector3D(1, 1, -1),
		                Vector3D(1, -1, -1)]

		vertices = []
		for vertex in baseVertices:
			worldVertex = Vector3D(*np.dot(vertex, transform.localToWorldMatrix))
			worldVertex.w = 1
			vertices.append(vertex)

		super().__init__(vertices, transform)


class Camera:
	"""
    A camera with the ability to render a mesh from its perspective.
    """

	def __init__(self, transform: Transform, fov=90, movementSpeed=0.1, rotationSpeed=0.1, near=0.001, far=1000):
		self.transform = transform

		self.fov = fov
		self.near = near
		self.far = far

		self.movementSpeed = movementSpeed
		self.rotationSpeed = rotationSpeed

		self.viewingTransform = array([[1 / tan(deg2rad(fov / 2)), 0, 0, 0],
		                               [0, 1 / tan(deg2rad(fov / 2)), 0, 0],
		                               [0, 0, (self.far + self.near) / (self.far - self.near), -1],
		                               [0, 0, 2 * self.far * self.near / (self.far - self.near), 0]])

	def project(self, mesh: Mesh):
		projectedVertices = []
		for vertex in mesh.vertices:
			relativeVertex = np.dot(vertex, self.transform.worldToLocalMatrix)  # Transform vertex into local camera space
			projectedVertex = Vector3D(*np.dot(self.viewingTransform, relativeVertex))  # Project vertex into image space
			projectedVertex /= projectedVertex.w  # Omg 4th dimension o_O
			projectedVertices.append(projectedVertex)

		return projectedVertices

	def render(self, screenSize):
		pygame.init()
		windowW, windowH = screenSize
		window = pygame.display.set_mode(screenSize)
		running = True

		isKeyDown = pygame.key.get_pressed()

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or isKeyDown[pygame.K_ESCAPE]:
					running = False

				elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
					isKeyDown = pygame.key.get_pressed()

			# Movement of camera in local orientation
			if isKeyDown[pygame.K_w]:
				self.transform.position += self.transform.forward * self.movementSpeed
			if isKeyDown[pygame.K_s]:
				self.transform.position += -self.transform.forward * self.movementSpeed

			if isKeyDown[pygame.K_d]:
				self.transform.position += -self.transform.right * self.movementSpeed
			if isKeyDown[pygame.K_a]:
				self.transform.position += self.transform.right * self.movementSpeed

			if isKeyDown[pygame.K_SPACE]:
				self.transform.position += self.transform.up * self.movementSpeed
			if isKeyDown[pygame.K_LCTRL]:
				self.transform.position += -self.transform.up * self.movementSpeed

			if isKeyDown[pygame.K_q]:
				self.transform.rotation += Vector3D(0, 0, -1) * self.rotationSpeed
			if isKeyDown[pygame.K_e]:
				self.transform.rotation += Vector3D(0, 0, 1) * self.rotationSpeed

			window.fill((0, 0, 0))  # Clear screen

			for vertex in cam.project(cube):
				screenSpaceTransform = array([[1, 0, 0, 0],
				                              [0, 1, 0, 0],
				                              [0, 0, 1, 0],
				                              [windowW / 2, windowH / 2, 0, 1]])

				screenSpaceVertex = np.dot(vertex, screenSpaceTransform)  # Center the vertex on the screen ((0,0) is top left)
				pygame.draw.circle(window, (255, 255, 255), screenSpaceVertex[:2], 3)  # We are now in screen-space -> forget about z and w

			pygame.display.update()


cam = Camera(Transform(Vector3D(0, 0, 2), Vector3D(0, 0, 0), Vector3D(1, 1, 1)), movementSpeed=0.001)
cube = Cube(Transform(Vector3D(0, 0, 0), Vector3D(0, 0, 0), Vector3D(1, 1, 1)))

cam.render((800, 800))
