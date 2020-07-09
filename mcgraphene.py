
import boundary
import point
import interaction
import contact

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

f = 0.2
# create instance of circular boundary and initial phonon
circle = boundary.Boundary(0,0,1,1,5)
intitaltheta = interaction.sample_cos_dis()
intialdir = np.array([-np.cos(intitaltheta), -np.sin(intitaltheta)])
phonon = point.Particle(direction = intialdir)


s_start, s_end = contact.circle_leads(0, 6, circle.radius)
source_lead  = contact.Source(s_start, s_end)

d_start, d_end = contact.circle_leads(180, 6, circle.radius)
drain_lead = contact.Drain(d_start, d_end)

list_intersections = []
contact_emission = False

phonon = interaction.contact_emmision(source_lead)
print([phonon.x0, phonon.y0])
curphonon = phonon

i = 0 

# plot the bounday equation
circle.plot_boundary_eq()

#iterate for multiple collisions with the boundary
while True: 
	# calculate intersection between ray and boundary
	intersection = interaction.Intersection(interaction.point_circle_intersection(curphonon, circle))
	# add coordinated to the intersections array
	#print(intersection.coordinates)
	list_intersections.append(intersection.coordinates)
	# create new phonon travelling in new direction
	if contact_emission:
		newphonon = interaction.contact_emmision(source_lead)
		contact_emission = False
	else:
		newphonon = interaction.scatter(f, curphonon, circle, intersection)
	# plot the linew betweent the current an new phonon interaction points
	interaction.plot_trajectory(curphonon,newphonon)
	drain_collision = drain_lead.check_intersection(curphonon, circle)
	if drain_collision:
		print("Collision with drain lead")
		break
	source_collision = source_lead.check_intersection(curphonon, circle)
	if source_collision: 
		contact_emission = True
		print("Collision with source lead")
	curphonon = newphonon
	i += 1
source_lead.plot()
drain_lead.plot()
plt.show()

polarthetas = [np.arctan(c[1]/c[0]) for c in list_intersections]
plt.hist(polarthetas,100)
plt.show()
#data = interaction.sample_cos_large_dist()
#plt.hist(data,100)
#plt.show()