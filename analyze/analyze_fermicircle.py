import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import datetime 

def convert_to_center(vector_set): 
	x_mean = np.mean(np.array(vector_set)[:,0])
	y_mean = np.mean(np.array(vector_set)[:,1])
	return [x_mean, y_mean]

def convert_to_deviation(original, centers):
	distances = []
	print('length centers: '+str(len(centers)))
	for center in centers: 
		distance = np.sqrt((original[0]-center[0])**2 + (original[1]-center[1])**2)
		distances.append(distance)
	return distances

def construct_data_set(emissions, deviations, lower, upper): 
	x_values = []
	y_values = []
	for i in range(len(emissions)): 
		if emissions[i][0] > lower and emissions[i][0] < upper:
			x_values.append(emissions[i][0]) 
			y_values.append(deviations[i])
	return [x_values, y_values]

def construct_horizontal_data_set(emissions, deviations, lower, upper): 
	x_values  = []
	y_values = []
	for i in range(len(emissions)): 
		test_range = lower < emissions[i][0] < upper
		test_verticle = emissions[i][0] not in [2, 4, 12, 14]
		if test_range and test_verticle:
			x_values.append(emissions[i][0]) 
			y_values.append(deviations[i])
	return [x_values, y_values]

def plot_deviations_length(original, centers, emissions, lower, upper):
	deviations = convert_to_deviation(original, centers)
	x,y = construct_data_set(emissions, deviations, lower, upper)
	fig, ax = plt.subplots()
	plt.scatter(x, y, s=1)
	plt.xlabel("Length from emission (cm)")
	plt.ylabel("Fermi circle deviation from unshifted")
	plt.show()

def binning(x, y, nbins, lower, upper):
	bins = np.linspace(lower, upper, nbins)
	x = np.array(x)
	ind = np.digitize(x, bins)
	sorted_into_bins = [[] for i in range(nbins-1)]
	for i in range(len(y)): 
		n_list = ind[i] - 1
		sorted_into_bins[n_list].append(y[i])
	return [bins, sorted_into_bins]

def get_bin_middles(upper, lower, nbins, bins): 
	binwidth = (upper-lower)/nbins 
	middles = bins[:-1]+binwidth/2
	return middles

def find_list_mean(sorted_into_bins):
	means = [np.mean(sublist) for sublist in sorted_into_bins]
	return means

def plot_binned_deviations(original, centers, emissions, lower, upper, nbins): 
	deviations = convert_to_deviation(original, centers)
	x,y = construct_data_set(emissions, deviations, lower, upper)
	bins, sorted_into_bins = binning(x, y, nbins, lower, upper)
	means = find_list_mean(sorted_into_bins)
	middles = get_bin_middles(upper, lower, nbins, bins)
	fig, ax = plt.subplots()
	plt.scatter(middles, means, s=1)
	plt.xlabel("Length from emission (cm)")
	plt.ylabel("Fermi circle deviation form unshifted")
	plt.show()

def fermi_circles_from_kvectors(original, k_vectors, emissions, lower, upper, nbins):
	x, y = construct_data_set(emissions, k_vectors, lower, upper)
	bins, sorted_into_bins = binning(x, y, nbins, lower, upper)
	centers =[]
	for vector_set in sorted_into_bins: 
		center = convert_to_center(vector_set)
		centers.append(center)
	deviations = convert_to_deviation(original, centers)
	middles = get_bin_middles(upper,lower, nbins, bins)
	fig, ax = plt.subplots()
	plt.scatter(middles, deviations, s=1)
	plt.xlabel("Length from emission (cm)")
	plt.ylabel("Fermi circle deviation form unshifted")
	plt.show()

def plot_circle_at_point(k_vectors, emissions, lower, upper, nbins, show_nbin): 
	x,y = construct_data_set(emissions, k_vectors, lower, upper)
	bins, sorted_into_bins = binning(x, y, nbins, lower, upper)
	vector_set = sorted_into_bins[show_nbin]
	start = str(bins[show_nbin])
	end = str(bins[show_nbin + 1])
	x, y = np.transpose(vector_set)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.scatter(x, y, s = 1)
	ax.set_aspect(1)
	plt.grid(linestyle='--') 
	plt.title("k-vectors measured from "+start+" to "+end)
	plt.xlabel(r'$k_x$')
	plt.ylabel(r'$k_y$')
	plt.show()

def plot_ratio_on_unshifted(k_vectors, emissions, lower, upper, nbins, efermi): 
	x,y = construct_data_set(emissions, k_vectors, lower, upper)
	bins, sorted_into_bins = binning(x, y, nbins, lower, upper)
	ratios = []
	for vector_set in sorted_into_bins: 
		unshifted = 0 
		for vector in vector_set: 
			radius = vector[0]**2 + vector[1]**2
			upperbound = efermi**2 + 0.00005
			lowerbound = efermi**2 - 0.00005
			if lowerbound <= radius <= upperbound: 
				unshifted += 1
		ratio = unshifted/len(vector_set)
		ratios.append(ratio)
	middles = get_bin_middles(upper, lower, nbins, bins)
	fig, ax = plt.subplots()
	plt.scatter(middles, ratios, s = 1)
	plt.xlabel("Length from emission")
	plt.ylabel("Ratio of k-vectors on the centered fermi circle")
	plt.show()

def plot_absolute_on_unshifted(k_vectors, emissions, lower, upper, nbins, efermi): 
	x,y = construct_horizontal_data_set(emissions, k_vectors, lower, upper)
	bins, sorted_into_bins = binning(x, y, nbins, lower, upper)
	absolutes = []
	for vector_set in sorted_into_bins: 
		unshifted = 0 
		for vector in vector_set: 
			radius = vector[0]**2 + vector[1]**2
			upperbound = efermi**2 + 0.00005
			lowerbound = efermi**2 - 0.00005
			if lowerbound <= radius <= upperbound: 
				unshifted += 1
		absolute = unshifted
		absolutes.append(absolute)
	middles = get_bin_middles(upper, lower, nbins, bins)
	fig, ax = plt.subplots()
	plt.scatter(middles, absolutes, s = 1)
	plt.xlabel("Length from emission")
	plt.ylabel("k-vectors on the centered fermi circle")
	plt.show()

def save_array(array, f, e, n_phonon, array_type): 
	date = str(datetime.date.today())
	loc = '../data_mcgraphenesim/'+array_type+'/'
	fstr = '_f'+str(f)+'_'
	estr = '_e'+str(e)+'_'
	name = loc+date+fstr+estr+str(n_phonon)+'.dat'
	np.savetxt(name, array)