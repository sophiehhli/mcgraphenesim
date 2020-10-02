from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import LinearRing
import shapely

import grad

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Circle():
	def __init__(self, x0=0, y0=0, width=1, height=1, radius=1): 
		"""attributes of a 2D graphene circle"""
		self.name = 'circle'
		self.x0 = x0 
		self.y0 = y0
		self.width = width
		self.height = height 
		self.radius = radius
		self.center_point = Point(self.x0, self.y0)
		self.reconstructed = self.center_point.buffer(self.radius).boundary

	def equation(self,x,y): 
		"""implicit equation of boundary in x and y"""
		return ((x-self.x0)/self.width)**2 + ((y - self.y0)/self.height)**2 - self.radius**2

	def grad(self, x, y): 
		"""calls function to calculate the gradient of the cicle at point (x,y)"""
		return grad.grad_circle(x, y, self.x0, self.y0, self.width, self.height)

	def lead_coordinates(self, kind, angle=1/30*np.pi):
		"""returns the lead coordinates depending kind of lead to be constructed"""
		if kind == 's': 
			#source lead 
			center = 0
		elif kind == 'd': 
			#drain lead 
			center = np.pi
		elif kind == 't1': 
			#top thermometer 
			center = np.pi*1/2
		elif kind == 't2':
			#bottom thermometer 
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
		"""plot the implicit equation of the circle boundary with matplotlib"""
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
		"""plots the collision by theta"""
		polarthetas = [np.arctan(c[1]/c[0]) for c in list_intersections]
		plt.hist(polarthetas,100)
		plt.title('Interactions by polar angle', fontsize=8)
		plt.xlabel('Theta')
		plt.ylabel('Interaction frequency')
		plt.show()

	def temperature_hist(self, list_intersections, nheater, binwidth, drain_coords, heater_coords): 
		"""plots the temperaure profile around the circle"""
		polarthetas = [np.arctan2(c[1],c[0]) for c in list_intersections]
		heater_angles = [np.arctan2(c[1],c[0]) for c in heater_coords]
		drain_angles = [np.arctan2(c[1],c[0]) for c in drain_coords]
		nds, bins = np.histogram(polarthetas,  bins=100)
		Tnorm = (nds/(binwidth))/(nheater/(max(heater_angles)-min(heater_angles)))
		centers = np.array(bins[:-1] + binwidth/2)*180/np.pi
		return [centers, Tnorm]


class Rectangle():  
	def __init__(self, length = 20, width = 2):
		"""attributes of a 2D graphene rectangle"""
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
		"""calculates the gradient of the reactangle depending on the point"""
		if x == self.lowerleft[0]: 
			return np.array([-1, 0])
		elif x == self.lowerright[0]: 
			return np.array([1, 0])
		elif y > (self.lowerleft[1]+ self.width/2): 
			return np.array([0, 1])
		else: 
			return np.array([0, -1])

	def lead_coordinates(self, kind):
		"""different options for the coordinates of different leads"""
		if kind == 'd':
			# drain lead on the vertical edge 
			return [self.lowerright, self.upperright]
		elif kind == 's': 
			# source lead on the vertical edge 
			return [self.upperleft, self.lowerleft]
		elif kind =='ld':
			# drain lead on the horizontal edge
			return [self.lowerright, [self.lowerright[0]-5, 0]] 
		elif kind == 'ls': 
			# source lead on the horizontal edge 
			return [[3,0], self.lowerleft]
		elif kind == '5t1': 
			# 5mm thermometer near drain 
			return [[131, 0], [136, 0]]
		elif kind == '5t2': 
			# 5mm thermometer near source 
			return [[12, 0], [17, 0]]
		elif kind == '3t1': 
			# 3mm thermometer near drain 
			return [[132, 0], [135, 0]]
		elif kind == '3t2': 
			# 3mm thermoemter near source
			return [[13, 0], [16, 0]]
		elif kind == '1t1': 
			# 1mm thermometer near drain 
			return [[134, 0], [135, 0]]
		elif kind == '1t2': 
			# 1mm thermoemter near source
			return [[13, 0], [14, 0]]

	def plot(self): 
		"""plots the rectangle in matplotlib""" 
		ax = plt.gca()
		ax.set_aspect(1)
		ax.set_axisbelow(True)
		ax.add_patch(matplotlib.patches.Rectangle(self.lowerleft, self.length, self.width, fill=False, ec = 'purple'))
		plt.title('Rectangular boundary, 5 mm thermometers', fontsize=8)
		plt.xlim(-5, self.length + 5)
		plt.ylim(-5, self.width + 5)
		plt.grid(linestyle='--')
		plt.xlabel("x (mm)")
		plt.ylabel("y (mm)")

	def temperature_hist(self, list_intersections, nheater, binwidth, source, drain): 
		""" converts the number of collisions on a specific section to temperature profile"""
		data = []
		left_edge = self.lowerleft[0]
		right_edge = self.lowerright[0]-self.lowerleft[0]

		for c in list_intersections: 
			if c[0] not in [left_edge, right_edge]:
				data.append(c[0])

		nds, bins = np.histogram(data, bins=np.arange(left_edge, right_edge + binwidth, binwidth))
		
		Tnorm = (nds/(binwidth*2))/(nheater/source.length)
		
		centers = bins[:-1] + binwidth/2
		return [centers, Tnorm]
		
