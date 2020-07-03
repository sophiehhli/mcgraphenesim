
import boundary
import point
import interaction

import matplotlib
import matplotlib.pyplot as plt

# create instance of circular boundary and initial phonon
circle = boundary.Boundary(0,0,1,1,5)
phonon = point.Particle()

list_intersections = []

curphonon = phonon

i = 0 

# plot the bounday equation
circle.plot_boundary_eq()

#iterate for multiple collisions with the boundary
while i < 35: 
	# calculate intersection between ray and boundary
	intersection = interaction.Intersection(interaction.point_circle_intersection(curphonon, circle))
	# add coordinated to the intersections array
	#print(intersection.coordinates)
	list_intersections.append(intersection.coordinates)
	# create new phonon travelling in new direction
	newphonon= interaction.specular_reflection(curphonon, circle, intersection)
	# plot the linew betweent the current an new phonon interaction points
	interaction.plot_trajectory(curphonon,newphonon)
	curphonon = newphonon
	i += 1

plt.show()