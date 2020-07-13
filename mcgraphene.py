import boundary
import point
import interaction
import contact
import plotfunc

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#bound = boundary.Circle(0,0,1,1,5)
bound = boundary.Rectangle(length = 150, width = 10)

source_lead  = contact.Source(bound.lead_coordinates('s'))
drain_lead = contact.Drain(bound.lead_coordinates('d'))

list_intersections = []
source_coll = 0
drain_coll = 0

f = 0.3
n_phonon = 1
i = 1

while i <= n_phonon: 
	bound.plot()
	contact_emission = False
	curphonon = interaction.contact_emmision(source_lead)
#iterate for multiple collisions with the boundary
	num = 0
	while True: 
		# calculate intersection between ray and boundary
		intersection = interaction.Intersection(interaction.point_intersection(curphonon, bound))
		# add coordinated to the intersections array
		list_intersections.append(intersection.coordinates)
		# create new phonon travelling in new direction
		newphonon = interaction.scatter(f, curphonon, bound, intersection)
		num += 1 
		interaction.plot_trajectory(curphonon,newphonon)
		drain_collision = drain_lead.check_intersection(curphonon, bound)
		if drain_collision:
			drain_coll += 1 
			break
		source_collision = source_lead.check_intersection(curphonon, bound)
		if source_collision: 
			source_coll += 1 
			break
		curphonon = newphonon
	source_lead.plot()
	drain_lead.plot()
	i += 1
plt.show()

print('Transmitted: '+ str(plotfunc.transmitted_precent(drain_coll, source_coll))) 
binwidth = 0.5 
bound.plot_collisions(list_intersections, n_phonon, binwidth)