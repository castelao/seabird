#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Export the parsed data into a NetCDF following different patterns
"""

from __future__ import print_function
from datetime import datetime
import logging

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

    nc.history = "Created by cnv2nc (PyCNV)"

    nc.DATE_CREATION = datetime.now().strftime("%Y%m%s%H%M%S")

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

        for a in data[k].attrs.keys():
            print("\t\033[93m%s\033[0m: %s" % (a, data[k].attrs[a]))
            # cdf_variables[k].__setattr__(a, data[k].attrs[a])
        cdf_variables[k][:] = data[k].data

    nc.close()
