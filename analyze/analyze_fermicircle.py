import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import datetime 

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