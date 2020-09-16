import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import datetime 

def show_boundary(bound, contacts): 
	bound.plot()
	for c in contacts: c.plot()

def update_trajectory(particle, trajectory_array):
	if particle.intermediate_point != 'empty':
		trajectory_array.append([True, particle.intermediate_point])
	particle.intermediate_point = 'empty'
	trajectory_array.append([False, particle.coords])

def show_trajectory(points):
	color = 'black' 
	for i in range(len(points) - 1):
		x_coords = [points[i][1][0], points[i+1][1][0]]
		y_coords = [points[i][1][1], points[i+1][1][1]]
		plt.plot(x_coords, y_coords, 'k-', color = color, lw=0.5)
		color = 'black'
		if points[i+1][0]:
			color = 'green'

def show_fermi_circles(circles): 
	plots = []
	fig, ax = plt.subplots()
	for circle in circles: 
		x, y = np.transpose(circle.sample)
		plot = plt.scatter(x, y, s = 1, label = circle.name)
		plots.append(plot)
	ax.set_aspect(1)
	plt.grid(linestyle='--') 
	plt.xlabel(r'$k_x$')
	plt.ylabel(r'$k_y$')
	plt.legend(handles=plots, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small')
	plt.show()