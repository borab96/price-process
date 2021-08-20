from scipy.stats import norm, levy_stable



class Distributions():
    def __init__(self, size):
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

    def gaussian(self, mean=0, std=1):
        self.mean = mean
        self.std = std
        return norm.rvs(mean, std, self.size)
