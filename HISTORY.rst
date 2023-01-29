.. :changelog:

History
-------

0.12.x
------

* Upgrading package structure. Before it was still an early Python-3 structure
  that limited to Python<3.8

0.11.x
------

* Migrating QC resources from CoTeDe to here. Until now CoTeDe would use PySeabird to understand CTD & TSG data files to QC, but now it is PySeabird that imports CoTeDe, as a plugin, to apply those same QC procedures.

0.10.x
------

* Data variables split by position. Rare cases use 11 characters thus not leaving any space between fields.
* Improved bottle dataset

0.9.x
-----

* This release is a dirty solution for some issues that I would like to address before refactor the whole package.
* Reads CTD bottle files (.btl)

0.8.x
-----

* Removed dependency on YAML, in favor to JSON.
* Added support to read binary file type.

0.7.x
-----

* Python 2.6 is no long supported.

0.6.x
-----

* CF vocabulary for variables names (PRES, TEMP, PSAL, LONGITUDE ...)
* Reorganizing the package. Removed src, and added several supporting files.
* Moving CNVError into seabird.exceptions
* Updated status for Production.
* Bugfix to md5hash a file with special latin1 characters.

0.5.9
-----

* New attributes, sbe_model and instrument_type.
* Sorry, lost track of updates.

0.5.3
-----

* Found a bug on load_data. Zeros could be mistaken by a bad_flag lower than 1e-8.
* The new rule accepts no notes on the header.
* Thanks to Laurynas for the .cnv file example that trigged the items above.

0.5.1
-----

* Testing structure
* Some minor improvements in the core.

0.4.4
-----

* Carolina Nobre provided some .cnv files without any time variable, i.e. no timeS, timeJ or timeQ. The CNV() will not fail anymore if lacks a time record.

0.4
---

* The oficial package name now is seabird. I realized that my goal here goes beyond to just parse the .cnv files, so the name seabird covers it better.

0.3
---

* cnv2nc, a script to convert the cnv into a netCDF file.

0.2
---

* First public release

0.1.8
-----

* Refactoring. Parsed text is saved in self.parsed, preparing to output
    everything that wasn't specifically parsed.
* XML is extracted into self.attrs['awkward_xml']

0.1.7
-----

* Now it calculate and include the hex md5sum.
* Bugfix, now handle well when timeJ has masked values.
* Bugfix converting timeJ, it was one day longer.
* I'll run on the whole PIRATA dataset to check against different formats
    and after that it will be ready for 0.2 as Beta version

0.1.6
-----

* When position available in the header.intro as NMEA, load this instead of
    try to parse from the header.notes.
* Load default values from a yaml file, like attributes{cruise, project,
    shipname ...}
* Using a recommended variable names list

0.1.5
-----

* Initial prototype of the cnvdump

0.1.1
-----

* Rules are now inside the package, and loaded with pkg_resources.

0.1
---

*Release date: 3-Jul-2012*

* Initial import.
* It's able to load the variables into Masked Array, but it's not the best way to do it.

pre-0.1
-------

This package was derived from what is now CoTeDe. It had a different name at
that time. Gui re-structure it in 2006 into a consistent Python package to
quality control TSG at NOAA/AOML. Operating with different models of TSGs and
different versions of outputs, it was crucial to parse and normalize those
into a consistent data model for a standard QC procedure.
