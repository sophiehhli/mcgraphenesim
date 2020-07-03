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

	def norm_tan(self, boundary):
		inward_norm = - boundary.grad_boundary_eq_circle(self.x, self.y)
		tangent = np.array([- inward_norm[1], inward_norm[0]])
		return np.array([inward_norm, tangent])

def point_circle_intersection(point, circle): 
	"""use shapely library to calcualte tajectory/boundary intersections"""
	reconstructed_circle = circle.reconstructed_circle
	line_string_coord = point.line_coordinates(circle)
	trajectory = LineString(line_string_coord)
	multipoint = trajectory.intersection(reconstructed_circle)
	return [multipoint.x, multipoint.y]

def specular_reflection(point, boundary, intersection):
	"""collision with boundary, specular
	returns Particle type with new direction, position at intersection"""
	nandt = intersection.norm_tan(boundary)
	odir = point.direction
	n = nandt[0]
	newdir = np.array(odir - 2*(np.dot(odir,n))*n)
	newparticle = Particle(intersection.x, intersection.y, newdir) 
	return newparticle

def plot_trajectory(inital_point, new_point):
	"""add line connecting interaction points with line"""
	x_cords = [inital_point.x0, new_point.x0]
	y_cords = [inital_point.y0, new_point.y0]
	plt.plot(x_cords, y_cords,'k-', lw=0.5)

def sample_cos_dist():
		"""sample cosine distribution for diffuse"""
		usample = np.random.random(1000) 
		theta = np.rad2deg(np.arcsin(np.sqrt(usample)))
		mult = np.random.choice([-1,1],1000)
		theta = np.multiply(theta,mult)
		return theta

def diffuse_reflection(point, boundary, intersection): 
	n = intersection.norm_tan(boundary)[0]
	ndir = np.zeros(2)
	usample = np.random.random() 
	mult = np.random.choice([-1,1])
	theta = np.arcsin(np.sqrt(usample))*mult
	ndir[0] = np.cos(theta) * n[0] - np.sin(theta) * n[1]
	ndir[1] = np.sin(theta) * n[0] + np.cos(theta) * n[1]
	newparticle = Particle(intersection.x, intersection.y, ndir) 
	return newparticle

def scatter(f, point, boundary, intersection):
	if np.random.random()< f: 
		return diffuse_reflection(point, boundary, intersection)
	else:
		return specular_reflection(point, boundary, intersection)

