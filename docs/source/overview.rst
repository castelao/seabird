********
Overview
********

Seabird is a popular brand of sensors used for hydrographic measurements around the world, and that means a great deal of historical CTD data. 
These hydrographic profiles are usually available as ASCII files, containing the data itself, and plenty of fundamental metadata, such as position, date, calibration coefficients, and much more. 
Typically, these files are not hard for a human to interpret, but their format has changed over time, so it is a problem for automated processing.

While working with several years of CTD data from the project PIRATA, I realized that the first problem is just to be able to properly read all the data. 
I built this Python package with the goal to parse, in a robust way, the different historical Seabird output data file formats, and return that data in a uniform structure.

At this point, my goal is to have an object with attributes parsed from the header, and the data in (NumPy) Masked Arrays, so that the user doesn't need to manually determine the version and details of a .cnv file, but will still have it in a standard pattern, ready to use. 
Taking advantage of the basic library, this package includes some binary commands to output content as ASCII, but in a persistent format, or to convert it into a NetCDF file.

ATTENTION: this is not an official Sea-Bird package, so if you have trouble with it, please do not complain to Sea-Bird. 
Instead, open an issue at GitHub (https://github.com/castelao/seabird/issues), and I'll try to help you.

