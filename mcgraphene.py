import boundary
import point
import interaction
import contact
import plotfunc

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

f = 0.2
# create instance of circular boundary and initial phonon
bound = boundary.Circle(0,0,1,1,5)
bound = boundary.Rectangle(length = 30, width = 1)

bound.plot()

source_lead  = contact.Source(bound.lead_coordinates('s'))
drain_lead = contact.Drain(bound.lead_coordinates('d'))

list_intersections = []
contact_emission = False

curphonon = interaction.contact_emmision(source_lead)

#iterate for multiple collisions with the boundary
while True: 
	# calculate intersection between ray and boundary
	intersection = interaction.Intersection(interaction.point_intersection(curphonon, bound))
	# add coordinated to the intersections array
	#print(intersection.coordinates)
	list_intersections.append(intersection.coordinates)
	# create new phonon travelling in new direction
	if contact_emission:
		newphonon = interaction.contact_emmision(source_lead)
		contact_emission = False
	else:
		newphonon = interaction.scatter(f, curphonon, bound, intersection)
	# plot the linew betweent the current an new phonon interaction points
	interaction.plot_trajectory(curphonon,newphonon)
	drain_collision = drain_lead.check_intersection(curphonon, bound)
	if drain_collision:
		print("Collision with drain lead")
		break
	source_collision = source_lead.check_intersection(curphonon, bound)
	if source_collision: 
		contact_emission = True
		print("Collision with source lead")
		break
	curphonon = newphonon

source_lead.plot()
drain_lead.plot()
plt.show()

bound.plot_collisions(list_intersections)

#data = interaction.sample_cos_large_dist()
#plt.hist(data,100)
#plt.show()