********
Overview
********

Seabird is a popular brand of sensors used for hydrographic measurements around the world, and that means most of the historical CTD data. 
These hydrographic profiles are usually available as ASCII files, containing the data itself and plenty of fundamental metadata as position, date, calibration coefficients and many more. 
It is not hard for a human to interpret it, but its format have been changing, and so it is a problem for a machine.

While working with several years of CTD data from the project PIRATA, I realized that the first problem is to just be able to properly read all the data. 
I built this Python package with the goal to parse, in a robust way, the different historical Seabird output data files, and return in a regular structure.

At this point my goal is to have an object with the attributes parsed from the header, and the data as Masked Arrays, so that the user don't need to loose time evaluating the version and details of that .cnv file, but have it in a standard pattern, ready to use.
Taking advantage of the basic library, this package comes with some binary commands to output the content as ASCII but in persistent format, or to convert it into a NetCDF file.

ATENTION, this is not an official package, so if you have trouble with this package, do not complain to Sea-Bird. 
Instead, open an issue at GitHub (https://github.com/castelao/seabird/issues), and I'll try to help you.

