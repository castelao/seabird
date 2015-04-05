seabird
=======

This is a parser for Sea Bird CTD output files.

The `Sea Bird CTD`_ post processed data usually uses the .cnv extention. The purpose of the PySeabird is to parse this type of files, considering the different versions along the time, as well as different setups.

At this point my goal is to have an object with the attributes parsed from the header, and the data as Masked Arrays, so that the user doesn't need to loose time evaluating the version and details of that cnv, but have it in a standard pattern, ready to use.

ATENTION, this is not an official package, so if you have trouble with it, do not complain to Sea-Bird. Open an issue at GitHub (https://github.com/castelao/seabird/issues), and I'll try to help you.

.. _`Sea Bird CTD`: http://www.seabird.com/software/SBEDataProcforWindows.htm

Support and Documentation
-------------------------

The documentation is available at `seabird.readthedocs.org`_.

The `Seasoft`_ manual might be the best reference for the format used.

The variables names were based on the `pcmdi standard name table`_

If PySeabird doesn't work with your .cnv files, send me a sample (just one .cnv) and I'll fix to run it. The SeaBird changed the format several times along the time, so I need to see what do you have, to adjust PySeabird to work with it.

.. _`seabird.readthedocs.org`: http://seabird.readthedocs.org
.. _`Seasoft`: http://www.seabird.com/pdf_documents/manuals/Seasoft_4.249Rev05-02.pdf
.. _`pcmdi standard name table`: http://cf-pcmdi.llnl.gov/documents/cf-standard-names/standard-name-table/19/cf-standard-name-table.html

Quick howto use
---------------

To install:

    pip install seabird


One way to use is running on the shell the cnvdump. Independent of the historical version of the cnv file, it will return a default structure: 

    cnvdump your_file.cnv


To convert a .cnv (CTD output) into a NetCDF file, run:

    cnv2nc your_file.cnv


In a python script, one can use like this:

    from seabird.cnv import fCNV

    profile = fCNV('your_file.cnv')

    profile.attributes  # It will return the header, as a dictionary.

    profile.keys() # It will list the available variables.

    profile['temperature2'] # If temperature2 was on the .keys(), this is how you get the data. It will be a masked array.


Check the example notebooks: http://nbviewer.ipython.org/github/castelao/seabird/tree/master/docs/notebooks/


License
-------

``seabird`` is offered under the PSFL.

Authors
-------

Guilherme Castelão <guilherme@castelao.net> and Luiz Irber <luiz.irber@gmail.com>
