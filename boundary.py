from shapely.geometry import Point
from shapely.geometry import LineString

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Boundary():
	"""define the attributed that a boundary type has
	   respresnts the boundary of the graphene flake"""
	def __init__(self, x0=0, y0=0, width=1, height=1, radius=1): 
		self.x0 = x0 
		self.y0 = y0
		self.width = width
		self.height = height 
		self.radius = radius
		# reconstruct the circle with the shapely library 
		# center point with a buffer of radius around it 
		self.center_point = Point(self.x0, self.y0)
		self.reconstructed_circle = self.center_point.buffer(self.radius).boundary

	def boundary_eq(self,x,y): 
		"""implicit equation of boundary in x and y"""
		return ((x-self.x0)/self.width)**2 + ((y - self.y0)/self.height)**2 - self.radius**2

	def grad_boundary_eq_circle(self, x, y): 
		"""gradient of the dedined cicle at point (x,y)"""
		v = np.zeros(2)
		v[0] = 2*(x-self.x0)*(1/self.width**2)
		v[1] = 2*(y-self.y0)*(1/self.height**2)
		return v/np.linalg.norm(v)

	def plot_boundary_eq(self): 
		"""plot the implicit equation with matplotlib"""
		xspace = np.linspace(-self.radius, self.radius, 100)
		yspace = np.linspace(-self.radius, self.radius, 100)
		X,Y = np.meshgrid(xspace,yspace)
		F = self.boundary_eq(X,Y)
		fig, ax = plt.subplots()
		ax.contour(X,Y,F,[0])
		ax.set_aspect(1)
		plt.title("Boundary", fontsize=8)
		plt.xlim(-self.radius - .25, self.radius + .25)
		plt.ylim(-self.radius - .25, self.radius + .25)
		plt.grid(linestyle='--')
