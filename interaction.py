from shapely.geometry import Point
from shapely.geometry import LineString
import shapely
import matplotlib
import matplotlib.pyplot as plt

import numpy as np 

from point import Particle
from boundary import Boundary

class Intersection():
	"""type with jsut corrdinates and can calculate normal and tangent"""
	def __init__(self, coordinates):
		self.coordinates = coordinates
		self.x = self.coordinates[0]
		self.y = self.coordinates[1]

	def normal(self, boundary):
		normal = - boundary.grad_boundary_eq_circle(self.x, self.y)
		return normal

	def tangent(self,boundary): 
		normal = normal(boundary)
		tangent = np.array([- normal[1], normal[0]])
		return tangent

def point_circle_intersection(point, circle): 
	"""use shapely library to calcualte tajectory/boundary intersections"""
	reconstructed_circle = circle.reconstructed_circle
	line_string_coord = point.line_coordinates(circle)
	trajectory = LineString(line_string_coord)
	multipoint = trajectory.intersection(reconstructed_circle)
	
	if isinstance(multipoint, shapely.geometry.MultiPoint)== True: 
		multiarray = [[p.x, p.y] for p in multipoint]
		if [point.x0, point.y0] in multiarray: 
			multiarray.remove([point.x0, point.y0])
		multiarray = multiarray[0]
		return multiarray

	if isinstance(multipoint, shapely.geometry.Point) == True: 
		return [multipoint.x, multipoint.y]
	
	if isinstance(multipoint, shapely.geometry.LineString) == True:
		print("Could not find the intersection")
		print("Position:")
		print(point.pos)
		print("Direction:")
		print(point.direction)


	return [multipoint.x, multipoint.y]

def specular_reflection(point, boundary, intersection):
	"""collision with boundary, specular
	returns Particle type with new direction, position at intersection"""
	odir = point.direction
	n = intersection.normal(boundary)
	newdir = np.array(odir - 2 * (np.dot(odir,n)) * n)
	newparticle = Particle(intersection.x, intersection.y, newdir) 
	return newparticle

theta_data = []

def sample_cos_dis(): 
	usample = np.random.random() 
	neg = np.random.choice([-1, 1])
	theta = np.arcsin(np.sqrt(usample)) * neg
	while np.rad2deg(theta) > 87 or np.rad2deg(theta) < -87: 
		usample = np.random.random() 
		neg = np.random.choice([-1, 1])
		theta = np.arcsin(np.sqrt(usample)) * neg
	return theta 

def diffuse_reflection(point, boundary, intersection): 
	theta = sample_cos_dis()
	n = intersection.normal(boundary)
	newdir = np.zeros(2)
	theta_data.append(theta)
	newdir[0] = np.cos(theta) * n[0] - np.sin(theta) * n[1]
	newdir[1] = np.sin(theta) * n[0] + np.cos(theta) * n[1]
	newparticle = Particle(intersection.x, intersection.y, newdir) 
	return newparticle

def scatter(f, point, boundary, intersection):
	if np.random.random() < f: 
		return diffuse_reflection(point, boundary, intersection)
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
	theta = np.rad2deg(np.arcsin(np.sqrt(usample)))
	mult = np.random.choice([-1,1], 1000)
	theta = np.multiply(theta, mult)
	return theta



