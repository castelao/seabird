************
Installation
************

Requirements
============

- `Python <http://www.python.org/>`_ 2.6 (>=2.6.5), 2.7, 3.1 or 3.2

- `Numpy <http://www.numpy.org>`_ (>=1.1)

Optional requirement
--------------------

- `NetCDF4 <https://pypi.python.org/pypi/netCDF4>`_, if you want to be able to export the data into netCDF files.


Installing Seabird 
==================

Using pip
---------

First you need to `install pip <https://pip.pypa.io>`_, then you can run:

    pip install seabird

Alternative
-----------
    pip install --no-deps seabird

.. note::

    The ``--no-deps`` flag is optional, but highly recommended if you already
    have Numpy installed, otherwise pip will sometimes try to "help" you
    by upgrading your Numpy installation, which may not always be desired.
