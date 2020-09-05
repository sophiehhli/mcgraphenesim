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
			newphonon = c.response(curphonon)
			if c.type in ['source','drain']:
				return [True, newphonon]
			else: 
				return [False, newphonon]
	newphonon = interaction.polygon_boundary_response(f_list[f], curphonon, bound, contacts)
	interaction.plot_trajectory(curphonon, newphonon)
	return [False, newphonon]

def polygon_loop(end, curphonon, f, bound, contacts): 
	line, intersection = interaction.polygon_intersection(curphonon, bound)
	line = list(line.coords) 
	line = list(map(list,line))
	for c in contacts: 
		if line == c.coordinates: 
			newphonon = c.response(curphonon)
			interaction.plot_trajectory(curphonon, newphonon)
			return [True, newphonon]
	newphonon = interaction.polygon_boundary_response(f, curphonon, bound, contacts)
	interaction.plot_trajectory(curphonon, newphonon)
	return [False, newphonon]