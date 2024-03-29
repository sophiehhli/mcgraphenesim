import boundary
import point
import interaction
import contact
import time
import loops
import fermicircle
import atombeamsim
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
#bound = boundary.Rectangle(length = 150, width = 10)
vertices = [(0,2),(0,4),(2,4),(2,6),(4,6),(4,4),(64,4),(64,2),(62,2),(62,0),(60,0),(60,2)]
vertices.reverse()
#shortvertices = [(0,2),(0,4),(2,4),(2,6),(4,6),(4,4),(16,4),(16,2),(14,2),(14,0),(12,0),(12,2)]
#shortvertices.reverse()
# %% codecell
import numpy as np
tup = (1,2)
list(tup)
# %% codecell

sheets = 30
length = 30
diameter = 3
tolerance = 0
angle = 90

vertices = atombeamsim.get_vertices_angled(tolerance, diameter, length, sheets, angle)
bound = boundary.Polygon(vertices)

# %% codecell
"""parameters to be chosen for simualtion"""
f_list = [0.03] # f denotes probability of diffuse scattering
emissivity = 0.4
n_particle = 10000 # number of phonons to be released by the source
binwidth = 0.1 # binning for any histograms to be created
specie = 'phonon'
#e_fermi = 10
#n_k_vec = n_particle #must be even
#d_kx = 1

lower = 0
upper = 16
nbins = 100

"""create instance of the leads to include in the simulation"""
#therm_len = '0'
source_coords = [list(vertices[0]),list(vertices[-1])]
drain_coords = [list(vertices[2*sheets-1]),list(vertices[2*sheets])]
source_coords.reverse()

# %% codecell
source = contact.Source(source_coords)
drain = contact.Drain(drain_coords)
#v1 = contact.Thermometer(bound.lead_coordinates('v1'), emissivity)
#v2 = contact.Thermometer(bound.lead_coordinates('v2'), emissivity)
#th1 = contact.Thermometer(bound.lead_coordinates(therm_len+'t1'))
#th2 = contact.Thermometer(bound.lead_coordinates(therm_len+'t2'))
contacts = [source, drain]#, v1, v2]#, th1, th2] #save in list for easier access

#sample = fermicircle.gen_sample(e_fermi, n_k_vec)
#centered_fermi_circle = fermicircle.Fermi_circle(sample, e_fermi, "Equilibrium")
#shifted_fermi_circle = fermicircle.Fermi_circle(centered_fermi_circle.shift(d_kx), e_fermi, "Non-Equilibrium")
#unchanged_shifted_fermi_circle = fermicircle.Fermi_circle(centered_fermi_circle.shift(d_kx), e_fermi, "Shifted, Unchanged")

#original_center = centered_fermi_circle.center()

#isual.show_fermi_circles([centered_fermi_circle])

"""lists that will be added to in the course of the simulation"""
emission_points = [] #array of interaction points at the boundary
trajectories = []
inverse_mfp = [] #array of the inverse mfp
centers = []
success_array = []
#k_vectors = []

visual.show_boundary(bound, contacts)
plt.show()
# start timer for loop
tic = time.perf_counter()
print("timer started at: "+ str(datetime.datetime.now()))
# main simuation loop

