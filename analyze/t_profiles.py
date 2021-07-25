import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime

def save_interactions(array, bound,f,therm_len,n_phonon):
	"""saves the interaction points in a file"""
	date = str(datetime.date.today())
	loc = '../data_mcgraphenesim/'+bound.name+'/'
	fstr = '_f'+str(f)+'_'
	length = '_'+therm_len+'mm'
	name = loc+date+length+fstr+str(n_phonon)+'.dat'
	np.savetxt(name, array)

def save_hist(array, bound, f):
	"""saves the historgam data in a file"""
	date = str(datetime.date.today())
	loc = '../data_mcgraphenesim/histograms'+bound.name+'/'
	fstr = '_f'+str(f)+'_'
	length = '_'+therm_len+'mm'
	name = loc+date+length+fstr+str(n_phonon)+'.dat'
	np.savetxt(name, array)

def plot_tnorm_cartesian(histograms, fs, n, bound):
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

def plot_tnorm_polar(histograms, fs, n):
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

def histogram_plot_cart(emission_points, n_phonon, binwidth, source, drain, f_list, bound):
	"""first produces the histogram values and then plots each historgram, for cartesian"""
	histograms = []
	for c in emission_points:
		hist = bound.temperature_hist(c, n_phonon, binwidth, source, drain)
		histograms.append(hist)
	plot_tnorm_cartesian(histograms, f_list, n_phonon, bound)
	plt.savefig("fig10remake_aug_10.png")
	plt.show()

def histogram_plot_polar(emission_points, n_phonon, binwidth, source, drain, f_list, bound):
	"""first produces the histogram values and then plots each historgram, for polar """
	histograms = []
	for c in emission_points:
		hist = bound.temperature_hist(c, n_phonon, binwidth, source, drain)
		histograms.append(hist)
	plot_tnorm_polar(histograms, f_list, n_phonon, bound)
	plt.savefig("fig10remake_aug_10.png")
	plt.show()

def plot_theta_distribution(theta_array):
	n, bins = np.histogram(theta_array, bins = "auto")
	binwidth = bins[1] - bins [0]
	theta = np.linspace(-np.pi/2, np.pi/2, 10000)
	r = np.cos(np.abs(theta))*max(n)
	fig, ax = plt.subplots()
	# ax.plot(theta, r, label=r'$cos(\theta)$')
	ax.scatter(bins[:-1]+binwidth/2, n/max(n), c="green", s=5)
	ax.set_ylabel(r"$j(\theta)$")
	ax.set_xlabel(r"$\theta$ (rad)")
	plt.show()

def plot_theta_polar(theta_array):
	"""a polar plot of points, compared to cosine(theta)"""
	n, bins = np.histogram(theta_array, bins = "auto")
	binwidth = bins[1] - bins[0]
	theta = np.linspace(-np.pi/2, np.pi/2, 10000)
	r = np.cos(np.abs(theta))
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='polar')
	b = ax.plot(theta, r, label=r'$cos(\theta)$')
	c = ax.scatter(bins[:-1]+binwidth/2, n/max(n), c='green', s=5, label='Distribution')
	ax.set_thetamin(-90)
	ax.set_thetamax(90)
	ax.set_theta_zero_location('N')
	ax.set_ylim(0, 1)

	ax.legend()
	plt.show()
