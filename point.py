import numpy as np
from scipy.stats import cosine 

import boundary

default_dir = np.array([-np.cos(np.pi/3), -np.sin(np.pi/5)])
#default_dir = np.array([-1,0])

class Particle(): 
	"""particle type with attributes of postitiona and direction"""
	def __init__(self, x0 = 3, y0 = 0, direction = default_dir):
		self.x0 = x0
		self.y0 = y0
		self.direction = direction
		self.pos = np.array([self.x0, self.y0])

	def line_coordinates(self, circle): 
		"""beginning and end of trajectory in a dir
		   for now it is arbitrarily long so interacition point is found"""
		start_coord = self.pos
		expanded_dir = circle.radius * 2 * self.direction
		end_coord = start_coord + expanded_dir
		line = [(start_coord[0],start_coord[1]), (end_coord[0], end_coord[1])]
		return line
