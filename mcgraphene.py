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
bound = boundary.Rectangle(length = 50, width = 5)
source = contact.Source(bound.lead_coordinates('ls'))
drain = contact.Drain(bound.lead_coordinates('ld'))
#th1 = contact.Thermometer(bound.lead_coordinates('t1'), emissivity=0.4) 
#th2 = contact.Thermometer(bound.lead_coordinates('t2'), emissivity=0.4)

theta_array = interaction.sample_cos_large_dist(1000000)
plotfunc.plot_theta_polar(theta_array)
#plotfunc.plot_theta_histogram(theta_array)
'''print('source normal ='+str(source.normal))
print('drain normal ='+str(drain.normal))
print('th1 normal ='+str(th1.normal))
print('th2 normal ='+str(th2.normal))'''

contacts = [source, drain]#, th1, th2]
emission_points= []

#bound.plot()
#for c in contacts: c.plot()
#plt.show()

f_list = [0, 0.05, 0.1, 0.5, 1]
n_phonon = 1

tic = time.perf_counter()

for f in range(len(f_list)): 
	i = 0
	fintersections = []
	while i <= n_phonon: 
		#bound.plot()
		curphonon = interaction.contact_emmision(source)
		fintersections.append(curphonon.coordinates)
		while True: 
			end = False
			#if th1.check_intersection(curphonon):
				#print("t1 collision")
				#newphonon = th1.response(curphonon)
				#print(newphonon.coordinates)
				#print(newphonon.direction)
			#elif th2.check_intersection(curphonon):
				#print("t2 collision")
				#newphonon = th2.response(curphonon)
				#print(newphonon.coordinates)
				#print(newphonon.direction)
			if drain.check_intersection(curphonon):
				#print("drain")	 
				newphonon = drain.response(curphonon)
				#interaction.plot_trajectory(curphonon, newphonon)
				end = True
			elif source.check_intersection(curphonon):
				#print("source") 
				newphonon = source.response(curphonon)#,f_list[f])
				#interaction.plot_trajectory(curphonon, newphonon)
				end = True
			else: 
				newphonon = interaction.boundary_response(f_list[f], curphonon, bound)
				#print("boundary")
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
plt.show()

binwidth = 0.1
histograms = []
for c in emission_points: 
	hist = bound.temperature_hist(c, n_phonon, binwidth, bound.lead_coordinates('d'), bound.lead_coordinates('s'))
	histograms.append(hist)
plotfunc.plot_multi_tnorm_catersian(histograms, f_list, n_phonon)

plt.show()
#plotfunc.save_hist(hist[0], bound)
#plotfunc.save_hist(hist[1], bound)