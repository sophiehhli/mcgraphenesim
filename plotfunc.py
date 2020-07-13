import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import datetime 

def polar_thetas(list_intersections): 
	polarthetas = [np.arctan(c[1]/c[0]) for c in list_intersections]
	plt.hist(polarthetas,100)
	plt.title("Interactions by polar angle", fontsize=8)
	plt.xlabel('Theta')
	plt.ylabel('Interaction frequency')
	plt.show()

def transmitted_precent(drain, source): 
	return (drain / (drain + source))

def save_array(array, bound):
	date = str(datetime.date) 
	savetext(bound.name + date, array, delimeter = ' ')