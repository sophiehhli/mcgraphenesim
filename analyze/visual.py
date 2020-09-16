import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import datetime 

def show_boundary(bound, contacts): 
	bound.plot()
	for c in contacts: c.plot()

def show_trajectory(points): 
	for i in range(len(points) - 1): 
		x_coords = [points[i][0], points[i+1][0]]
		y_coords = [points[i][1], points[i+1][1]]
		plt.plot(x_coords, y_coords, 'k-', lw=0.5)

def update_trajectories(particle, trajectory_array):
	if particle.intermediate_point != 'empty':
		trajectory_array.append([True, particle.intermediate_point])
	particle.intermediate_point = 'empty'
	trajectory_array.append([False, particle.coords])

def show_alternate_trajectory(points):
	color = 'black' 
	for i in range(len(points) - 1):
		x_coords = [points[i][1][0], points[i+1][1][0]]
		y_coords = [points[i][1][1], points[i+1][1][1]]
		plt.plot(x_coords, y_coords, 'k-', color = color, lw=0.5)
		color = 'black'
		if points[i+1][0]:
			color = 'green'