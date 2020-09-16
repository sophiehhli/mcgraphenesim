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
	interaction.polygon_boundary_response(f_list[f], curphonon, bound)
	return False

def polygon_loop(end, particle, f, bound, contacts): 
	line, intersection = interaction.polygon_intersection(particle, bound)
	line = list(line.coords)
	line = list(map(list,line))
	for c in contacts: 
		if line == c.coordinates: 
			c.response(particle, intersection)
			if c.type in ['source','drain']: 
				return True
			else:
				return False
	interaction.polygon_boundary_response(f, particle, bound, line, intersection)
	return False