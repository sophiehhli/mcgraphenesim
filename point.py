import numpy as np
from scipy.stats import cosine 
import matplotlib.pyplot as plt
dx = 0.0000000000001
linelength = 2000

def_dir = np.array([-np.cos(np.pi/3), -np.sin(np.pi/5)])

#default_dir = np.array([-1,0])

class Particle(): 
	"""particle type with attributes of postition and direction"""
	def __init__(self, coords, direction = def_dir, specie= 'phonon'):
		self.coords = coords
		self.x = coords[0]
		self.y = coords[1]
		#self.fermi_cicle = fermi_circle
		self.direction = direction
		self.specie = specie

	def line_coordinates(self): 
		"""beginning and end of trajectory in a dir"""
		start_coord = self.coords + dx * self.direction/np.linalg.norm(self.direction)
		expanded_dir = linelength * self.direction
		end_coord = self.coords + expanded_dir
		line = [(start_coord[0], start_coord[1]), (end_coord[0], end_coord[1])]
		return line

	def normal(self, boundary):
		"""calculates inward normal of the boundary at the interseciton point""" 
		normal = - boundary.grad(self.x, self.y)
		return normal

	def tangent(self,boundary): 
		"""calculated tangent to the boundary and the intersection point""" 
		normal = normal(boundary)
		tangent = np.array([- normal[1], normal[0]])
		return tangent