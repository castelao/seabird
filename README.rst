PyCNV.
==========================

This is a parser for Sea Bird CTD output files.

The `Sea Bird CTD`_ post processed data usually uses the .cnv extention. The
purpose of the PyCNV is to parse this type of files, considering the different
versions along the time, as well as different setups.

At this point my goal is to have an object with the attributes parsed from the
header, and the data as Masked Arrays, so that the user don't need to loose
time evaluating the version and details of that cnv, but have it in a
standard pattern, ready to use.

The `Seasoft`_ manual might be the best reference for the format used.

.. _`Sea Bird`: http://www.seabird.com/software/SBEDataProcforWindows.htm
.. _`Seasoft`: http://www.seabird.com/pdf_documents/manuals/Seasoft_4.249Rev05-02.pdf

Support and Documentation
-------------------------

See the `PyCNV Wiki`_ to view documentation, report bugs, and obtain support.

.. _`PyCNV Wiki`: https://bitbucket.org/castelao/pycnv/wiki/Home

License
-------

``PyCNV`` is offered under the PSFL. I guess I need to put a link here?

Authors
-------

Guilherme Castelão <guilherme@castelao.net>
Roberto de Almeida <roberto@dealmeida.net>
Luiz Irber <luiz.irber@gmail.com>
