#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Export the parsed data into a NetCDF following different patterns
"""

from __future__ import print_function
from datetime import datetime, date, time
import logging
import numpy as np

module_logger = logging.getLogger('seabird.netcdf')

try:
    import netCDF4
except:
    module_logger.warning("netCDF4 is not available.")


def cnv2nc(data, filename):
    """ Save a CNV() object into filename as a NetCDF

        To save the CTD.cnv into a NetCDF, just run:

        profile = cnv.fCNV("CTD.cnv")
        cnv2nc(profile, "CTD.nc")
    """
    print("Saving netcdf output file: %s" % filename)

    nc = netCDF4.Dataset(filename, 'w', format='NETCDF4')

    nc.history = "Created by cnv2nc (seabird)"

    nc.DATE_CREATION = datetime.now().strftime("%Y%m%d%H%M%S")

    # print "Global attributes"
    A = sorted(data.attrs.keys())
    for a in A:
        try:
            nc.__setattr__(a, data.attrs[a])
        except:
            module_logger.warning("Problems with %s" % a)

    # Assign bottle number as a dimension for bottle data, otherwise stay with scan value
    # TODO could add time if timeseries and depth/pressure if bin data
    if data.attrs['instrument_type'] == 'CTD-bottle':
        nc.createDimension('bottle', len(data.data[0]))
        dimVar = 'bottle'
    else:
        nc.createDimension('scan', int(data.attrs['nvalues']))
        dimVar = 'scan'

    print("\nVariabes")
    cdf_variables = {}
    for k in data.keys():
        print(k)
        try:
            cdf_variables[k] = nc.createVariable(k, 'd', (dimVar,))
        except:
            cdf_variables[k] = nc.createVariable(
                    k.decode('utf8', 'ignore'), 'd', (dimVar,))
            print("\033[91mATENTION, I need to ignore the non UTF-8 "
                  "characters in '%s' to create the netCDF file.\033[0m" % k)
        try:
            cdf_variables[k].missing_value = data[k].fill_value
        except:
            print(str(data[k].attrs['name']) + ': Ignore fill_value')

        # Add attributes available
        for a in data[k].attrs.keys():
            print("\t\033[93m%s\033[0m: %s" % (a, data[k].attrs[a]))
            cdf_variables[k].setncattr(a, data[k].attrs[a])

        # Deal with time separately
        if data[k].dtype == object:
            if issubclass(type(data[k][0]), date) or issubclass(type(data[k][0]), datetime):
                cdf_variables[k][:] = data[k].data.astype('datetime64[s]').astype('float64')
                cdf_variables[k].units = 'seconds since 1970-01-01T00:00:00'

                # TODO need one specific to timezone aware times
            elif issubclass(type(data[k][0]), time):
                fraction_of_day = []
                for time_ in data[k]:
                    fraction_of_day.append(
                        (time_.hour + (time_.minute + (time_.second + time_.microsecond / 1000) / 60) / 60) / 24)

                cdf_variables[k][:] = fraction_of_day
                cdf_variables[k].units = 'Fraction of day'

        else:
            cdf_variables[k][:] = data[k].data

    nc.close()
