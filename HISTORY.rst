.. :changelog:

History
-------

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
* XML is extracted into self.attributes['awkward_xml']

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
