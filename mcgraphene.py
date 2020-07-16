import boundary
import point
import interaction
import contact
import plotfunc
import time 

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


#bound = boundary.Circle(0,0,1,1,10)
bound = boundary.Rectangle(length = 150, width = 5)

source = contact.Source(bound.lead_coordinates('s'))

drain = contact.Drain(bound.lead_coordinates('d'))

th1 = contact.Thermometer(bound.lead_coordinates('t1'), emissivity=0.4) 

th2 = contact.Thermometer(bound.lead_coordinates('t2'), emissivity=0.4)

contacts = [source, drain]
emission_points= []

f_list = [0,0.03]
n_phonon = 100000
tic = time.perf_counter()
for f in range(len(f_list)): 
	i = 1
	fintersections = []
	while i <= n_phonon: 
		#bound.plot()
		curphonon = interaction.contact_emmision(source)
		while True: 
			end = False
			if th1.check_intersection(curphonon):
				newphonon = th1.response(curphonon)
			elif th2.check_intersection(curphonon):
				newphonon = th2.response(curphonon)
			if drain.check_intersection(curphonon): 
				newphonon = drain.response(curphonon)
				#interaction.plot_trajectory(curphonon, newphonon)
				end = True
			elif source.check_intersection(curphonon): 
				newphonon = source.response(curphonon)
				#interaction.plot_trajectory(curphonon, newphonon)
				end = True
			else: 
				newphonon = interaction.boundary_response(f_list[f], curphonon, bound)
				#interaction.plot_trajectory(curphonon, newphonon)
			if end: 
				break 
			fintersections.append(newphonon.coordinates)
			curphonon = newphonon
		#for c in contacts: c.plot()
		i += 1
	emission_points.append(fintersections)
	print('Transmitted: '+ str(plotfunc.transmitted_precent(drain.n_collisions, source.n_collisions)))
	#plotfunc.save_interactions(list_intersections[f], bound)
toc = time.perf_counter()
print(f"Executed loop in {toc - tic:0.4f} seconds")
#plt.show()

binwidth = 0.5 
histograms = []
for c in emission_points: 
	hist = bound.temperature_hist(c, n_phonon, binwidth, bound.lead_coordinates('d'), bound.lead_coordinates('s'))
	histograms.append(hist)
plotfunc.plot_multi_tnorm(histograms, f_list, n_phonon)

plt.show()
#plotfunc.save_hist(hist[0], bound)
#plotfunc.save_hist(hist[1], bound)