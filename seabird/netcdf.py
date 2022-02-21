#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Export the parsed data into a NetCDF following different patterns
"""

from __future__ import print_function
from datetime import datetime, date, time
import logging

module_logger = logging.getLogger("seabird.netcdf")

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
    logging.info("Saving netcdf output file: %s" % filename)

    nc = netCDF4.Dataset(filename, 'w', format='NETCDF4')

    nc.history = "Created by cnv2nc (PyCNV)"

    nc.date_created = datetime.now().isoformat()

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
    if 'nvalue' not in data.attributes:
        logging.warning('Unknown original data length, nvalues not available within the cnv file.')
    elif real_values != int(data.attributes["nvalues"]):
        logging.warning(
            "\033[91mATENTION The data suggest '%s' records are available while the header suggest '%s' records]."
            % (real_values, data.attributes["nvalues"])
        )

    logging.info("\nVariabes")
    cdf_variables = {}
    for k in data.keys():
        logging.info(k)
        # handle datetime variables, convert to string format 
        if data[k].dtype == object and type(data[k][0]) in (datetime,time,date):
            str_values = data[k].data.astype(str)
            string_length = len(str_values[0])
            cdf_variables[k] = nc.createVariable(k, 'S' + str(string_length), ('scan',))
            cdf_variables[k][:] = str_values
            continue

        if k in cdf_variables:
            logging.warning(
                "\033[91mATENTION The duplicated variables are not"
                " compatible with the NetCDF Format. "
                "The very first variable '%s' will be considered." % k
            )
            continue

        try:
            cdf_variables[k] = nc.createVariable(k, 'd', ('scan',))
        except:
            ik = k
            k = k.replace('/','Per')
            cdf_variables[k] = nc.createVariable(
                    k, 'd', ('scan',))
            logging.warning("\033[91mATENTION, I need to ignore the non UTF-8 "
                  "characters in '%s' by '%s' to create the netCDF file.\033[0m" % (ik,k))
        
        # Ignore unknown fill_value
        if data[k].fill_value not in ['?','N/A'] :
            cdf_variables[k].missing_value = data[k].fill_value

        for a in data[k].attrs.keys():
            logging.info("\t\033[93m%s\033[0m: %s" % (a, data[k].attrs[a]))
            # cdf_variables[k].__setattr__(a, data[k].attrs[a])

        cdf_variables[k][:] = data[k].data

    nc.close()
