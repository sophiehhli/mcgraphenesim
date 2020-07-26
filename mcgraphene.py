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

source = contact.Source(bound.lead_coordinates('ls'))
drain = contact.Drain(bound.lead_coordinates('ld'))
th1 = contact.Thermometer(bound.lead_coordinates('st1'))
th2 = contact.Thermometer(bound.lead_coordinates('st2'))

#theta_array = interaction.sample_cos_large_dist(1000000)
#plotfunc.plot_theta_polar(theta_array)

contacts = [source, drain, th1, th2]
emission_points= []

f_list = [0, 0.03]#0.00, 0.02, 0.05, 0.1, 0.2, 0.5, 1]
n_phonon = 10000

tic = time.perf_counter()

for f in range(len(f_list)): 
	i = 0
	fintersections = []
	while i <= n_phonon: 
		curphonon = interaction.contact_emmision(source)
		fintersections.append(curphonon.coordinates)
		while True: 
			end = False
			if th1.check_intersection(curphonon):
				#print("t1 collision")
				newphonon = th1.response(curphonon)
			elif th2.check_intersection(curphonon):
				#print("t2 collision")
				newphonon = th2.response(curphonon)
			elif drain.check_intersection(curphonon):
				#print("drain")	 
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

bound.plot()
for c in contacts: c.plot()
plt.show()

toc = time.perf_counter()

print(f"Executed loop in {toc - tic:0.4f} seconds")

binwidth = 0.5
histograms = []

for c in emission_points: 
	hist = bound.temperature_hist(c, n_phonon, binwidth, source, drain)
	histograms.append(hist)

plotfunc.plot_multi_tnorm_catersian(histograms, f_list, n_phonon, bound)

plt.show()

mfp = plotfunc.mean_free_path(drain, source, th2, th1, bound)
print('Mean Free Path = '+str(mfp))