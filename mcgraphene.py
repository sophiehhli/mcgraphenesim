import boundary
import point
import interaction
import contact
import plotfunc
import time 

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

"""call plots unrelated to main graphene simulation""" 
#plotfunc.plot_mfp_from_file('inverse_mfp_data2.dat')

#theta_array = interaction.sample_cos_large_dist(1000000)
#plotfunc.plot_theta_polar(theta_array)

"""choose circular or recatngular boundary by creating instance from class""" 
#bound = boundary.Circle(0,0,1,1,10)
bound = boundary.Rectangle(length = 150, width = 5)

"""create instance of the leads to include in the simulation""" 
source = contact.Source(bound.lead_coordinates('ls'))
drain = contact.Drain(bound.lead_coordinates('ld'))
th1 = contact.Thermometer(bound.lead_coordinates('st1'))
th2 = contact.Thermometer(bound.lead_coordinates('st2'))
contacts = [source, drain, th1, th2] #save in list for easier access

"""parameters to be chosen for simualtion""" 
f_list = [0] # f denotes probability of diffuse scattering 
n_phonon = 1 # number of phonons to be relareased by the source

"""lists that will be added to in the course of the simulation""" 
emission_points= [] #array of interaction points at the boundary 
inverse_mfp = [] #array of the inverse mfp 

# start timer for loop 
tic = time.perf_counter()

# main simuation loop 
for f in range(len(f_list)): 
	i = 1 #counter for the number of phonons released 
	fintersections = [] #list of the intersection for the f 

	while i <= n_phonon: 
		curphonon = interaction.contact_emmision(source)
		fintersections.append(curphonon.coordinates)

		while True: 
			end = False
			# collision with thermometer 1 
			if th1.check_intersection(curphonon):
				newphonon = th1.response(curphonon)
			# collision with thermometer 2
			elif th2.check_intersection(curphonon):
				newphonon = th2.response(curphonon)
			# collusion with drain lead 
			elif drain.check_intersection(curphonon): 
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
	
	print('f = ' +str(f_list[f]) +' complete') # keep track of simulation progress 
	print('Transmitted: '+ str(plotfunc.transmitted_precent(drain.n_collisions, source.n_collisions))) #print transmission rate
	
	# caluclate mfp and append the inverse to the array for current f value 
	mfp = plotfunc.mean_free_path(drain, source, th2, th1, bound)
	inverse_mfp.append(1/mfp)
	
	for c in contacts: c.n_collisions = 0 #reset the collision count for the leads 
	
	emission_points.append(fintersections) #add array of intersection to the nested array 

# end timer for the loop 
toc = time.perf_counter()
print(f"Executed loop in {toc - tic:0.4f} seconds")

def show_boundary(bound, contacts): 
	bound.plot()
	for c in contacts: c.plot()
	plt.show()

def save_inverse_mfp_data(f_list, inverse_mfp, name):
	data = np.column_stack((f_list, inverse_mfp))
	header = "f values, inverse mfp"
	np.savetxt(name+'.dat', data, header = header)

def plot_temp_profile(emission_points, n_phonon, binwidth, source, drain, f_list, bound): 
	histograms = []
	for c in emission_points: 
		hist = bound.temperature_hist(c, n_phonon, binwidth, source, drain)
		histograms.append(hist)
	plotfunc.plot_multi_tnorm_catersian(histograms, f_list, n_phonon, bound)
	plt.show()

mfp = plotfunc.mean_free_path(drain, source, th2, th1, bound)