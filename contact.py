from shapely.geometry import Point
from shapely.geometry import LineString
import shapely

import point
import grad
import interaction

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
	def __init__(self, coordinates): 
		self.coordinates = coordinates
		self.start = coordinates[0]
		self.end = coordinates [1]
		self.line = LineString([tuple(self.start), tuple(self.end)])
		self.normal = -grad.grad_line(self.start, self.end)
		self.n_collisions = 0

	def check_intersection(self, particle):
		line_string_coord = particle.line_coordinates()
		trajectory = LineString(line_string_coord)
		intersection = self.line.intersection(trajectory)
		check = isinstance(intersection, shapely.geometry.Point)
		return check 

	def get_intersection(self, particle):
		line_string_coord = particle.line_coordinates()
		trajectory = LineString(line_string_coord)
		intersection = self.line.intersection(trajectory)
		return intersection
	
class Source(Lead):
	def __init__(self, coordinates):
		super().__init__(coordinates)

	def plot(self):
		xandy = sep_xy(self.start, self.end)
		plt.plot(xandy[0], xandy[1], 'k-', lw=1, color='blue')

	def response(self, particle): 
		self.n_collisions += 1 
		intersection = self.get_intersection(particle)
		return point.Particle(intersection.x, intersection.y)

	def alternate_response(self, particle, f): 
		intersection = self.get_intersection(particle)
		if np.random.random() < f:
			return interaction.diffuse_reflection(self.normal, intersection)
		else:
			return interaction.c_specular_reflection(particle, self.normal, intersection)

class Drain(Lead): 
	def __init__(self, coordinates): 
		super().__init__(coordinates)

	def plot(self): 
		xandy = sep_xy(self.start, self.end)
		plt.plot(xandy[0], xandy[1], 'k-', lw=1, color='red')

	def response(self, particle): 
		self.n_collisions += 1
		intersection = self.get_intersection(particle)
		return point.Particle(intersection.x, intersection.y)

class Thermometer(Lead): 
	def __init__(self, coordinates, emissivity = 0.3):
		super().__init__(coordinates)
		self.emissivity = emissivity

	def plot(self):
		xandy = sep_xy(self.start, self.end)
		plt.plot(xandy[0], xandy[1], 'k-', lw=1, color='green')

	def response(self, particle): 
		self.n_collisions += 1 
		if self.emissivity >= np.random.random():
			intersection = self.get_intersection(particle)
			middle_particle = point.Particle(intersection.x, intersection.y)
			#interaction.plot_trajectory(particle, middle_particle)
			newphoton = interaction.contact_emmision(self)
			return newphoton
		else: 
			intersection = self.get_intersection(particle)
			return interaction.c_specular_reflection(particle, self.normal, intersection)
