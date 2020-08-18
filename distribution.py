import scipy.stats 
import numpy as np

class Fermi_dirac(rv_continuous): 
    "Fermi Dirac distribution"
    def _pdf(self, eps, mu, T):
        self.mu = mu
        self.T = T
        return 1/(np.exp((eps - mu)/(kB * T)) + 1)
    def _cdf(self, eps, mu, T):
       
    def _stats(self, eps, mu, T):
    