from shapely.geometry import Point
from shapely.geometry import LineString
import shapely

import point
import grad

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def circle_leads(center_theta, width_theta, radius):
	a1 = np.deg2rad(center_theta + width_theta/2)
	a2 = np.deg2rad(center_theta - width_theta/2)
	point_max = radius * np.array([np.cos(a1), np.sin(a1)])
	point_min = radius * np.array([np.cos(a2), np.sin(a2)])
	return (point_max, point_min)

def sep_xy(start, end): 
	x = [start[0], end[0]]
	y = [start[1], end[1]]
	return [x, y]

class Lead():
	def __init__(self, start, end): 
		self.start = start 
		self.end = end
		self.line = LineString([tuple(self.start), tuple(self.end)])
		self.normal = grad.grad_line(self.start, self.end)

	def check_intersection(self, particle, circle):
		line_string_coord = particle.line_coordinates(circle)
		trajectory = LineString(line_string_coord)
		intersection = self.line.intersection(trajectory)
		result = isinstance(intersection, shapely.geometry.Point)
		return result

class Source(Lead):
	def __init__(self, start, end):
		super().__init__(start, end)

	def plot(self):
		xandy = sep_xy(self.start, self.end)
		plt.plot(xandy[0], xandy[1], 'k-', lw=0.5, color='blue')


class Drain(Lead): 
	def __init__(self, start, end): 
		super().__init__(start, end)

	def plot(self): 
		xandy = sep_xy(self.start, self.end)
		plt.plot(xandy[0], xandy[1], 'k-', lw=0.5, color='red')
	