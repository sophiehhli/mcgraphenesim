import matplotlib.pyplot as plt
import numpy as np
import datetime 

def transmitted_precent(drain, source): 
	"""calulates the precentage of particles transmitted to the drain""" 
	return (drain / (drain + source))