for f in range(len(f_list)):# --------- loop of f values ---------

	released = 0 #counter for the number of phonons released
	f_emissions = [] #list of the intersection for the f
	f_centers = []
	f_trajectories = []
	f_k_vectors = []
	bar = IncrementalBar('Progress f = '+str(f_list[f]), max = n_particle)

	while released < n_particle:
		"""loop until the specifed number of phonons has been released"""
		trajectory = []
		particle = interaction.intialize_particle(source, specie, released)
		loops.initialize_f_arrays(f_emissions, f_centers, trajectory, particle)
		#f_k_vectors.append(particle.fermi_circle.sample[released])
		drain_collisions = drain.n_collisions

		while True:
			"""loop through until phonon collides with source or drain"""
			end = False
			end = loops.polygon_loop(particle, f_list[f], bound, contacts)
			#f_k_vectors.append(particle.fermi_circle.sample[released])
			visual.update_trajectory(particle, trajectory)
			loops.update_f_arrays(f_emissions, f_centers, particle)
			if end: break

		if drain.n_collisions > drain_collisions:
			success_array.append(True)
		else:
			success_array.append(False)
		released += 1

		#visual.show_boundary(bound, contacts)
		#visual.show_trajectory(trajectory)
		#plt.show()
		#visual.show_fermi_circles([centered_fermi_circle, shifted_fermi_circle])
		#plt.show()
		f_trajectories.append(trajectory)
		bar.next()
		# ------------------
	print('\n Transmitted: '+ str(calculate.transmitted_precent(drain.n_collisions, source.n_collisions))) #print transmission rate

	# caluclate mfp and append the inverse to the array for current f value
	#mfp = plotfunc.mean_free_path(drain, source, th2, th1, bound)
	#inverse_mfp.append(1/mfp)

	for c in contacts: c.n_collisions = 0 #reset the collision count for the leads
	loops.update_arrays(trajectories, emission_points, centers, f_trajectories, f_emissions, f_centers)
	#k_vectors.append(f_k_vectors)
	# ------------------
# end timer for the loop
bar.finish()
toc = time.perf_counter()
print(f"Executed loop in {toc - tic:0.4f} seconds")
#visual.show_fermi_circles([centered_fermi_circle, unchanged_shifted_fermi_circle, shifted_fermi_circle])
#plt.show()
#print(trajectories)
#analyze_fermicircle.save_array(k_vectors[0], f_list[0], emissivity, n_particle, 'k_vectors')
#analyze_fermicircle.save_array(emission_points[0], f_list[0], emissivity, n_particle, 'emissions')
#analyze_fermicircle.plot_deviations_length(original_center, centers[0], emission_points[0], 2, 14)
#for i in [0, 9, 19, 29, 39, 49]:
	#analyze_fermicircle.plot_circle_at_point(k_vectors[0], emission_points[0], 0, 64, 50, i)
#analyze_fermicircle.fermi_circles_from_kvectors(original_center, k_vectors[0], emission_points[0], 0, 64, 50)

angle_array = atombeamsim.get_exit_angle_array(trajectories, success_array)

with open('angle_array_smooth.npy', 'wb') as f:
	np.save(f, angle_array)
# t_profiles.plot_theta_polar(angle_array)
#k_vectors_04 = np.loadtxt('../data_mcgraphenesim/k_vectors/2020-10-02_f0.06__e0.4_100000.dat')
#emissions_04 = np.loadtxt('../data_mcgraphenesim/emissions/2020-10-02_f0.06__e0.4_100000.dat')
#k_vectors_003 = np.loadtxt('../data_mcgraphenesim/k_vectors/2020-10-02_f0.03__e0.4_100000.dat')
#emissions_003 = np.loadtxt('../data_mcgraphenesim/emissions/2020-10-02_f0.03__e0.4_100000.dat')

#middles_ratios_04 = analyze_fermicircle.convert_to_middles_ratios(k_vectors_04, emissions_04, lower, upper, nbins, e_fermi)
#middles_ratios_003 = analyze_fermicircle.convert_to_middles_ratios(k_vectors_003, emissions_003, lower, upper, nbins, e_fermi)

#data_arrays = [middles_ratios_04, middles_ratios_003]

#analyze_fermicircle.plot_ratio_on_unshifted(data_arrays, [[0.06, 0.4], [0.03, 0.4]])

#middle_ratios = analyze_fermicircle.convert_to_middles_ratios(k_vectors[0], emission_points[0], lower, upper, nbins, e_fermi)
#analyze_fermicircle.plot_ratio_on_unshifted([middle_ratios])
#plotfunc.histogram_plot_cart(emission_points, n_phonon, binwidth, source, drain, f_list, bound)
#plotfunc.save_inverse_mfp_data(f_list, inverse_mfp, "aug_11_inverse_mfp")
