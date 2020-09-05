import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import datetime 

def show_boundary(bound, contacts): 
	bound.plot()
	for c in contacts: c.plot()
	plt.show()
