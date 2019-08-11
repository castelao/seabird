************
Installation
************

Requirements
============

- `Python <http://www.python.org/>`_ 2.7 or 3.X (recommended >=3.5)

- `Numpy <http://www.numpy.org>`_ (>=1.1)

Optional requirement
--------------------

- `netCDF4 <https://pypi.python.org/pypi/netCDF4>`_, if you want to be able to export the data into netCDF files.

- `CoTeDe <http://cotede.castelao.net>`_, if you want to quality control your profiles, install the latest version of CoTeDe with PIP::

    pip install git+https://github.com/castelao/CoTeDe.git

Installing Seabird 
==================

Virtual Environments
--------------------

You don't need to, but I strongly recommend to use `virtualenv <https://virtualenv.pypa.io/en/stable/>`_ or `conda <https://conda.io/en/latest/>`_.

Using pip
---------

Currently, the most convenient way to install is with pip, by running in the terminal::

    pip install seabird

If you don't have pip installed, you'll need to `install pip <https://pip.pypa.io>`_ first.
