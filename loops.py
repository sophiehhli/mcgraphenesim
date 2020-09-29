import boundary
import point
import interaction
import contact
import analyze
import time 

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime

def rectangle_loop(particle, f, bound, contacts): 
	trajectory = contacts[0].calculate_line(particle)
	for c in contacts:
		check, intersection = c.check_intersection(particle, trajectory)
		if check: 
			c.response(particle, intersection)
			if c.type in ['source','drain']:
				return True
			else: 
				return False
	interaction.boundary_response(f, particle, bound, trajectory)
	return False

def error_escape(line): 
	if line == 'error': 
		print('error sequence triggered')
		return True 

def polygon_loop(particle, f, bound, contacts): 
	line, intersection = interaction.polygon_intersection(particle, bound)
	error_escape(line)
	line = list(line.coords)
	line = list(map(list,line))
	for c in contacts: 
		if line == c.coordinates: 
			c.response(particle, intersection)
			if c.type in ['source','drain']: 
				return True
			else:
				return False
	interaction.polygon_boundary_response(f, particle, bound, line, intersection)
	return False

def initialize_f_arrays(f_emissions, f_centers, trajectory, particle, shifted_fermi_circle):
	f_emissions.append(particle.coords)
	f_centers.append(shifted_fermi_circle.center())
	trajectory.append([False, particle.coords])

def update_f_arrays(f_emissions, f_centers, particle, shifted_fermi_circle):
	f_emissions.append(particle.coords) #add the new phonon coordinates to the intersection points
	f_centers.append(shifted_fermi_circle.center())

def update_arrays(trajectories, emission_points, centers, f_trajectories, f_emissions, f_centers): 
	trajectories.append(f_trajectories)
	emission_points.append(f_emissions) #add array of intersection to the nested array 
	centers.append(f_centers)