class Polygon():
	def __init__(self, vertices): 
		"""attributes of a 2D polygon"""
		self.name = 'polygon'
		self.vertices = vertices
		self.n_vertices = len(vertices)
		self.reconstructed = shapely.geometry.Polygon(vertices)
		self.xy_sep_lines = self.xy_sep_lines()
		self.lines_coords = self.line_coords()
		self.construct_lines = [LineString(coord) for coord in self.lines_coords]
		self.x_max = self.min_max()[0][0]
		self.y_max = self.min_max()[0][1]
		self.x_min = self.min_max()[1][0]
		self.y_min = self.min_max()[1][1]

	def grad(self, line): 
		start, end = line
		return grad.grad_line(start, end)

	def min_max(self):
		x = [lst[0] for lst in self.vertices]
		y = [lst[1] for lst in self.vertices]
		return[[max(x), max(y)], [min(x), min(y)]]
	
	def xy_sep_lines(self): 
		lines = []
		for i in range(len(self.vertices)):
			if i == len(self.vertices)-1: 
				x = [self.vertices[i][0], self.vertices[0][0]]
				y = [self.vertices[i][1], self.vertices[0][1]]
			else: 
				x = [self.vertices[i][0], self.vertices[i+1][0]]
				y = [self.vertices[i][1], self.vertices[i+1][1]]
			lines.append([x,y])
		return lines

	def line_coords(self): 
		lines = []
		for i in range(len(self.vertices)):
			if i == len(self.vertices)-1: 
				start_end = [self.vertices[i], self.vertices[0]]
			else: 
				start_end = [self.vertices[i], self.vertices[i+1]]
			lines.append(start_end)
		return lines

	def plot(self): 
		ax = plt.gca()
		ax.set_aspect(1)
		for i in self.xy_sep_lines: 
			plt.plot(i[0], i[1], color='purple')
		edge = 1
		plt.xlim(self.x_min-edge, self.x_max+edge) 
		plt.ylim(self.y_min-edge, self.y_max+edge)
		plt.grid(linestyle='--')
		plt.xlabel("x")
		plt.ylabel("y")

	def lead_coordinates(self, kind):
		"""different options for the coordinates of different leads"""
		if kind == 'i+':
			# source lead on the vertical edge 
			return [[0,4],[0,2]]
		if kind == 'i-': 
			return [[4,6], [2,6]]
		if kind == 'v2': 
			return [[16,2], [16,4]]
		if kind == 'v1': 
			return [[12,0], [14,0]]
		if kind == 'lv2':
			return [[64,2], [64,4]]
		if kind == 'lv1': 
			return [[60,0], [62, 0]]