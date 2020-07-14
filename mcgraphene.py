import boundary
import point
import interaction
import contact
import plotfunc

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#bound = boundary.Circle(0,0,1,1,5)
bound = boundary.Rectangle(length = 150, width = 5)

source_lead  = contact.Source(bound.lead_coordinates('s'))
drain_lead = contact.Drain(bound.lead_coordinates('d'))
th1 = contact.Thermometer([[131, 0], [136, 0]])
th2 = contact.Thermometer([[12, 0], [17, 0]])

list_intersections = []
source_coll = 0
drain_coll = 0
th1_coll = 0 
th2_coll = 0

f_list = [0.03]
n_phonon = 1

for f in range(len(f_list)): 
	i = 1
	fintersections = []
	while i <= n_phonon: 
		bound.plot()
		curphonon = interaction.contact_emmision(source_lead)
		num = 0
		while True: 
			intersection = interaction.Intersection(interaction.point_intersection(curphonon, bound))
			fintersections.append(intersection.coordinates)
			th1_collision = th1.check_intersection(curphonon, bound)
			th2_collision = th2.check_intersection(curphonon, bound)
			if th1_collision or th2_collision: 
				newphonon = interaction.scatter(1, curphonon, bound, intersection)
			else: 
				newphonon = interaction.scatter(f_list[f], curphonon, bound, intersection)
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
		th1.plot()
		th2.plot()
		i += 1
	list_intersections.append(fintersections)
	print('Transmitted: '+ str(plotfunc.transmitted_precent(drain_coll, source_coll)))
	#plotfunc.save_interactions(list_intersections[f], bound)
plt.show()

binwidth = 0.5 
histograms = []
for l in list_intersections: 
	hist = bound.temperature_hist(l, n_phonon, binwidth)
	histograms.append(hist)
#plotfunc.plot_multi_tnorm(histograms, f_list, n_phonon)
#th1.plot()
#th2.plot()
#plt.show()
#plotfunc.save_hist(hist[0], bound)
#plotfunc.save_hist(hist[1], bound)