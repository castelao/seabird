#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Export the parsed data into a NetCDF following different patterns
"""

from __future__ import print_function
from datetime import datetime, date, time
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

    nc.DATE_CREATION = datetime.now().strftime("%Y%m%d%H%M%S")

    # print "Global attributes"
    A = sorted(data.attrs.keys())
    for a in A:
        try:
            if type(data.attrs[a]) is datetime:
                nc.__setattr__(a, data.attrs[a].isoformat())
            else:
                nc.__setattr__(a, data.attrs[a])
        except:
            module_logger.warning("Problems with %s" % a)

    real_values = len(data[data.keys()[0]])
    if     real_values != int(data.attributes['nvalues']):
        print("\033[91mATENTION The data suggest '%s' records are available while the header suggest '%s' records." % (real_values, data.attributes['nvalues']))
    nc.createDimension('scan', len(data[data.keys()[0]]))

    print("\nVariabes")
    cdf_variables = {}
    for k in data.keys():
        print(k)
        # handle datetime variables, convert to string format 
        if data[k].dtype == object and type(data[k][0]) in (datetime,time,date):
            str_values = data[k].data.astype(str)
            string_length = len(str_values[0])
            cdf_variables[k] = nc.createVariable(k, 'S' + str(string_length), ('scan',))
            cdf_variables[k][:] = str_values
            continue

        if k in cdf_variables:
            print("\033[91mATENTION The duplicated variables are not"
            " compatible with the NetCDF Format. "
            "The very first variable '%s' will be considered." % k)
            continue

        try:
            cdf_variables[k] = nc.createVariable(k, 'd', ('scan',))
        except:
            cdf_variables[k] = nc.createVariable(
                    k.decode('utf8', 'ignore'), 'd', ('scan',))
            print("\033[91mATENTION, I need to ignore the non UTF-8 "
                  "characters in '%s' to create the netCDF file.\033[0m" % k)
        
        # Ignore unknown fill_value
        if data[k].fill_value not in ['?','N/A'] :
            cdf_variables[k].missing_value = data[k].fill_value

        for a in data[k].attrs.keys():
            print("\t\033[93m%s\033[0m: %s" % (a, data[k].attrs[a]))
            # cdf_variables[k].__setattr__(a, data[k].attrs[a])

        cdf_variables[k][:] = data[k].data

    nc.close()
