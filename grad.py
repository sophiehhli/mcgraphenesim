import numpy as np 

def grad_circle(x, y, x0, y0, width, height): 
	"""gradient of the dedined cicle at point (x,y)"""
	v = np.zeros(2)
	v[0] = 2*(x-x0)*(1/width**2)
	v[1] = 2*(y-y0)*(1/height**2)
	return v/np.linalg.norm(v)

def grad_line(start, end):
	"""gradient of a line with start and end points"""
	v = np.zeros(2)
	v[0] = end[1] - start[1]
	v[1] = end[0] - start[0]
	return v/np.linalg.norm(v)

""" Must be carful with how the start and end of a line are inputted
define inward pointing normal to the right of travel 
drain: top to bottom 
source: bottom to top""" 