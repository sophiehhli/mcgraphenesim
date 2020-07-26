import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import datetime 

def transmitted_precent(drain, source): 
	return (drain / (drain + source))

def mean_free_path(drain, source, th_warm, th_cold, bound): 
	p_norm = drain.n_collisions/(drain.n_collisions + source.n_collisions)
	del_t_norm = th_warm.t_norm(source) - th_cold.t_norm(source)
	print(del_t_norm)
	del_x =  (th_cold.end[0]+th_cold.length) - (th_warm.end[0]+th_warm.length)
	print(del_x)
	a_cross_sec = bound.width
	a_heater = source.length
	l_mcs = 3/4 * (del_x/del_t_norm)*(a_heater/a_cross_sec)*p_norm
	return l_mcs

def save_interactions(array, bound):
	date = str(datetime.datetime.now()) 
	loc = 'data/'+bound.name+'/'
	np.savetxt(loc+bound.name+date+'.txt', array, delimiter = ' ')

def save_hist(array, bound): 
	date = str(datetime.datetime.now()) 
	loc = 'data/histograms/'
	np.savetxt(loc+bound.name+date+'hist.txt', array, delimiter = ' ')

def plot_multi_tnorm_catersian(histograms, fs, n, bound): 
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
# facecolors='none', edgecolors ='r'

def plot_theta_histogram(theta_array): 
	plt.hist(theta_array, bins ='auto')
	plt.xlabel(r'$\theta$, from normal')
	plt.ylabel('Frequency')
	plt.title(r'$\theta = sin^{-1}\sqrt{\beta}$')
	#plt.plot(1000*np.cos(np.linspace(-np.pi, np.pi, 10000)),np.linspace(-np.pi, np.pi, 10000) )
	plt.show()

def plot_theta_polar(theta_array): 
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

