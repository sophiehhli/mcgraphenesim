import numpy as np
from scipy.stats import cosine 
import matplotlib.pyplot as plt
dx = 0.0000000000001
linelength = 2000

default_dir = np.array([-np.cos(np.pi/3), -np.sin(np.pi/5)])
#default_dir = np.array([-1,0])

class Particle(): 
	"""particle type with attributes of postition and direction"""
	def __init__(self, x0 = 5, y0 = 0, direction = default_dir):
		self.x0 = x0
		self.y0 = y0
		self.coordinates = [self.x0, self.y0]
		self.direction = direction
		self.pos = np.array([self.x0, self.y0])

	def line_coordinates(self): 
		"""beginning and end of trajectory in a dir"""
		start_coord = self.pos + dx * self.direction/np.linalg.norm(self.direction)
		expanded_dir = linelength * self.direction
		end_coord = self.pos + expanded_dir
		line = [(start_coord[0], start_coord[1]), (end_coord[0], end_coord[1])]
		return line

	def diffuse_reflection(): 
		

class Phonon(Particle): 
	def __init__(self, x, y, direction): 
		"""inherits from the Particle class""" 
		super().__init__(x, y, direction)

class Electron(Particle):
	def __init__(self, x, y, direction, k_vector):
		"""inherits from the Particle class""" 
		super().__init__(x, y, direction)
		self.k_vector = k_vector