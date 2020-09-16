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
	"""caluclates where the a lead would fall on the ede of a circular boundary"""
	a1 = np.deg2rad(center_theta + width_theta/2)
	a2 = np.deg2rad(center_theta - width_theta/2)
	point_max = radius * np.array([np.cos(a1), np.sin(a1)])
	point_min = radius * np.array([np.cos(a2), np.sin(a2)])
	return (point_max, point_min)

def sep_xy(start, end): 
	"""rearranges the star and end coorinates of a line into x and y speratly"""
	x = [start[0], end[0]]
	y = [start[1], end[1]]
	return [x, y]

class Lead():
	def __init__(self, coordinates): 
		"""attributes of a lead""" 
		self.coordinates = coordinates
		self.start = coordinates[0]
		self.end = coordinates [1]
		self.line = LineString([tuple(self.start), tuple(self.end)])
		self.normal = -grad.grad_line(self.start, self.end)
		self.n_collisions = 0
		self.length = np.sqrt((self.start[0]-self.end[0])**2+(self.start[1]-self.end[1])**2)

	def check_intersection(self, particle):
		"""returns boolean if the the lead intersects with the path of a particle"""
		line_string_coord = particle.line_coordinates()
		trajectory = LineString(line_string_coord)
		intersection = self.line.intersection(trajectory)
		check = isinstance(intersection, shapely.geometry.Point)
		return check 

	def get_intersection(self, particle):
		"""returns intersection between lead and path of particle""" 
		line_string_coord = particle.line_coordinates()
		trajectory = LineString(line_string_coord)
		intersection = self.line.intersection(trajectory)
		return intersection
	
class Source(Lead):
	"""Source class which had methods specific for collisions with a source boundary""" 
	def __init__(self, coordinates):
		"""inherits from the Lead class""" 
		super().__init__(coordinates)
		self.type = 'source'

	def plot(self):
		"""plot the source lead in matplotlib""" 
		xandy = sep_xy(self.start, self.end)
		plt.plot(xandy[0], xandy[1], 'k-', lw=1, color='blue')

	def response(self, particle): 
		"""used if check_intersection returns true.
		output: new particle with position at intersection point,
		direcion is unchanged because the particle will be absorbed by source"""
		self.n_collisions += 1 
		intersection = self.get_intersection(particle)
		particle.coords = [intersection.x, intersection.y]

	def alternate_response(self, particle, f): 
		"""alternate response that acts like thermometer
		not called in code""" 
		intersection = self.get_intersection(particle)
		if np.random.random() < f:
			interaction.diffuse_reflection(particle.specie, self.normal, intersection)
		else:
			interaction.specular_reflection(particle, self.normal, intersection)

class Drain(Lead): 
	def __init__(self, coordinates): 
		"""inherits from the Lead class""" 
		super().__init__(coordinates)
		self.type = 'drain'

	def plot(self): 
		"""plot the drain lead in matplotlib""" 
		xandy = sep_xy(self.start, self.end)
		plt.plot(xandy[0], xandy[1], 'k-', lw=1, color='red')

	def response(self, particle): 
		"""used if check_intersection returns true.
		output: new particle with position at intersection point,
		direcion is unchanged because the particle will be absorbed by drain"""
		self.n_collisions += 1
		intersection = self.get_intersection(particle)
		particle.coords = [intersection.x, intersection.y]

class Thermometer(Lead): 
	def __init__(self, coordinates, emissivity = 0.4):
		"""inherits from the Lead class""" 
		super().__init__(coordinates)
		self.emissivity = emissivity
		self.type = 'thermometer'

	def plot(self):
		"""plot the drain lead in matplotlib""" 
		xandy = sep_xy(self.start, self.end)
		plt.plot(xandy[0], xandy[1], 'k-', lw=1, color='green')

	def response(self, particle): 
		print("thermometer response")
		"""used if collision with thermometer
		output: new particle, either specularly or diffusivly scattered""" 
		self.n_collisions += 1 
		if self.emissivity >= np.random.random():
			print("contact_emmision")
			"""diffusivly scattered from a random point on the thermometer""" 
			#initial_intersection = self.get_intersection(particle)
			#middle_particle = point.Particle([intersection.x, intersection.y])
			#uncomment line below to plot the trajectory of the particle
			#interaction.plot_trajectory(particle, middle_particle)
			interaction.contact_emmision(self, particle)
		else: 
			"""specularly scattered from the point of intersection"""
			print("specular thermometer")
			intersection_point = self.get_intersection(particle)
			print("intersection coords: " + str(intersection_point))
			intersection = point.Particle([intersection_point.x, intersection_point.y])
			print("intersection after conversion: " + str(intersection))
			interaction.specular_reflection(particle, self.normal, intersection)

	def t_norm(self, heater): 
		"""returns the normalised temperature averaged over the whole thermometer""" 
		return (self.n_collisions/self.length)/(heater.n_collisions/heater.length)
