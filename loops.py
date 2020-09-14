import boundary
import point
import interaction
import contact
import analyze
import time 

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime

def phonon_loop(end, curphonon, f, bound, contacts, specie): 
	for c in contacts: 
		if c.check_intersection(curphonon): 
			c.response(curphonon)
			if c.type in ['source','drain']:
				return True
			else: 
				return False
	newphonon = interaction.polygon_boundary_response(f_list[f], curphonon, bound, contacts)
	#interaction.plot_trajectory(curphonon, newphonon)
	return False

def polygon_loop(end, particle, f, bound, contacts): 
	line, intersection = interaction.polygon_intersection(particle, bound)
	line = list(line.coords)
	line = list(map(list,line))
	for c in contacts: 
		if line == c.coordinates: 
			c.response(particle)
			#interaction.plot_trajectory(curphonon, newphonon)
			return True
	interaction.polygon_boundary_response(f, particle, bound, contacts)
	#interaction.plot_trajectorys(curphonon, newphonon)
	return False