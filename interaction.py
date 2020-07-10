from shapely.geometry import Point
from shapely.geometry import LineString
import shapely
import matplotlib
import matplotlib.pyplot as plt

import numpy as np 

import point 
import boundary
import contact

class Intersection():
	"""type with jsut corrdinates and can calculate normal and tangent"""
	def __init__(self, coordinates):
		self.coordinates = coordinates
		self.x = self.coordinates[0]
		self.y = self.coordinates[1]

	def normal(self, boundary):
		normal = - boundary.grad(self.x, self.y)
		return normal

	def tangent(self,boundary): 
		normal = normal(boundary)
		tangent = np.array([- normal[1], normal[0]])
		return tangent

def point_intersection(point, boundary): 
	"""use shapely library to calcualte tajectory/boundary intersections"""
	line_string_coord = point.line_coordinates()
	trajectory = LineString(line_string_coord)
	multipoint = trajectory.intersection(boundary.reconstructed)
	
	if isinstance(multipoint, shapely.geometry.MultiPoint)== True: 
		multiarray = [[p.x, p.y] for p in multipoint]
		if [point.x0, point.y0] in multiarray: 
			multiarray.remove([point.x0, point.y0])
		multiarray = multiarray[0]
		return multiarray
	elif isinstance(multipoint, shapely.geometry.Point) == True: 
		return [multipoint.x, multipoint.y]
	else:
		print("Could not find the intersection")
		print('Coordinate: ' + str([point.x0, point.y0]))
		print('direction: ' + str(point.direction))
	return [multipoint.x, multipoint.y]

def specular_reflection(particle, boundary, intersection):
	"""collision with boundary, specular
	returns Particle type with new direction, position at intersection"""
	odir = particle.direction
	n = intersection.normal(boundary)
	newdir = np.array(odir - 2 * (np.dot(odir,n)) * n)
	newparticle = point.Particle(intersection.x, intersection.y, newdir) 
	return newparticle

theta_data = []

def sample_cos_dis(): 
	usample = np.random.random() 
	neg = np.random.choice([-1, 1])
	theta = np.arcsin(np.sqrt(usample)) * neg
	#while np.rad2deg(theta) > 85 or np.rad2deg(theta) < -85: 
		#usample = np.random.random() 
		#neg = np.random.choice([-1, 1])
		#theta = np.arcsin(np.sqrt(usample)) * neg
	return theta 

def diffuse_reflection(n, intersection): 
	theta = sample_cos_dis()
	newdir = np.zeros(2)
	theta_data.append(theta)
	newdir[0] = np.cos(theta) * n[0] - np.sin(theta) * n[1]
	newdir[1] = np.sin(theta) * n[0] + np.cos(theta) * n[1]
	newparticle = point.Particle(intersection.x, intersection.y, newdir) 
	return newparticle

def scatter(f, point, boundary, intersection):
	if np.random.random() < f: 
		normal =  intersection.normal(boundary)
		return diffuse_reflection(normal, intersection)
	else:
		return specular_reflection(point, boundary, intersection)


def plot_trajectory(inital_point, new_point):
	"""add line connecting interaction points with line"""
	x_cords = [inital_point.x0, new_point.x0]
	y_cords = [inital_point.y0, new_point.y0]
	plt.plot(x_cords, y_cords, 'k-', lw=0.5)

def sample_cos_large_dist():
	"""sample cosine distribution for diffuse"""
	usample = np.random.random(1000) 
	theta = np.rad2deg(np.arcsin((usample)))
	mult = np.random.choice([-1,1], 1000)
	theta = np.multiply(theta, mult)
	return theta

def gen_line_point(start, end):
	'''generates a random point on a line'''
	a = [max(start[0], end[0]), max(start[1], end[1])]
	b = [min(start[0], end[0]), min(start[1], end[1])]
	x = (a[0] - b[0]) * np.random.random_sample() + b[0]
	if (start[0] - end[0]) == 0:
		y = (a[1] - b[1]) * np.random.random_sample() + b[1]
	else:
		gradient = (start[1] - end[1])/(start[0]- end[0])
		y = x * gradient
	return Intersection([x,y])

def contact_emmision(lead):
	'''diffusive emission from a random point in the contact'''
	random_point = gen_line_point(lead.start, lead.end)
	return diffuse_reflection(lead.normal, random_point)
