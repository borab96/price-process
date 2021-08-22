.. Price Process documentation master file, created by
   sphinx-quickstart on Sun Aug 22 14:27:02 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.




.. include:: ../_README.rst


Docs
======

The Process() base class
-------------------------

.. autoclass:: price_process.process.Process
    :special-members: __init__
    :members:
    :inherited-members:


Gaussian() subclass of Brownian motion
---------------------------------------

.. autoclass:: price_process.process.Gaussian
    :special-members: __init__
    :members:

Levy() subclass of Levy flights
---------------------------------------

.. autoclass:: price_process.process.Levy
    :special-members: __init__
    :members:

Ising() subclass of Ising price dynamics
------------------------------------------

.. autoclass:: price_process.process.Ising
    :special-members: __init__
    :members:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
