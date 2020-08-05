import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import datetime 

def transmitted_precent(drain, source): 
	"""calulates the precentage of particles transmitted to the drain""" 
	return (drain / (drain + source))

def mean_free_path(drain, source, th_warm, th_cold, bound): 
	"""calulates the mean free path via equation 5.8 in Klitsner""" 
	p_norm = drain.n_collisions/(drain.n_collisions + source.n_collisions)
	del_t_norm = th_warm.t_norm(source) - th_cold.t_norm(source)
	del_x = ((th_cold.end[0]+th_cold.length) - (th_warm.end[0]+th_warm.length))*10**(-1)
	a_cross_sec = bound.width
	a_heater = source.length
	l_mcs = 3/4 * (del_x/del_t_norm)*(a_heater/a_cross_sec)*p_norm
	return l_mcs

def save_interactions(array, bound):
	"""saves the interaction points in a file""" 
	date = str(datetime.datetime.now()) 
	loc = 'data/'+bound.name+'/'
	np.savetxt(loc+bound.name+date+'.txt', array, delimiter = ' ')

def save_hist(array, bound): 
	"""saves the historgam data in a file""" 
	date = str(datetime.datetime.now()) 
	loc = 'data/histograms/'
	np.savetxt(loc+bound.name+date+'hist.txt', array, delimiter = ' ')

def plot_multi_tnorm_catersian(histograms, fs, n, bound): 
	"""plots the tempetaure profile of multiple f values on the same plot
	suitable for boundaries best represented in cartesian coordinates"""
	fig, ax = plt.subplots()
	plots = []
	for i in range(len(histograms)):
		f = ax.scatter(histograms[i][0], histograms[i][1], s=1, label = '$f = $'+ str(fs[i]))
		plots.append(f)
	plt.title("Normalized temperature profile, $N_{phonons}$ = "+str(n), fontsize=8)
	plt.xlabel('x (mm)')
	plt.ylabel('$T^4_{norm}(x)$')
	plt.legend(handles = plots, loc='upper right')#, bbox_to_anchor=(0., 1.02, 1., .102))
	ax.tick_params(direction="in", right=True)
	ax.set_ylim(0,1)
	ax.set_xlim(0,bound.length)

def plot_multi_tnorm_polar(histograms, fs, n): 
	"""plots the the temperature profile of multiple f values on the same plot
	suitable for boundaries best represented in polar coordinates""" 
	fig, ax = plt.subplots()
	plots = []
	for i in range(len(histograms)):
		f = ax.scatter(histograms[i][0], histograms[i][1], s=1, label = '$f = $'+ str(fs[i]))
		plots.append(f)
	plt.title("Normalized temperature profile, $N_{phonons}$ = "+str(n), fontsize=8)
	plt.xlabel(r'$\theta (\degree)$')
	plt.ylabel('$T^4_{norm}(x)$')
	plt.legend(handles = plots, loc='upper right')#, bbox_to_anchor=(0., 1.02, 1., .102))
	ax.tick_params(direction="in", right=True)


def plot_theta_polar(theta_array): 
	"""a polar plot of points, compared to cosine(theta)"""
	n, bins = np.histogram(theta_array, bins = "auto")
	binwidth = bins[1] - bins[0]
	theta = np.linspace(-np.pi/2, np.pi/2, 10000)
	r = np.cos(np.abs(theta))*max(n)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='polar')
	b = ax.plot(theta, r, label=r'$cos(\theta)$')
	c = ax.scatter(bins[:-1]+binwidth/2, n, c='green', s=10, alpha=0.75, label='Distribution')
	ax.set_thetamin(-90)
	ax.set_thetamax(90)
	ax.set_theta_zero_location('N')
	ax.set_ylim(0, max(n)+max(n)/100)

	ax.legend()
	plt.show()

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