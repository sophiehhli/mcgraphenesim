import numpy as np 

class K_vector(): 
	def __init__(self, fermi_circle): 
		self.vector = np.random.choice(fermi_circle.sample)

	def reflect(self): 
		return self.vector = - self.vector 

	def randomize(self, e_fermi): 
		return e_fermi * vp.random.sample(2)

class Fermi_circle():
	def __init__(self, e_fermi, N): 
		self.sample = self.gen_sample(e_fermi, N)

	def gen_sample(self, e_fermi, N): 
		angles = 2 * np.pi * random_sample(size=N/2)
		pos_vectors = [e_fermi * [np.cos(a), np.sin(a)] for a in angles]
		all_vectors = np.concatenate(pos_vectors, pos_vectors*pos_vectors)
		return all_vectors

	def shift(self, delta_kx): 
		self.sample += delta_kx

def gen_sample(self, e_fermi, N): 
	angles = 2 * np.pi * random_sample(size=N/2)
	pos_vectors = [e_fermi * [np.cos(a), np.sin(a)] for a in angles]
	all_vectors = np.concatenate(pos_vectors, pos_vectors*pos_vectors)
	return all_vectors

def shift_fermi(fermi_cirle, dx): 
	for v in fermi_circle: 
		v = v[0]+dx
	return fermi_circle
	
def pick_vector(fermi_circle): 
	vector  = np.random.choice(fermi_cicle)
	return vector 

