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

More examples
=============

I keep a notebooks collection of `practical examples handling CTD data <http://nbviewer.ipython.org/github/castelao/seabird/tree/master/docs/notebooks/>`_
. 
If you have any suggestion, please let me know.
