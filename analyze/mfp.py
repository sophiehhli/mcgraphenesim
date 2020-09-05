import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import datetime 

def mean_free_path(drain, source, th_warm, th_cold, bound): 
	"""calulates the mean free path via equation 5.8 in Klitsner""" 
	p_norm = drain.n_collisions/(drain.n_collisions + source.n_collisions)
	del_t_norm = th_warm.t_norm(source) - th_cold.t_norm(source)
	del_x = ((th_cold.end[0]+th_cold.length) - (th_warm.end[0]+th_warm.length))*10**(-1)
	a_cross_sec = bound.width
	a_heater = source.length
	l_mcs = 3/4 * (del_x/del_t_norm)*(a_heater/a_cross_sec)*p_norm
	return l_mcs

def plot_inverse_mfp_from_file(file): 
	"""loads inverse mfp data from a file and plots it versus the f values""" 
	data = np.loadtxt(file)
	f = data[:, 0]
	invers_mfp = data[:, 1]
	fig = plt.figure()
	ax = fig.add_subplot(111)
	scatter = ax.scatter(f, invers_mfp, s = 10, c='darkblue')
	ax.tick_params(direction="in", right=True)
	ax.grid(ls='--')
	plt.xlabel('Diffuse Scattering Probability')
	plt.ylabel(r'Inverse Phonon Mean Free Path (cm$^{-1}$)')
	plt.show()

def plot_mfp_from_file(file): 
	"""loads mfp data from a file a plots it versus the f values""" 
	data = np.loadtxt(file)
	f = data[:, 0]
	mfp = 1/data[:, 1]
	fig = plt.figure()
	ax = fig.add_subplot(111)
	scatter = ax.scatter(f, mfp, s = 10, c='darkblue')
	ax.tick_params(direction="in", right=True)
	ax.grid(ls='--')
	plt.xlabel('Diffuse Scattering Probability')
	plt.ylabel(r'Phonon Mean Free Path (cm)')
	plt.show()

def save_inverse_mfp_data(f_list, inverse_mfp, name):
	data = np.column_stack((f_list, inverse_mfp))
	header = "f values, inverse mfp"
	loc = '.../data_mcgraphenesim/inverse_mfp/'
	np.savetxt(loc+name+'.dat', data, header = header)