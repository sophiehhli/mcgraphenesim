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

def plot_multi_tnorm(histograms, fs, n): 
	fig, ax = plt.subplots()
	plots = []
	for i in range(len(histograms)):
		f = ax.scatter(histograms[i][0], histograms[i][1], s=1, label = '$f = $'+ str(fs[i]))
		plots.append(f)
	plt.title("Normalized temperature profile, $N_{phonons}$ = "+str(n), fontsize=8)
	plt.xlabel('x (mm)')
	plt.ylabel('$T^4_{norm}(x)$')
	plt.legend(handles = plots, loc='upper right', bbox_to_anchor=(0., 1.02, 1., .102))
	ax.tick_params(direction="in", right=True)
	#plt.show()

# facecolors='none', edgecolors ='r'