Price process generator
=======================

This library provides various vectorized generators of stochastic
processes modelling price dynamics. The generated synthetic price data
can be used in Monte Carlo simulations (or similar statistical
experiments) and potentially as training data.

Currently the implemented/planned generators are

-  `Geometric Wiener
   motion <https://en.wikipedia.org/wiki/Geometric_Brownian_motion>`__
-  `Geometric Lévy
   flights <https://en.wikipedia.org/wiki/L%C3%A9vy_process>`__
-  `Ising <https://borab96.github.io/IsingPriceDynamics/ising.html>`__
   (TODO)

Installation
------------

``pip install price_process`` to get the current PyPi version or clone
this repo and run ``pip install .`` in the directory for most recent
version.

Basic usage
-----------

The standard model of stochastic price dynamics is the SDE

with solution the *geometric Brownian motion*

In order to display, say 10 samples of a 1000 point process, one would
run

::

    from price_process.process import *
    price_proc = Gaussian([1000, 10]).to_geometric(0, 0.04)
    price_proc.plot()

| The ``np.ndarray`` output is accessed through
| ``price_proc.process`` ## Custom process

Custom generators can be implemented by subclassing ``Process``. The
only requirement is that ``self.size`` to be given as an input of shape
``[n_steps, n_samples]`` and the desired process to be assigned to
``self.process``.

Here is how one might implement the gamma process for instance

::

    from price_process.process import *
    from scipy.stats import gamma
    import numpy as np

    class Gamma(Process):
        def __init__(self, alpha, beta, size, initial=0, T=1):
            super().__init__(size, initial=initial, T=T)
            self.alpha, self.beta = alpha, beta
            self.rvs = gamma.rvs(alpha, size=self.size, scale=1/self.beta)
            self.process = np.cumsum(self.rvs, axis=0)

See
`this <https://datalore.jetbrains.com/view/notebook/7ePCXEffpdZr2dA5ySdwr1>`__
for a more advanced use case.
