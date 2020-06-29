import numpy as np 
import matplotlib as plt

class Boundary():
	def __init__(self, x0=0, y0=0, width=1, height=1, radius=1): 
		self.x0 = x0 
		self.y0 = y0
		self.width = width
		self.height = height 
		self.radius = radius

	def boundary_eq(self): 
		return ((x-x0)/width)**2 + ((y - y0)/height)**2 - radius**2

plt.pyplot.contour()
plt.show()