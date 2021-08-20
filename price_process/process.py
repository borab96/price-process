import numpy as np
import scipy as sc
from scipy import stats
from math import factorial
from scipy.stats import norm, uniform, levy_stable
import matplotlib.pyplot as plt
from distributions import *

def normalize(vec):
    return vec/np.max(np.abs(vec))

class Process():

    def __init__(self, size, initial=0, T=1):
        if hasattr(size, "__len__"):
            if len(size) != 2:
                raise ValueError(f"size of random matrix to be generated must be 2, not {len(size)}")
            else:
                self.n_steps = size[0]
                self.n_samples = size[1]
        else:
            self.n_steps = size
            self.n_samples = 1
        self.size = size
        self.initial = initial
        self.t = np.linspace(0, T, self.n_steps)
        self.process = None
        self.log_process = None

    def to_geometric(self, drift, vol):
        self.log_process = self.process
        self.process = np.exp(self.log_process*vol+(drift-0.5*vol**2))
        return self

    def plot(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.t, self.process)
        plt.xlabel(r'$t$')
        plt.ylabel(r'$P_t$')
        plt.show()



class Gaussian(Process):
    def __init__(self,size, mu=0, std=1, initial=0, T=1):
        super().__init__(size, initial=initial, T=T)
        self.mu, self.std = mu, std
        if self.mu != 0 or self.std != 1:
            raise Warning("Using non-standard underlying process")
        self.rvs = norm.rvs(mu, std, self.size)
        self.process = np.cumsum(self.rvs, axis=0)


class Levy(Process):
    def __init__(self, alpha, beta, size, mu=0, std=1, initial=0, T=1):
        super().__init__(size, initial=initial, T=T)
        if 0 < alpha <= 2 and -1 <= beta <= 1:
            self.alpha, self.beta = alpha, beta
        else:
            raise ValueError("Parameter bounds: 0<alpha<=2, -1<=beta<=1")

        self.mu, self.std = mu, std
        self.rvs = levy_stable.rvs(self.alpha, self.beta, size=self.size, loc=mu, scale=std**2)
        if self.mu != 0 or self.std != 1:
            raise Warning("Using non-standard underlying process")
        self.process = np.cumsum(self.rvs, axis=0)

    def plot_pdf(self, bounds=(-7, 7), n=200):
        x = np.linspace(*bounds, n)
        plt.plot(x, normalize(levy_stable.pdf(x, self.alpha, self.beta, loc=self.mu, scale=self.std)), label=f"Levy ({self.alpha}, {self.beta})")
        plt.plot(x, normalize(norm.pdf(x, loc=self.mu, scale=self.std*np.sqrt(2))), '--', label="Normal")
        plt.legend()
        plt.show()


# Levy(1.5, -0.01, [100, 5]).to_geometric(0, 0.1).plot()
# Levy(1.5, 0, [100, 5]).plot_pdf()

Gaussian([1000, 10]).to_geometric(0, 0.04).plot()
