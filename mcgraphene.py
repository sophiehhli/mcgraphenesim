import boundary
import point
import interaction
import contact
import plotfunc
import time 

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime

#plotfunc.plot_inverse_mfp_from_file('data/inverse_mfp/aug_11_inverse_mfp.dat')
#plotfunc.plot_mfp_from_file('data/inverse_mfp/aug_11_inverse_mfp.dat')

"""choose circular or recatngular boundary by creating instance from class""" 
#bound = boundary.Circle(0,0,1,1,10)
bound = boundary.Rectangle(length = 10, width = 1)
polygon = boundary.Polygon([(0,2),(0,4),(2,4),(2,6),(4,6),(4,4),(16,4),(16,2),(14,2),(14,0),(12,0),(12,2)])

polygon.plot()
plt.show()
'''
"""create instance of the leads to include in the simulation""" 
therm_len = '0'
source = contact.Source(bound.lead_coordinates('s'))
drain = contact.Drain(bound.lead_coordinates('d'))
#th1 = contact.Thermometer(bound.lead_coordinates(therm_len+'t1'))
#th2 = contact.Thermometer(bound.lead_coordinates(therm_len+'t2'))
contacts = [source, drain]#, th1, th2] #save in list for easier access

"""parameters to be chosen for simualtion""" 
f_list = [0, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0] # f denotes probability of diffuse scattering 
n_phonon = 10**1# number of phonons to be released by the source
binwidth = 0.1 # binning for any histograms to be created

"""lists that will be added to in the course of the simulation""" 
emission_points= [] #array of interaction points at the boundary 
inverse_mfp = [] #array of the inverse mfp

plotfunc.show_boundary(bound,contacts)
# start timer for loop 
tic = time.perf_counter()
print("timer started at: "+ str(datetime.datetime.now()))
# main simuation loop 
for f in range(len(f_list)): 
	i = 1 #counter for the number of phonons released 
	fintersections = [] #list of the intersection for the f 

	while i <= n_phonon:
		"""loop until the specifed number of phonons has been released"""
		curphonon = interaction.contact_emmision(source)
		fintersections.append(curphonon.coordinates)

		while True:
			"""loop throug until phonon collides with source or drain"""
			end = False
			# collision with thermometer 1 
			#if th1.check_intersection(curphonon):
				#newphonon = th1.response(curphonon)
			# collision with thermometer 2
			#elif th2.check_intersection(curphonon):
				#newphonon = th2.response(curphonon)
			# collusion with drain lead 
			if drain.check_intersection(curphonon): 
				newphonon = drain.response(curphonon)
				#interaction.plot_trajectory(curphonon, newphonon)
				end = True #triggers end of loop 
			# collision with source lead 
			elif source.check_intersection(curphonon):
				newphonon = source.response(curphonon)
				#interaction.plot_trajectory(curphonon, newphonon)
				end = True #triggers end of loop 
			# collision with the boundary 
			else: 
				newphonon = interaction.boundary_response(f_list[f], curphonon, bound)
				#interaction.plot_trajectory(curphonon, newphonon)
			if end: 
				break # this phoonon has be absorbed by drain or source lead
			
			fintersections.append(newphonon.coordinates) #add the new phonon coordinates to the intersection points
			
			curphonon = newphonon
		
		i += 1 # add to counter of number of phonons 
		if i == n_phonon/2:
			print('50%')
	print('f = ' +str(f_list[f]) +' complete') # keep track of simulation progress 
	print('Transmitted: '+ str(plotfunc.transmitted_precent(drain.n_collisions, source.n_collisions))) #print transmission rate
	
	# caluclate mfp and append the inverse to the array for current f value 
	#mfp = plotfunc.mean_free_path(drain, source, th2, th1, bound)
	#inverse_mfp.append(1/mfp)
	
	for c in contacts: c.n_collisions = 0 #reset the collision count for the leads 
	plotfunc.save_interactions(fintersections, bound, f_list[f], therm_len, n_phonon)
	emission_points.append(fintersections) #add array of intersection to the nested array 

# end timer for the loop 
toc = time.perf_counter()
print(f"Executed loop in {toc - tic:0.4f} seconds")
plotfunc.histogram_plot_cart(emission_points, n_phonon, binwidth, source, drain, f_list, bound)
#plotfunc.save_inverse_mfp_data(f_list, inverse_mfp, "aug_11_inverse_mfp")'''