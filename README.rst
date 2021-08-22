.. role:: raw-html-m2r(raw)
   :format: html


Price process generator
=======================

This library provides various vectorized generators of stochastic processes modelling price dynamics. 
The generated synthetic price data can be used in Monte Carlo simulations (or similar statistical experiments) and 
potentially as training data. 

Currently the implemented/planned generators are


* `Geometric Wiener motion <https://en.wikipedia.org/wiki/Geometric_Brownian_motion>`_
* `Geometric Lévy flights <https://en.wikipedia.org/wiki/L%C3%A9vy_process>`_
* `Ising <https://borab96.github.io/IsingPriceDynamics/ising.html>`_ 

Installation
------------

``pip install price_process`` to get the current PyPi version or clone this repo and run ``pip install .`` in the directory 
for most recent version.

Basic usage
-----------

The textbook stochastic price model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The standard model of stochastic price dynamics is the SDE

:raw-html-m2r:`<img src="https://latex.codecogs.com/svg.image?\color[rgb]{0.36,&space;0.54,&space;0.66}dP_t&space;=&space;\mu&space;S_t&space;dt&plus;\sigma&space;S_tdW_t" title="dP_t = \mu S_t dt+\sigma S_tdW_t" />`

with solution the *geometric Brownian motion*

:raw-html-m2r:`<img src="https://latex.codecogs.com/svg.image?\color[rgb]{0.36,&space;0.54,&space;0.66}P_t&space;=&space;P_0e^{\mu&space;t&plus;\frac{1}{2}t^2&space;\sigma}" title="\color[rgb]{0.36, 0.54, 0.66}P_t = P_0e^{\mu t+\frac{1}{2}t^2 \sigma}" />`

In order to display, say 10 samples of a 1000 point process, one would run

.. code-block::

   from price_process.process import *
   price_proc = Gaussian([1000, 10]).to_geometric(0, 0.04)
   price_proc.plot()


.. image:: ../examples/figures/exp_gaussian_ex.png
   :target: examples/figures/exp_gaussian_ex.png
   :alt: out:exp_gaussian


The ``np.ndarray`` output is accessed through ``price_proc.process``

Ising price model
^^^^^^^^^^^^^^^^^

Perhaps the most interesting generator that is currently implemented is the Ising model of price dynamics. This
is a statistical mechanical model that captures the competition between going with the local consensus trade decision and
contradiciting the consensus. Please refer to my `notebook <https://borab96.github.io/IsingPriceDynamics/ising.html>`_ for details of the model.

.. code-block::

   from price_process.process import *
   Ising(0.05, 500, [1000, 10]).plot()


.. image:: ../examples/figures/ising_ex.png
   :target: examples/figures/ising_ex.png
   :alt: out:ising


Note that ``Ising(...).process`` is already a price process so one should not evoke ``.to_geometric(drift, vol)``. See
the documentation for all the parameters of this model and recommended ranges. 

Custom process
--------------

Custom generators can be implemented by subclassing ``Process``. The only requirement is that ``self.size`` to be
given as an input of shape ``[n_steps, n_samples]`` and the desired process to be assigned to ``self.process``.

Here is how one might implement the gamma process
for instance

.. code-block::

   from price_process.process import *
   from scipy.stats import gamma
   import numpy as np

   class Gamma(Process):
       def __init__(self, alpha, beta, size, initial=0, T=1):
           super().__init__(size, initial=initial, T=T)
           self.alpha, self.beta = alpha, beta
           self.rvs = gamma.rvs(alpha, size=self.size, scale=1/self.beta)
           self.process = np.cumsum(self.rvs, axis=0)

See `this <https://datalore.jetbrains.com/view/notebook/7ePCXEffpdZr2dA5ySdwr1>`_ for a more advanced use case.
