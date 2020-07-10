from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import LinearRing

import grad

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Circle():
	"""attributes of a 2D graphene circle"""
	def __init__(self, x0=0, y0=0, width=1, height=1, radius=1): 
		self.x0 = x0 
		self.y0 = y0
		self.width = width
		self.height = height 
		self.radius = radius
		# reconstruct the circle with the shapely library 
		# center point with a buffer of radius around it 
		self.center_point = Point(self.x0, self.y0)
		self.reconstructed = self.center_point.buffer(self.radius).boundary

	def equation(self,x,y): 
		"""implicit equation of boundary in x and y"""
		return ((x-self.x0)/self.width)**2 + ((y - self.y0)/self.height)**2 - self.radius**2

	def grad(self, x, y): 
		"""gradient of the dedined cicle at point (x,y)"""
		return grad.grad_circle(x, y, self.x0, self.y0, self.width, self.height)

	def lead_coordinates(self, kind, angle=6):
		if kind == 's': 
			center = 0
		if kind == 'd': 
			center = 180
		a1 = np.deg2rad(center + angle/2)
		a2 = np.deg2rad(center - angle/2)
		point_max = self.radius * np.array([np.cos(a1), np.sin(a1)])
		point_min = self.radius * np.array([np.cos(a2), np.sin(a2)])
		return (point_max, point_min)

	def plot(self): 
		"""plot the implicit equation with matplotlib"""
		xspace = np.linspace(-self.radius, self.radius, 100)
		yspace = np.linspace(-self.radius, self.radius, 100)
		X,Y = np.meshgrid(xspace,yspace)
		F = self.equation(X,Y)
		fig, ax = plt.subplots()
		ax.contour(X,Y,F,[0])
		ax.set_aspect(1)
		plt.title("Boundary", fontsize=8)
		plt.xlim(-self.radius - .25, self.radius + .25)
		plt.ylim(-self.radius - .25, self.radius + .25)
		plt.grid(linestyle='--')

	def plot_collisions(self, list_intersections): 
		polarthetas = [np.arctan(c[1]/c[0]) for c in list_intersections]
		plt.hist(polarthetas,100)
		plt.title("Interactions by polar angle", fontsize=8)
		plt.xlabel('Theta')
		plt.ylabel('Interaction frequency')
		plt.show()

class Rectangle(): 
	"""attributes of a 2D graphene rectangle""" 
	def __init__(self, length = 20, width = 2): 
		self.length = length 
		self.width = width 

		self.upperleft = [-self.length/2, self.width/2]
		self.upperright = [self.length/2, self.width/2]
		self.lowerright = [self.length/2, -self.width/2]
		self.lowerleft = [-self.length/2, -self.width/2]
		self.coordinates = [self.upperleft, self.upperright, self.lowerright, self.lowerleft]

		self.reconstructed = LinearRing(self.coordinates)

	def grad(self, x, y): 
		if y > 0: 
			return np.array([0, 1])
		else: 
			return np.array([0, -1])

	def lead_coordinates(self, kind):
		if kind == 's':
			return [self.upperright, self.lowerright]
		if kind == 'd': 
			return [self.upperleft, self.lowerleft]

	def plot(self): 
		"""plots the rectangle in matplotlib""" 
		ax = plt.gca()
		ax.set_aspect(1)
		ax.set_axisbelow(True)
		ax.add_patch(matplotlib.patches.Rectangle(self.lowerleft, self.length, self.width, fill=False, ec = 'purple'))
		plt.title("Rectagular Boundary", fontsize=8)
		plt.xlim(-self.length/2 - 1, self.length/2 + 1)
		plt.ylim(-self.width/2 - 1, self.width/2 + 1)
		plt.grid(linestyle='--')

	def plot_collisions(self, list_intersections): 
		x_vals = [c[0] for c in list_intersections]
		plt.hist(x_vals, 50)
		plt.title("Linear ditribution of interactions", fontsize=8)
		plt.xlabel('x')
		plt.ylabel('Interaction frequency')
		plt.show()
		
