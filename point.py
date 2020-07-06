import numpy as np
from scipy.stats import cosine 
import matplotlib.pyplot as plt
import boundary
dx = 0.000000000001
linelength = 10

default_dir = np.array([-np.cos(np.pi/3), -np.sin(np.pi/5)])
#default_dir = np.array([-1,0])

class Particle(): 
	"""particle type with attributes of postition and direction"""
	def __init__(self, x0 = 5, y0 = 0, direction = default_dir):
		self.x0 = x0
		self.y0 = y0
		self.direction = direction
		self.pos = np.array([self.x0, self.y0])

	def line_coordinates(self, circle): 
		"""beginning and end of trajectory in a dir
		   for now it is arbitrarily long so interacition point is found"""
		start_coord = self.pos + dx * self.direction/np.linalg.norm(self.direction)
		expanded_dir = circle.radius * linelength * self.direction
		end_coord = self.pos + expanded_dir
		line = [(start_coord[0], start_coord[1]), (end_coord[0], end_coord[1])]
		#x_cords = [start_coord[0], end_coord[0]]
		#y_cords = [start_coord[1], end_coord[1]]
		#plt.plot(x_cords, y_cords, 'k-', lw=0.5)
		return line
