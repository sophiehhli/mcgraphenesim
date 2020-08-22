import scipy.stats as stats 
import numpy as np

kB = 1.3807 * 10 ** (-23)

class Fermi_dirac(stats.rv_continuous): 
    "Fermi Dirac distribution"
    def _pdf(self, eps, mu, T):
        self.mu = mu
        self.T = T
        return 1/(np.exp((eps - mu)/(kB * T)) + 1)

    def _cdf(self, eps, mu, T):
       return eps + kB * T *(np.log(1+np.exp(-mu/(kB * T))) - np.log(1+np.exp((-mu+eps)/(kB * T))))

    '''def _stats(self, eps, mu, T):''' 
fermi_dirac = Fermi_dirac(name = "fermi_dirac")

samples = fermi_dirac.rvs(mu=1, T = 5*10**4, size = 10)

print(samples)

class gaussian_gen(stats.rv_continuous):
	"Gaussian distribution"
	def _pdf(self, x):
		return np.exp(-x**2 / 2.) / np.sqrt(2.0 * np.pi)

gaussian = gaussian_gen(name='gaussian')

samples = gaussian.rvs(size = 10)

print(samples)