import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import datetime 

def transmitted_precent(drain, source): 
	return (drain / (drain + source))

def plot_tnorm(centers, tnorm, f, n): 
	fig, ax = plt.subplots()
	scat = ax.scatter(centers, tnorm, s=1, label = '$f = $'+ str(f), facecolors='none', edgecolors='black')
	plt.title("Normalized temperature profile, $N_{phonons}$ = "+str(n), fontsize=8)
	plt.xlabel('x (mm)')
	plt.ylabel('$T^4_{norm}(x)$')
	plt.legend(handles = [scat], loc='upper right', bbox_to_anchor=(0., 1.02, 1., .102))
	ax.tick_params(direction="in", right=True)
	plt.show()

def save_interactions(array, bound):
	date = str(datetime.datetime.now()) 
	loc = 'data/'+bound.name+'/'
	np.savetxt(loc+bound.name+date+'.txt', array, delimiter = ' ')

def save_hist(array, bound): 
	date = str(datetime.datetime.now()) 
	loc = 'data/histograms/'
	np.savetxt(loc+bound.name+date+'hist.txt', array, delimiter = ' ')

def plot_multi_tnorm_catersian(histograms, fs, n): 
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
	#plt.show()

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
	plt.ylim(0,1)
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
	binwidth = bins[1] - bins[1]
	theta = np.linspace(-np.pi/2, np.pi/2, 10000)
	r = np.cos(theta)*max(n)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='polar')
	b = ax.plot(theta, r, label=r'$cos(\theta)$')
	c = ax.scatter(bins[:-1]+binwidth/2, n, c=n, s=10, alpha=0.75, label='Distribution')
	ax.set_thetamin(-90)
	ax.set_thetamax(90)
	ax.set_theta_zero_location('N')
	ax.set_ylim(0, max(n)+max(n)/100)
		
	ax.legend()
	plt.show()
