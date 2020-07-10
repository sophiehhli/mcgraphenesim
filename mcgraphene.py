import boundary
import point
import interaction
import contact
import plotfunc

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

f = 0.03
# create instance of circular boundary and initial phonon
# bound = boundary.Circle(0,0,1,1,5)
bound = boundary.Rectangle(length = 30, width = 1)


source_lead  = contact.Source(bound.lead_coordinates('s'))
drain_lead = contact.Drain(bound.lead_coordinates('d'))

print(source_lead.coordinates)
print(drain_lead.coordinates)
list_intersections = []
source_lead_collisions = 0
drain_lead_collisions = 0

n_phonon = 10000
i = 1
while i <= n_phonon: 
	#bound.plot()
	contact_emission = False
	curphonon = interaction.contact_emmision(source_lead)
	print('particle released: ' + str(i))
	print('Coordinate: ' + str([curphonon.x0, curphonon.y0]))
	print('direction: ' + str(curphonon.direction))
	while curphonon.direction[0] > 0.999 or curphonon.direction[0] < -0.999: 
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
			if newphonon.x0 == 15.0: 
				source_lead_collisions += 1 
				#print("Collision with source lead")
				break
			if newphonon.x0 == -15.0: 
				drain_lead_collisions += 1 
				#print("Collision with source lead")
				break
		else:
			newphonon = interaction.scatter(f, curphonon, bound, intersection)
			if newphonon.x0 == 15.0: 
				source_lead_collisions += 1 
				#print("Collision with source lead")
				break
			if newphonon.x0 == -15.0: 
				drain_lead_collisions += 1 
				#print("Collision with source lead")
				break
		# plot the linew betweent the current an new phonon interaction points
		#interaction.plot_trajectory(curphonon,newphonon)
		'''drain_collision = drain_lead.check_intersection(curphonon, bound)
		if drain_collision:
			drain_lead_collisions += 1 
			#print("Collision with drain lead")
			break
		source_collision = source_lead.check_intersection(curphonon, bound)
		if source_collision: 
			contact_emission = True
			source_lead_collisions += 1 
			#print("Collision with source lead")
			break'''
		curphonon = newphonon

	#source_lead.plot()
	#drain_lead.plot()

	i += 1
print('Transmitted: '+ str(drain_lead_collisions/(source_lead_collisions + drain_lead_collisions)*100)) 
plt.show()
bound.plot_collisions(list_intersections)

#data = interaction.sample_cos_large_dist()
#plt.hist(data,100)
#plt.show()