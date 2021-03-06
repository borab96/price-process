

<h1 align="center">Price process generator</h1>
<p align="center">A synthetic data source</p>




This library provides various vectorized generators of stochastic processes modelling price dynamics. 
The generated synthetic price data can be used in Monte Carlo simulations (or similar statistical experiments) and 
potentially as training data. 

Currently the implemented generators:

>- [Geometric Wiener motion](https://en.wikipedia.org/wiki/Geometric_Brownian_motion)
>- [Geometric Lévy flights](https://en.wikipedia.org/wiki/L%C3%A9vy_process)
>- [Ising](https://borab96.github.io/IsingPriceDynamics/ising.html)

Planned features:

- [ ] Generative adversarial network (GAN) implementation
- [ ] Improved interface with `ising.py` 

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/borab96/price_process/graphs/commit-activity)
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://price-process.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://binder.pangeo.io/badge_logo.svg)](TODO)

## Installation

``pip install price_process`` to get the current PyPi version or clone this repo and run ``pip install .`` in the directory 
for most recent version.

## Basic usage

### The textbook stochastic price model

The standard model of stochastic price dynamics is the SDE

<img src="https://latex.codecogs.com/svg.image?\color[rgb]{0.36,&space;0.54,&space;0.66}dP_t&space;=&space;\mu&space;S_t&space;dt&plus;\sigma&space;S_tdW_t" title="dP_t = \mu S_t dt+\sigma S_tdW_t" />

with solution the *geometric Brownian motion*

<img src="https://latex.codecogs.com/svg.image?\color[rgb]{0.36,&space;0.54,&space;0.66}P_t&space;=&space;P_0e^{\mu&space;t&plus;\frac{1}{2}t^2&space;\sigma}" title="\color[rgb]{0.36, 0.54, 0.66}P_t = P_0e^{\mu t+\frac{1}{2}t^2 \sigma}" />

In order to display, say 10 samples of a 1000 point process, one would run

````
from price_process.process import *
price_proc = Gaussian([1000, 10]).to_geometric(0, 0.04)
price_proc.plot()
````

<img src="examples/figures/exp_gaussian_ex.png">

[comment]: <> (![out:exp_gaussian]&#40;examples/figures/exp_gaussian_ex.png&#41;)

The `np.ndarray` output is accessed through `price_proc.process`

### The Levy stable process

The most immediate generalization to the Wiener process (Brownian motion) that
is still relevant to asset pricing is the [Levy stable process](https://galton.uchicago.edu/~lalley/Courses/385/LevyProcesses.pdf) which introduces two parameters
that respectively changes the tail weight and skewness as compared to the normal 
distribution. 

As in the previous example, we run

````
from price_process.process import *
Levy(1.5, 0.02, [1000, 10]).to_geometric(0, 0.05).plot().plot()
````

<img src="examples/figures/exp_levy_ex.png">




### Ising price model

Perhaps the most interesting generator that is currently implemented is the Ising model of price dynamics. This
is a statistical mechanical model that captures the competition between going with the local consensus trade decision and
contradiciting the consensus. Please refer to my [notebook](https://borab96.github.io/IsingPriceDynamics/ising.html) for details of the model.

````
from price_process.process import *
Ising(0.05, 500, [1000, 10]).plot()
````

<img src="examples/figures/ising_ex.png">

[comment]: <> (![out:ising]&#40;examples/figures/ising_ex.png&#41;)

Note that `Ising(...).process` is already a price process so one should not evoke `.to_geometric(drift, vol)`. See
the documentation for all the parameters of this model and recommended ranges. 

## Custom process

Custom generators can be implemented by subclassing ``Process``. The only requirement is that `self.size` to be
given as an input of shape `[n_steps, n_samples]` and the desired process to be assigned to `self.process`.

Here is how one might implement the gamma process
for instance

````
from price_process.process import *
from scipy.stats import gamma
import numpy as np

class Gamma(Process):
    def __init__(self, alpha, beta, size, initial=0, T=1):
        super().__init__(size, initial=initial, T=T)
        self.alpha, self.beta = alpha, beta
        self.rvs = gamma.rvs(alpha, size=self.size, scale=1/self.beta)
        self.process = np.cumsum(self.rvs, axis=0)
````

See [this notebook](https://datalore.jetbrains.com/view/notebook/7ePCXEffpdZr2dA5ySdwr1) for a more advanced use case (Gamma sampled
Wiener process).
