PyCNV
==========================

This is a parser for Sea Bird CTD output files.

The `Sea Bird CTD`_ post processed data usually uses the .cnv extention. The
purpose of the PyCNV is to parse this type of files, considering the different
versions along the time, as well as different setups.

At this point my goal is to have an object with the attributes parsed from the
header, and the data as Masked Arrays, so that the user don't need to loose
time evaluating the version and details of that cnv, but have it in a
standard pattern, ready to use.

.. _`Sea Bird`: http://www.seabird.com/software/SBEDataProcforWindows.htm

Support and Documentation
-------------------------

See the `PyCNV Wiki`_ to view documentation, report bugs, and obtain support.

The `Seasoft`_ manual might be the best reference for the format used.

The variables names were based on the `pcmdi standard name table`

If PyCNV don't work with your .cnv files, send me a sample (just one .cnv) and I'll fix to run it. The SeaBird changed the format several times along the time, so I need to see what do you have, to adjust PyCNV to work with it.

.. _`PyCNV Wiki`: http://pycnv.castelao.net
.. _`Seasoft`: http://www.seabird.com/pdf_documents/manuals/Seasoft_4.249Rev05-02.pdf
.. _`pcmdi standard name table`: http://cf-pcmdi.llnl.gov/documents/cf-standard-names/standard-name-table/19/cf-standard-name-table.html

Fast howto use
--------------

To install:

pip install pycnv

One way to use is running on the shell the cnvdump. Independent of the historical version of the cnv file, it will return a default structure: 

cnvdump your_file.cnv

To convert a .cnv to a NetCDF, run:

cnv2cdf your_file.cnv

In a python script, one way to do it is:

profile = fCNV('your_file.cnv')

profile will be an object, always with the same pattern.

License
-------

``PyCNV`` is offered under the PSFL. I guess I need to put a link here?

Authors
-------

Guilherme Castelão <guilherme@castelao.net>
Luiz Irber <luiz.irber@gmail.com>
