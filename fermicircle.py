import numpy as np 

class Wave_vector(): 
	def __init__(self, fermi_circle): 
		self.vector = np.random.choice(fermi_circle.sample)



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