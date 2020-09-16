import boundary 
import point
import interaction
import contact
import time 
import loops
import fermicircle
from analyze import *

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime
import time
from progress.bar import IncrementalBar

#plotfunc.plot_inverse_mfp_from_file('data/inverse_mfp/aug_11_inverse_mfp.dat')
#plotfunc.plot_mfp_from_file('data/inverse_mfp/aug_11_inverse_mfp.dat')

"""choose boundary by creating instance from class""" 
#bound = boundary.Circle(0,0,1,1,10)
#bound = boundary.Rectangle(length = 10, width = 1)
vertices = [(0,2),(0,4),(2,4),(2,6),(4,6),(4,4),(16,4),(16,2),(14,2),(14,0),(12,0),(12,2)]
vertices.reverse()
bound = boundary.Polygon(vertices)

"""create instance of the leads to include in the simulation""" 
#therm_len = '0'
source = contact.Source(bound.lead_coordinates('i+'))
drain = contact.Drain(bound.lead_coordinates('i-'))
v1 = contact.Thermometer(bound.lead_coordinates('v1'))
v2 = contact.Thermometer(bound.lead_coordinates('v2'))
print("v1 emmisvity: " + str(v1.emissivity))
#th1 = contact.Thermometer(bound.lead_coordinates(therm_len+'t1'))
#th2 = contact.Thermometer(bound.lead_coordinates(therm_len+'t2'))
contacts = [source, drain, v1, v2]#, th1, th2] #save in list for easier access

"""parameters to be chosen for simualtion""" 
f_list = [0.5] # f denotes probability of diffuse scattering 
n_phonon = 1 # number of phonons to be released by the source
binwidth = 0.1 # binning for any histograms to be created
specie = 'electron'
e_fermi = 10
n_k_vec = 8 #must be even
d_kx = 1

sample = fermicircle.gen_sample(e_fermi, n_k_vec)
centered_fermi_circle = fermicircle.Fermi_circle(sample, e_fermi)
shifted_fermi_circle = fermicircle.Fermi_circle(centered_fermi_circle.shift(d_kx), e_fermi)

"""lists that will be added to in the course of the simulation""" 
emission_points= [] #array of interaction points at the boundary 
inverse_mfp = [] #array of the inverse mfp

visual.show_boundary(bound, contacts)
# start timer for loop 
tic = time.perf_counter()
print("timer started at: "+ str(datetime.datetime.now()))
# main simuation loop 

for f in range(len(f_list)): 
	released = 1 #counter for the number of phonons released 
	fintersections = [] #list of the intersection for the f 
	bar = IncrementalBar('Progress f = '+str(f_list[f]), max = n_phonon)
	while released <= n_phonon:
		"""loop until the specifed number of phonons has been released"""
		particle = interaction.intialize_particle(source, specie, shifted_fermi_circle)
		fintersections.append(particle.coords)

		while True:
			"""loop through until phonon collides with source or drain"""
			end = False
			end = loops.polygon_loop(end, particle, f_list[f], bound, contacts) 
			fintersections.append(particle.coords) #add the new phonon coordinates to the intersection points
			if end: break
		released += 1 # add to counter of number of phonons 
		bar.next()

	print('\n Transmitted: '+ str(calculate.transmitted_precent(drain.n_collisions, source.n_collisions))) #print transmission rate
	
	# caluclate mfp and append the inverse to the array for current f value 
	#mfp = plotfunc.mean_free_path(drain, source, th2, th1, bound)
	#inverse_mfp.append(1/mfp)
	
	for c in contacts: c.n_collisions = 0 #reset the collision count for the leads 
	emission_points.append(fintersections) #add array of intersection to the nested array 

# end timer for the loop 
bar.finish()
toc = time.perf_counter()
print(f"Executed loop in {toc - tic:0.4f} seconds")
visual.show_trajectory(emission_points[0])
plt.show()
#plotfunc.histogram_plot_cart(emission_points, n_phonon, binwidth, source, drain, f_list, bound)
#plotfunc.save_inverse_mfp_data(f_list, inverse_mfp, "aug_11_inverse_mfp")