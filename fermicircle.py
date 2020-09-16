import numpy as np 

def gen_sample(e_fermi, N): 
	angles = 2 * np.pi * np.random.random_sample(size= int(N/2))
	pos_vectors = [e_fermi * np.array([np.cos(a), np.sin(a)]) for a in angles]
	all_vectors = np.concatenate((pos_vectors, -1*np.array(pos_vectors)))
	return all_vectors

class Fermi_circle():
	def __init__(self, sample, e_fermi): 
		self.sample = sample
		self.n = len(sample)
		self.e_fermi = e_fermi

	def shift(self, d_kx):
		add = np.zeros((self.n, 2))
		add[:,0] = d_kx
		return self.sample + add

	def pick_vector_index(self): 
		return np.random.randint(0,len(self.sample))

	def reflect(self, i): 
		self.sample[i] = -self.sample[i]

	def randomize(self, i): 
		self.sample[i] = self.e_fermi * np.random.sample(2)