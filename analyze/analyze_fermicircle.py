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
	print('length deviations: '+ str(len(deviations)))
	print('length emissions: '+ str(len(emissions)))
	for i in range(len(emissions)): 
		if emissions[i][0] > lower and emissions[i][0] < upper:
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

def find_list_mean(sorted_into_bins):
	means = [np.mean(sublist) for sublist in sorted_into_bins]
	return means

def plot_binned_deviations(original, centers, emissions, lower, upper, nbins): 
	deviations = convert_to_deviation(original, centers)
	x,y = construct_data_set(emissions, deviations, lower, upper)
	bins, sorted_into_bins = binning(x, y, nbins, lower, upper)
	means = find_list_mean(sorted_into_bins)
	binwidth = (upper-lower)/nbins
	centers = bins[:-1] + binwidth/2
	fig, ax = plt.subplots()
	plt.scatter(centers, means, s=1)
	plt.xlabel("Length from emission (cm)")
	plt.ylabel("Fermi circle deviation form unshifted")
	plt.show()

def fermi_circles_from_kvectors(original, k_vectors, emmisions, lower, upper, nbins):
	x, y = construct_data_set(emmisions, k_vectors, lower, upper)
	bins, sorted_into_bins = binning(x, y, nbins, lower, upper)
	centers =[]
	for vector_set in sorted_into_bins: 
		center = convert_to_center(vector_set)
		centers.append(center)
	deviations = convert_to_deviation(original, centers)
	binwidth = (upper-lower)/nbins
	middle = bins[:-1] + binwidth/2
	fig, ax = plt.subplots()
	plt.scatter(middle, deviations, s=1)
	plt.xlabel("Length from emission (cm)")
	plt.ylabel("Fermi circle deviation form unshifted")
	plt.show()
