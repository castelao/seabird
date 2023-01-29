****************************
Getting Started with Seabird
****************************

Inside python
=============

    >>> import seabird



In a python script, one can use like this::

    >>> from seabird.cnv import fCNV
    >>> profile = fCNV('your_file.cnv')
    >>> profile.attributes  # It will return the header, as a dictionary.
    >>> profile.keys() # It will list the available variables.
    >>> profile['TEMP2'] # If TEMP2 was on the .keys(), this is how you get the data. It will be a masked array.

The data from a profile is hence treated as it was a dictionary of Masked Arrays. To plot it, one could::

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(profile['depth'], profile['TEMP'], '.')
    >>> plt.show()

From the terminal
=================

One way to use is running on the shell the cnvdump.
Independent of the historical version of the cnv file, it will return a default structure::

    seabird cnvdump your_file.cnv

That can be used in a regular shell script.
For example, let's consider a directory cruise1 with several sub directories, one for each leg of the cruise.
One could list all the latitudes of each CTD cast like::

    for file in `find ./cruise1 -iname '*.cnv'`
    do seabird cnvdump $file | grep latitude
    done

Now let's get that list ordered by the latitude::

    for file in `find ./cruise1 -iname '*.cnv'`
    do
        echo -n  `seabird cnvdump $file | grep latitude`
        echo -n " "
        echo $file
    done | sort -n > mylist.txt

To convert a .cnv to a standard NetCDF, run::

    seabird cnv2nc your_file.cnv

Quality Control
===============

Until version 10.X the package CoTeDe would import PySeabird to apply QC, but since 11.X this relation inverted, and PySeabird now imports CoTeDe's resources on QC to evaluate CTD and TSG data.

To QC a cnv file, first load the QC function::

    >>> from seabird.qc import fProfileQC

Now you're able to load the CTD data::

    >>> pqc = fProfileQC('example.cnv')

The keys() will give you the data loaded from the CTD, similar to the output from the seabird.fCNV::

    >>> pqc.keys()

To see one of the read variables listed on the previous step::

    >>> pqc['temperature']

The flags are stored at pqc.flags and is a dictionary, being one item per variable evaluated. For example, to see the flags for the secondary salinity instrument, just do::

    >>> pqc.flags['salinity2']

or for a specific test::

    >>> pqc.flags['salinity2']['gradient']

To evaluate a full set of profiles at once, use the class ProfileQCCollection, like:::

    >>> dataset = ProfileQCCollection('/path/to/data/', inputpattern=".*\.cnv")
    >>> dataset.flags['temperature'].keys()

The class cotede.qc.ProfileQCed is equivalent to the seabird.qc.ProfileQC, but it already mask the non approved data (flag != 1). Another it can also be used like:::

    >>> from seabird import cnv
    >>> data = cnv.fCNV('example.cnv')

    >>> import cotede.qc
    >>> ped = cotede.qc.ProfileQCed(data)

More examples
=============

I keep a notebooks collection of `practical examples handling CTD data <http://nbviewer.ipython.org/github/castelao/seabird/tree/master/docs/notebooks/>`_
.
If you have any suggestion, please let me know.
