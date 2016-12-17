=======
Seabird
=======

.. image:: https://zenodo.org/badge/4645/castelao/seabird.svg
   :target: https://zenodo.org/badge/latestdoi/4645/castelao/seabird

.. image:: https://readthedocs.org/projects/seabird/badge/?version=latest
   :target: https://readthedocs.org/projects/seabird/?badge=latest
      :alt: Documentation Status

.. image:: https://img.shields.io/travis/castelao/seabird.svg
        :target: https://travis-ci.org/castelao/seabird

.. image:: https://codecov.io/github/castelao/seabird/coverage.svg?branch=master
    :target: https://codecov.io/github/castelao/seabird?branch=master

.. image:: https://img.shields.io/pypi/v/seabird.svg
        :target: https://pypi.python.org/pypi/seabird


This is a parser for Sea Bird CTD and TSG output files.

The `Sea Bird CTD`_ post processed data usually uses the .cnv extention. The purpose of the PySeabird is to parse this type of files, considering the different versions along the time, as well as different setups.

At this point my goal is to have an object with the attributes parsed from the header, and the data as Masked Arrays, so that the user doesn't need to loose time evaluating the version and details of that cnv, but have it in a standard pattern, ready to use.

ATENTION, this is not an official package, so if you have trouble with it, do not complain to Sea-Bird. Open an issue at GitHub (https://github.com/castelao/seabird/issues), and I'll try to help you.

.. _`Sea Bird CTD`: http://www.seabird.com/software/SBEDataProcforWindows.htm

Support and Documentation
-------------------------

The documentation is available at `seabird.readthedocs.org`_.

The `Seasoft`_ manual might be the best reference for the format used.

If PySeabird doesn't work with your .cnv files, send me a sample (just one .cnv) and I'll fix to run it. The SeaBird changed the format several times along the time, so I need to see what do you have, to adjust PySeabird to work with it.

.. _`seabird.readthedocs.org`: http://seabird.readthedocs.org
.. _`Seasoft`: http://www.seabird.com/pdf_documents/manuals/Seasoft_4.249Rev05-02.pdf

Quick howto use
---------------

To install:

    pip install seabird


One way to use is running on the shell the cnvdump. Independent of the historical version of the cnv file, it will return a default structure: 

    seabird cnvdump your_file.cnv


To convert a .cnv (CTD output) into a NetCDF file, run:

    seabird cnv2nc your_file.cnv


In a python script, one can use like this:

    from seabird.cnv import fCNV

    profile = fCNV('your_file.cnv')

    profile.attributes  # It will return the header, as a dictionary.

    profile.keys() # It will list the available variables.

    profile['TEMP2'] # If TEMP2 was on the .keys(), this is how you get the data. It will be a masked array.


Check the example notebooks: http://nbviewer.ipython.org/github/castelao/seabird/tree/master/docs/notebooks/


License
-------

``seabird`` is licensed under a 3-clause BSD style license - see LICENSE.rst

Authors
-------

Guilherme Castelão <guilherme@castelao.net> and Luiz Irber <luiz.irber@gmail.com>
