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
		self.name = 'circle'
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

	def lead_coordinates(self, kind, angle=1/30*np.pi):
		if kind == 's': 
			center = 0
		elif kind == 'd': 
			center = np.pi
		elif kind == 't1': 
			center = np.pi*1/2
		elif kind == 't2':
			center = np.pi*3/2 
		a1 = (center + angle/2)
		a2 = (center - angle/2)
		s = 0.05
		point_max = (self.radius-s) * np.array([np.cos(a1), np.sin(a1)])
		point_min = (self.radius-s) * np.array([np.cos(a2), np.sin(a2)])
		if kind == 's': 
			return (point_min, point_max)
		elif kind == 'd': 
			return (point_min, point_max)
		elif kind == 't1': 
			return (point_max, point_min)
		elif kind == 't2':
			return (point_max, point_min)
		

	def plot(self): 
		"""plot the implicit equation with matplotlib"""
		xspace = np.linspace(-self.radius, self.radius, 1000)
		yspace = np.linspace(-self.radius, self.radius, 1000)
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
		plt.title('Interactions by polar angle', fontsize=8)
		plt.xlabel('Theta')
		plt.ylabel('Interaction frequency')
		plt.show()

	def temperature_hist(self, list_intersections, nheater, binwidth, drain_coords, heater_coords): 
		polarthetas = [np.arctan2(c[1],c[0]) for c in list_intersections]
		heater_angles = [np.arctan2(c[1],c[0]) for c in heater_coords]
		drain_angles = [np.arctan2(c[1],c[0]) for c in drain_coords]
		#for c in polarthetas: 
			#if min(heater_angles)<= c <= max(heater_angles): 
				#polarthetas.remove(c)
			#elif min(drain_angles)<= c <= max(drain_angles): 
				#polarthetas.remove(c)
		nds, bins = np.histogram(polarthetas,  bins=100)
		Tnorm = (nds/(binwidth))/(nheater/(max(heater_angles)-min(heater_angles)))
		centers = np.array(bins[:-1] + binwidth/2)*180/np.pi
		return [centers, Tnorm]

#np.arange(0, 2*np.pi + binwidth, binwidth
class Rectangle(): 
	"""attributes of a 2D graphene rectangle""" 
	def __init__(self, length = 20, width = 2):
		self.name = 'rectangle'
		self.length = length 
		self.width = width 

		self.upperleft = [0, self.width]
		self.upperright = [self.length, self.width]
		self.lowerright = [self.length, 0]
		self.lowerleft = [0, 0]
		self.coordinates = [self.upperleft, self.upperright, self.lowerright, self.lowerleft]

		self.reconstructed = LinearRing(self.coordinates)

	def grad(self, x, y):
		if x == self.lowerleft[0]: 
			return np.array([-1, 0])
		elif x == self.lowerright[0]: 
			return np.array([1, 0])
		elif y > (self.lowerleft[1]+ self.width/2): 
			return np.array([0, 1])
		else: 
			return np.array([0, -1])

			

	def lead_coordinates(self, kind):
		if kind == 'd':
			return [self.lowerright, self.upperright]
		elif kind == 's': 
			return [self.upperleft, self.lowerleft]
		elif kind =='ld':
			return [self.lowerright, [self.lowerright[0]-5, 0]] 
		elif kind == 'ls': 
			return [[5,0], self.lowerleft]
		elif kind == 't1': 
			return [[136, 0], [131, 0]]
		elif kind == 't2': 
			return [[17, 0], [12, 0]]

	def plot(self): 
		"""plots the rectangle in matplotlib""" 
		ax = plt.gca()
		ax.set_aspect(1)
		ax.set_axisbelow(True)
		ax.add_patch(matplotlib.patches.Rectangle(self.lowerleft, self.length, self.width, fill=False, ec = 'purple'))
		plt.title('Rectagular Boundary', fontsize=8)
		plt.xlim(-5, self.length + 5)
		plt.ylim(-5, self.width + 5)
		plt.grid(linestyle='--')

	def temperature_hist(self, list_intersections, nheater, binwidth, drain, source): 
		data = []
		left_edge = 0
		right_edge = self.length

		for c in list_intersections: 
			if c[0] not in [left_edge, right_edge]: 
				data.append(c[0])

		nds, bins = np.histogram(data, bins=np.arange(left_edge, right_edge+ binwidth, binwidth))
		Tnorm = (nds/(binwidth*2))/(nheater/5)
		centers = bins[:-1] + binwidth/2
		return [centers, Tnorm]
		
